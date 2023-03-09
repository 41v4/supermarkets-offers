from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetCompleteView
)
from django.urls import include, path
from offers.views import (HomePageView, WishlistItemCreateView,
                          WishlistItemDeleteView, WishlistItemDetail,
                          WishlistItemUpdateView, WishlistView, SingupView, ContactView, WishlistMultiActionView)

urlpatterns = [
    path('', HomePageView.as_view(), name="homepage"),
    path('admin/', admin.site.urls),
    path('offers/', include('offers.urls', namespace="offers")),
    path('wishlist/', WishlistView.as_view(), name="wishlist"),
    path('wishlist-multi-action/', WishlistMultiActionView.as_view(), name="wishlist-multi-action"),
    path('wishlist/create/', WishlistItemCreateView.as_view(), name="wishlist-create"),
    path('wishlist/<int:pk>/', WishlistItemDetail.as_view(), name="wishlist-item-detail"),
    path('wishlist/<int:pk>/update/', WishlistItemUpdateView.as_view(), name="wishlist-item-update"),
    path('wishlist/<int:pk>/delete/', WishlistItemDeleteView.as_view(), name="wishlist-item-delete"),
    path('signup/', SingupView.as_view(), name='signup'),
    path('reset-password', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('contact-us/', ContactView.as_view(), name='contact')
]

# urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)