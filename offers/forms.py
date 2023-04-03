from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Supermarket, Offer, WishlistItem

User = get_user_model()


class DateInput(forms.DateInput):
    input_type = "date"


class OfferModelForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = (
            'is_active',
            'valid_until',
            'product_name',
            'product_price',
            'product_discount',
            'product_descr',
            'product_addt_info',
            'product_img_orig',
            'product_img_local',
            'supermarket'
        )
        widgets = {
            'valid_until': DateInput()
        }


class WishlistItemModelForm(forms.ModelForm):
    supermarket_choices = [(obj.id, obj.get_name_display()) for obj in Supermarket.objects.all()]
    supermarkets = forms.MultipleChoiceField(choices=supermarket_choices, widget=forms.CheckboxSelectMultiple(), error_messages={'required': 'Please select at least one supermarket.'})

    class Meta:
        model = WishlistItem
        fields = (
            'is_active',
            'product_name',
            'product_name_exact',
            'product_brand',
            'product_brand_exact',
            'valid_until',
            'supermarkets'
        )
        widgets = {
            'valid_until': DateInput(),
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