import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import constants as message_constants
from django.contrib.messages import get_messages
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string
from django.views import View, generic
from django_tables2 import RequestConfig, SingleTableView

from .forms import (CustomUserCreationForm, OfferModelForm,
                    WishlistItemModelForm)
from .models import (Category, Offer, Subcategory, Supermarket, User,
                     WishlistItem)
from .tables import ItemTable


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
    paginate_by = 2  # set the number of items per page
    
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
                    'html_from_offer_detail_view': render_to_string(html_template_name, {'offer': offer, 'request': request}),
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
    template_name = "wishlist_item_create.html"
    form_class = WishlistItemModelForm
    model = Offer

    def get_queryset(self):
        queryset = super().get_queryset()
        product_name = self.request.GET.get("product_name")
        product_brand = self.request.GET.get("product_brand")
        supermarkets = self.request.GET.getlist('selected_values')
        is_product_name_empty = not bool(product_name)  # check if product_name is empty or None
        is_supermarkets_empty = not bool(supermarkets) # check if supermarkets is empty or None

        self.custom_messsages = []
        if is_product_name_empty:
            messages.add_message(self.request, messages.WARNING, "Product name cannot be empty.")

        if is_supermarkets_empty:
            messages.add_message(self.request, messages.WARNING, "Supermarkets cannot be empty.")

        if any([is_product_name_empty, is_supermarkets_empty]):
            print("Returning NONE")
            return None  # returning None will not render the template and instead trigger the else block of the get() method
        
        if product_name and supermarkets and not product_brand:
            queryset = queryset.filter(
                product_name__istartswith=product_name,
                supermarket_id__in=[int(i) for i in supermarkets]
            )
        # elif product_name and supermarkets and product_brand: # Implement later
        #     queryset = queryset.filter(
        #         product_name__istartswith=product_name,
        #         product_brand__istartswith=product_brand,
        #         supermarket_id__in=[int(i) for i in supermarkets]
        #     )
        
        return queryset

    def get(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            queryset = self.get_queryset()
            if queryset:
                html_template_name = "wishlist_tbody.html"
                return JsonResponse({
                    'html_from_wishlist_item_create_view': render_to_string(html_template_name, {'offers': queryset}),
                })
            else:
                html_template_name = "wishlist_item_errors.html"
                msgs_storage = get_messages(request)
                warning_msg_exist = False
                for msg in msgs_storage:
                    if msg.level == message_constants.WARNING:
                        warning_msg_exist = True
                if not warning_msg_exist:
                    messages.add_message(request, messages.INFO, "No results. Try changing product name and/or supermarket(s).")
                    msgs_storage = get_messages(request)
                return JsonResponse({
                    'custom_msgs': render_to_string(html_template_name, {'messages': msgs_storage}),
                })

        initial_prepop = {}
        product_name_prepop = request.GET.get('product_name_prepop')
        supermarket_prepop = request.GET.get('supermarket_prepop')

        if product_name_prepop:
            initial_prepop["product_name"] = product_name_prepop

        if supermarket_prepop:
            initial_prepop["supermarkets"] = supermarket_prepop

        form = self.form_class(initial=initial_prepop or request.GET)

        if request.method == 'POST' and form.is_valid():
            offer_obj = form.save(commit=False)
            offer_obj.user = self.request.user
            offer_obj.save()
            form.save_m2m()
            return redirect("wishlist")

        return render(request, self.template_name, {"form": form})

    def post(self, request):
        initial_prepop = {}
        product_name_prepop = request.POST.get('product_name_prepop')
        supermarket_prepop = request.POST.get('supermarket_prepop')

        if product_name_prepop:
            initial_prepop["product_name"] = product_name_prepop
        if supermarket_prepop:
            initial_prepop["supermarkets"] = supermarket_prepop

        if initial_prepop:
            form = self.form_class(initial=initial_prepop)
        else:
            form = self.form_class(request.POST)

        if form.is_valid():
            offer_obj = form.save(commit=False)
            offer_obj.user = self.request.user
            offer_obj.save()
            form.save_m2m()  # save many-to-many relationship
            return redirect("wishlist")
        else:
            print("INVALID FORM!")

        return render(request, self.template_name, {"form": form})

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
        messages.success(self.request, "Offer updated successfully")
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

    def get_initial(self):
        initial = super().get_initial()
        # Get the WishlistItem instance being edited
        wishlist_item = self.get_object()
        # Get the IDs of the supermarkets associated with the WishlistItem
        supermarket_ids = wishlist_item.supermarkets.values_list('id', flat=True)
        # Set the initial value of the supermarkets field to the list of IDs
        initial['supermarkets'] = supermarket_ids
        return initial

    def get_queryset(self, is_ajax=False):
        if is_ajax:
            queryset = Offer.objects.all()
            product_name = self.request.GET.get("product_name")
            product_brand = self.request.GET.get("product_brand")
            supermarkets = self.request.GET.getlist('selected_values')
            is_product_name_empty = not bool(product_name)  # check if product_name is empty or None
            is_supermarkets_empty = not bool(supermarkets) # check if supermarkets is empty or None

            self.custom_messsages = []
            if is_product_name_empty:
                messages.add_message(self.request, messages.WARNING, "Product name cannot be empty.")

            if is_supermarkets_empty:
                messages.add_message(self.request, messages.WARNING, "Supermarkets cannot be empty.")

            if any([is_product_name_empty, is_supermarkets_empty]):
                print("RETURNING NONE")
                return None  # returning None will not render the template and instead trigger the else block of the get() method
            
            if product_name and supermarkets and not product_brand:
                print("FILTERING!!!")
                queryset = queryset.filter(
                    product_name__istartswith=product_name,
                    supermarket_id__in=[int(i) for i in supermarkets]
                )
            # elif product_name and supermarkets and product_brand: # Implement later
            #     queryset = queryset.filter(
            #         product_name__istartswith=product_name,
            #         product_brand__istartswith=product_brand,
            #         supermarket_id__in=[int(i) for i in supermarkets]
            #     )
            return queryset
        
        queryset = super().get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            queryset = self.get_queryset(is_ajax=True)
            if queryset:
                html_template_name = "wishlist_tbody.html"
                return JsonResponse({
                    'html_from_wishlist_item_create_view': render_to_string(html_template_name, {'offers': queryset}),
                })
            else:
                html_template_name = "wishlist_item_errors.html"
                msgs_storage = get_messages(request)
                warning_msg_exist = False
                for msg in msgs_storage:
                    if msg.level == message_constants.WARNING:
                        warning_msg_exist = True
                if not warning_msg_exist:
                    messages.add_message(request, messages.INFO, "No results. Try changing product name and/or supermarket(s).")
                    msgs_storage = get_messages(request)
                return JsonResponse({
                    'custom_msgs': render_to_string(html_template_name, {'messages': msgs_storage}),
                })
        else:
            # Render regular HTML response
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

    def get_success_url(self):
        return reverse("wishlist")


class WishlistItemDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "wishlist_item_delete.html"
    queryset = WishlistItem.objects.all()
    context_object_name = "wishlist_item"

    def get_success_url(self):
        return reverse("wishlist")


class SubcategoryAPIView(View):
    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
                subcategories = category.subcategory_set.all()
                data = {
                    'subcategories': [
                        {'id': subcategory.id, 'name': subcategory.name}
                        for subcategory in subcategories
                    ]
                }
                return JsonResponse(data)
            except Category.DoesNotExist:
                pass
        return JsonResponse({'subcategories': []})
    

class ItemListView(SingleTableView):
    table_class = ItemTable
    # queryset = Offer.objects.all()
    queryset = Offer.objects.all().order_by('created_on')
    template_name = "offers/table_main.html"
    paginate_by = 50

    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        category_choices = [(category.id, category.name) for category in Category.objects.all()]
        subcategory_choices = [(subcategory.id, subcategory.name, subcategory.category) for subcategory in Subcategory.objects.all()]
        table.category_choices = category_choices
        table.subcategory_choices = subcategory_choices
        return table


class SaveCategoriesAPIView(View):
    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        if json_data:
            for item in json_data:
                try:
                    object_id = item.get("offerId")
                    category_id = item.get("categoryId")
                    subcategory_id = item.get("subcategoryId")

                    # Retrieve the Offer object based on its ID
                    offer_obj = get_object_or_404(Offer, id=object_id)

                    # Update the Offer object using the additional data
                    if category_id:
                        category_obj = get_object_or_404(Category, id=category_id)
                        offer_obj.category = category_obj
                    else:
                        offer_obj.category = None

                    if subcategory_id:
                        subcategory_obj = get_object_or_404(Subcategory, id=subcategory_id)
                        offer_obj.subcategory = subcategory_obj
                    else:
                        offer_obj.subcategory = None

                    offer_obj.save()

                except (Offer.DoesNotExist, Category.DoesNotExist, Subcategory.DoesNotExist) as e:
                    return JsonResponse({'error': str(e)}, status=400)

            return JsonResponse({'message': 'Objects updated successfully'})

        return JsonResponse({'error': 'No JSON data was received.'}, status=400)
    
    def get_success_url(self):
        messages.success(self.request, "Categories updated successfully")
        return reverse("offers:categories")