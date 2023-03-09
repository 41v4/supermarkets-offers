from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Supermarket, Offer, WishlistItem

User = get_user_model()


class OfferModelForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = (
            'product_name',
            'product_price',
            'product_discount',
            'product_addt_info',
            'product_img_orig',
            'supermarket'
        )


class DateInput(forms.DateInput):
    input_type = "date"


class WishlistItemModelForm(forms.ModelForm):
    supermarket_choices = [(obj.name, obj.get_name_display()) for obj in Supermarket.objects.all()]
    supermarkets = forms.MultipleChoiceField(choices=supermarket_choices, required=False, widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = WishlistItem
        fields = (
            'product_name',
            'product_name_exact',
            'product_brand',
            'product_brand_exact',
            'is_active',
            'valid_until',
            'supermarkets'
        )
        widgets = {
            'valid_until': DateInput()
        }


class OfferForm(forms.Form):
    supermarkets = [(obj.name, obj.get_name_display()) for obj in Supermarket.objects.all()]
    product_name = forms.CharField()
    product_price = forms.FloatField(required=False)
    product_discount = forms.IntegerField(required=False)
    product_addt_info = forms.CharField(required=False)
    product_img_orig = forms.CharField(required=False)
    supermarket = forms.MultipleChoiceField(choices=supermarkets, widget=forms.CheckboxSelectMultiple())


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username",)
        field_classes = {"username": UsernameField}