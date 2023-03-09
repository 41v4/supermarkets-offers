from django.contrib import admin
from .models import User, Offer, Supermarket, WishlistItem


admin.site.register(User)
admin.site.register(Offer)
admin.site.register(Supermarket)
admin.site.register(WishlistItem)