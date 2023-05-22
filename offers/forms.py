from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Supermarket, Offer, WishlistItem, Category, Subcategory

User = get_user_model()


class DateInput(forms.DateInput):
    input_type = "date"


class OfferModelForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.none())

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
            'category',
            'subcategory',
            'supermarket'
        )
        widgets = {
            'valid_until': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.all()

        self.fields['category'].widget.attrs['onchange'] = 'load_subcategories(this.value);'

    class Media:
        js = ('js/subcategories.js',)  # Replace with the actual path to your JavaScript file


class WishlistItemModelForm(forms.ModelForm):
    supermarkets = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        error_messages={'required': 'Please select at least one supermarket.'}
    )

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supermarkets'].choices = [
            (obj.id, obj.get_name_display()) for obj in Supermarket.objects.all()
        ]


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username",)
        field_classes = {"username": UsernameField}