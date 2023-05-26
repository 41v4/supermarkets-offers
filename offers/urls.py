from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from .views import (OfferCreateView, OfferDeleteView, OfferDetailView,
                    OfferListView, OfferUpdateView, SubcategoryAPIView, ItemListView, SaveCategoriesAPIView)

app_name = "offers"

urlpatterns = [
   path('', OfferListView.as_view(), name="offer-list") ,
   path('<int:pk>/', OfferDetailView.as_view(), name="offer-detail"),
   path('<int:pk>/update/', staff_member_required(OfferUpdateView.as_view()), name="offer-update"),
   path('<int:pk>/delete/', staff_member_required(OfferDeleteView.as_view()), name="offer-delete"),
   path('create/', staff_member_required(OfferCreateView.as_view()), name="offer-create"),
   path('get_subcategories/', SubcategoryAPIView.as_view(), name='get_subcategories'),
   path('categories/', staff_member_required(ItemListView.as_view()), name='categories'),
   path('save_categories/', staff_member_required(SaveCategoriesAPIView.as_view()), name='save-categories'),
]
