from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.template.loader import render_to_string
from django.views import generic

from .forms import (CustomUserCreationForm, OfferModelForm,
                    WishlistItemModelForm)
from .models import Offer, Supermarket, User, WishlistItem


class SingupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class ContactView(generic.CreateView):
    template_name = "contact.html"
    form_class = CustomUserCreationForm # DELETE/FIX

class HomePageView(generic.ListView):
    template_name = "offers/offers_list.html"
    queryset = Offer.objects.filter(is_active=True)
    # context_object_name = "offers"


class WishlistView(LoginRequiredMixin, generic.ListView):
    template_name = "wishlist.html"
    
    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).order_by("-created_on")


class WishlistMultiActionView(LoginRequiredMixin, generic.ListView):
    template_name = "wishlist.html"
    
    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).order_by("-created_on")
    
    def post(self, request):
        wishlist_item_ids = request.POST.getlist('wishlist-item')
        multi_action_val = request.POST.get('multi-action-val')

        wishlist_items_for_action = WishlistItem.objects.filter(id__in=tuple(wishlist_item_ids))
        
        if multi_action_val == "enable":
            wishlist_items_for_action.update(is_active=True)
        elif multi_action_val == "disable":
            wishlist_items_for_action.update(is_active=False)
        elif multi_action_val == "delete":
            wishlist_items_for_action.delete()

        return redirect("wishlist")


class WishlistItemDetail(LoginRequiredMixin, generic.DetailView):
    template_name = "wishlist_item_detail.html"
    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user) # It will automatically grab pk
    context_object_name = "wishlist_item"


class OfferListView(generic.ListView):
    template_name = "offers/offers_list.html"
    model = Offer
    context_object_name = 'offer'
    paginate_by = 2  # Show 8 products per page

    def get_queryset(self):
        queryset = super().get_queryset()
        self.selected_supermarkets = [int(i) for i in self.request.GET.getlist('sm')]
        if self.selected_supermarkets:
            queryset = queryset.filter(supermarket__in=self.selected_supermarkets)
        self.offer_search = self.request.GET.get("offer_search")
        if self.offer_search:
            queryset = queryset.filter(product_name__icontains=self.offer_search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supermarkets'] = Supermarket.objects.all()
        context['selected_supermarkets'] = self.selected_supermarkets
        context['offer_search'] = self.offer_search
        return context
    
    def get(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            # Process AJAX request
            paginator = Paginator(self.get_queryset(), self.paginate_by)
            page_number = request.GET.get("page", 1)
            page_obj = paginator.get_page(page_number)
            return JsonResponse({
                'html_from_view_offer_list': render_to_string('offers/offers_list_ajax.html', {'object_list': page_obj}),
                'html_from_view_pagination': render_to_string('offers/pagination.html', {'page_obj': page_obj, 'paginator': paginator, 'selected_supermarkets': self.selected_supermarkets, 'request': request}),
            })
        else:
            # Render regular HTML response
            return super().get(request, *args, **kwargs)


class OfferDetailView(generic.DetailView):
    template_name = "offers/offer_details.html"
    queryset = Offer.objects.all()
    context_object_name = "offer"

    def get_queryset(self):
        queryset = super().get_queryset()
        tab_clicked = self.request.GET.get("tab_clicked")
        offer_name = self.request.GET.get("offer_name")
        
        if tab_clicked == "exp":
            if offer_name:
                queryset = queryset.filter(product_name__icontains=offer_name, is_active=False)
        
        return queryset


    def get(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            queryset = self.get_queryset()
            tab_clicked = request.GET.get("tab_clicked", 1)
            if tab_clicked == "desc":
                html_template_name = "offers/offer_details_inner.html"
                offer = self.get_object()
                return JsonResponse({
                    'html_from_offer_detail_view': render_to_string(html_template_name, {'offer': offer}),
                })
            elif tab_clicked == "exp":
                html_template_name = "offers/exp_offers.html"
                return JsonResponse({
                    'html_from_offer_detail_view': render_to_string(html_template_name, {'exp_offers': queryset}),
                })
            else:
                raise Exception("Unidentified tab clicked.")
        else:
            # Render regular HTML response
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


class OfferCreateView(generic.CreateView):
    template_name = "offers/create_offer.html"
    form_class = OfferModelForm

    def form_valid(self, form: form_class) -> HttpResponse:
        offer_obj = form.save(commit=False)
        offer_obj.user = User.objects.first()
        offer_obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("offers:offer-list")


class WishlistItemCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "create_wishlist_item.html"
    form_class = WishlistItemModelForm

    # def get(self, request):
    #     if request.method == 'GET':
    #         form = self.form_class(initial={"product_name": "GET"})
    #     elif request.method == 'POST':
    #         form = self.form_class(initial={"product_name": "POST"})
    #     return render(request, self.template_name, {"form": form})

    def post(self, request):
        initial_prepop = {}
        product_name_prepop = request.POST.get('product_name_prepop')
        supermarket_prepop = request.POST.get('supermarket_prepop')
        
        if product_name_prepop:
            print("PRODUCT NAME PREPOP")
            initial_prepop["product_name"] = product_name_prepop
        if supermarket_prepop:
            initial_prepop["supermarkets"] = supermarket_prepop

        # print(initial_prepop)

        if initial_prepop:
            print("INITIAL PREPOP")
            form = self.form_class(initial=initial_prepop)
            # form.fields["supermarkets"].initial = "lidl"
            # print(dir(form.fields["supermarkets"]))
            # print(form.fields["supermarkets"].initial)
            # print(dir(form.fields["supermarket"].choices))
        else:
            form = self.form_class(request.POST)
            print("UPDATE")
            # form.fields["supermarkets"].initial = "maxima"

        data = request.POST.dict()
        sm = data.get("supermarkets")
        # print(sm)

        if form.is_valid():
            offer_obj = form.save(commit=False)
            offer_obj.user = self.request.user
            offer_obj.save()
            return redirect("wishlist")
        else:
            print("INVALID FORM!")
        
        return render(request, self.template_name, {"form": form})
        # if form.is_valid():
        #     form.save()
        # return redirect("main:home")

    # def get_initial(self):
    #     """
    #     Returns the initial data to use for forms on this view.
    #     """
    #     initial = super().get_initial()
    #     initial["product_name"] = "Product name test"
    #     return initial

    def form_valid(self, form: form_class) -> HttpResponse:
        offer_obj = form.save(commit=False)
        offer_obj.user = self.request.user
        offer_obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("wishlist")



class OfferUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "offers/update_offer.html"
    queryset = Offer.objects.all()
    context_object_name = "offer"
    form_class = OfferModelForm

    def get_success_url(self):
        offer_pk = self.get_object().pk
        return reverse("offers:offer-detail", kwargs={'pk': offer_pk})


class OfferDeleteView(generic.DeleteView):
    template_name = "offers/offer_delete.html"
    queryset = Offer.objects.all()

    def get_success_url(self):
        return reverse("offers:offer-list")


class WishlistItemUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "wishlist_item_update.html"
    queryset = WishlistItem.objects.all()
    context_object_name = "wishlist_item"
    form_class = WishlistItemModelForm

    def get_success_url(self):
        return reverse("wishlist")


class WishlistItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "wishlist_item_delete.html"
    queryset = WishlistItem.objects.all()
    context_object_name = "wishlist_item"

    def get_success_url(self):
        return reverse("wishlist")
