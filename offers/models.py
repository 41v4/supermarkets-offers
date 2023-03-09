from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Offer(models.Model):
    # choices for created_method
    AUTO = "auto"
    MAN = "man"
    CREATED_METHOD_CHOICES = [
        (AUTO, "automated"),
        (MAN, "manual")
    ]

    product_name = models.CharField(max_length=50)
    product_descr = models.CharField(max_length=200)
    product_price = models.FloatField(blank=True, null=True)
    product_discount = models.IntegerField(blank=True, null=True)
    product_weight = models.IntegerField(blank=True, null=True)
    product_addt_info = models.CharField(max_length=200, blank=True, null=True)
    product_img_orig = models.CharField(max_length=200, blank=True, null=True)
    product_img_local = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    valid_until = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_method = models.CharField(max_length=10, choices=CREATED_METHOD_CHOICES, default=MAN)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_method = models.CharField(max_length=10, choices=CREATED_METHOD_CHOICES, default=MAN)
    deactivated_on = models.DateTimeField(blank=True, null=True)
    deactivated_method = models.CharField(max_length=10, choices=CREATED_METHOD_CHOICES, default=MAN)
    
    supermarket = models.ForeignKey("Supermarket", on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_name}, {self.supermarket}, {self.created_on}"


class Supermarket(models.Model):
    # choices for supermarket
    MAXIMA = "maxima"
    IKI = "iki"
    LIDL = "lidl"
    NORFA = "norfa"
    RIMI = "rimi"
    supermarket_choices = [
        (MAXIMA, "Maxima"),
        (IKI, "Iki"),
        (LIDL, "Lidl"),
        (NORFA, "Norfa"),
        (RIMI, "Rimi")
    ]

    name = models.CharField(max_length=50, choices=supermarket_choices, default="")
    website_url = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WishlistItem(models.Model):
    product_name = models.CharField(max_length=50)
    product_name_exact = models.BooleanField(default=False)
    product_brand = models.CharField(max_length=50, blank=True, null=True)
    product_brand_exact = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    valid_until = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True) 
    supermarkets = models.CharField(max_length=50, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def beautify_supermarkets(self):
        if not self.supermarkets:
            return "-"
        supermarkets_list = self.supermarkets.strip('[]').replace("'", "").split(',')
        supermarkets_beautified = ", ".join([i.strip().capitalize() for i in supermarkets_list])
        return supermarkets_beautified

    def __str__(self):
        return self.product_name
