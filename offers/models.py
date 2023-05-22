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
    product_brand = models.CharField(max_length=50, blank=True, null=True)
    product_descr = models.CharField(max_length=1000, blank=True, null=True)
    product_price = models.FloatField(blank=True, null=True)
    product_discount = models.IntegerField(blank=True, null=True)
    product_weight = models.IntegerField(blank=True, null=True)
    product_addt_info = models.CharField(max_length=1000, blank=True, null=True)
    product_img_orig = models.CharField(max_length=200, blank=True, null=True)
    product_img_local = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_method = models.CharField(max_length=10, choices=CREATED_METHOD_CHOICES, default=MAN)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_method = models.CharField(max_length=10, choices=CREATED_METHOD_CHOICES, default=MAN)
    deactivated_on = models.DateTimeField(blank=True, null=True)
    deactivated_method = models.CharField(max_length=10, choices=CREATED_METHOD_CHOICES, default=MAN)
    
    category = models.ForeignKey("Category", blank=True, null=True, on_delete=models.CASCADE)
    subcategory = models.ForeignKey("Subcategory", blank=True, null=True, on_delete=models.SET_NULL)
    supermarket = models.ForeignKey("Supermarket", on_delete=models.CASCADE)
    abst_product = models.ForeignKey("AbstProduct", blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_name}, {self.supermarket}, {self.created_on}"
    
class Category(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=False)
    url = models.CharField(max_length=100, unique=True)
    priority = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=100, unique=False)
    url = models.CharField(max_length=100, unique=True)
    priority = models.PositiveIntegerField()

    category = models.ForeignKey(Category, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class SubcategoryProductNames(models.Model):
    name = models.CharField(max_length=100)
    
    subcategory = models.ForeignKey(Subcategory, blank=False, null=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    class Meta:
        # Define the unique_together option
        unique_together = ('id', 'name')


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

    name = models.CharField(max_length=50, choices=supermarket_choices, unique=True, default="")
    website_url = models.CharField(max_length=100)
    descr = models.CharField(max_length=1000)

    def __str__(self):
        return self.name.capitalize()
    
class AbstProduct(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True) 

    def __str__(self):
        return self.product_name
    
class MultiOfferAbstProductMatch(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    abst_product = models.ForeignKey(AbstProduct, on_delete=models.CASCADE)
    sim_score_spacy = models.FloatField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.offer

class WishlistItem(models.Model):
    product_name = models.CharField(max_length=50)
    product_name_exact = models.BooleanField(default=False)
    product_brand = models.CharField(max_length=50, blank=True, null=True)
    product_brand_exact = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    valid_until = models.DateField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True) 
    supermarkets = models.ManyToManyField(Supermarket)
    notificators = models.ManyToManyField("Notificator")

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def beautify_supermarkets(self):
        if not self.supermarkets.exists():
            return "-"
        supermarkets_beautified = ", ".join([s.name.capitalize() for s in self.supermarkets.all()])
        return supermarkets_beautified

    def __str__(self):
        return self.product_name
    
class Notificator(models.Model):
    # choices for notificator
    EMAIL = "email"
    TELEGRAM = "telegram"
    notificator_choices = [
        (EMAIL, "Email"),
        (TELEGRAM, "Telegram")
    ]

    name = models.CharField(max_length=50, choices=notificator_choices, unique=True, default="")

    def __str__(self):
        return self.name

class MatchSession(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)


class WishlistOfferMatch(models.Model):
    match_session = models.ForeignKey(MatchSession, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wishlist_item = models.ForeignKey(WishlistItem, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist item: {self.wishlist_item} - Offer: {self.offer}"


class WishlistOfferMatchCombined(models.Model):
    match_session = models.ForeignKey(MatchSession, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match_session', 'user'], name='unique_match_user')
        ]


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.ForeignKey(Notificator, on_delete=models.CASCADE)
    match_user_id = models.ForeignKey(WishlistOfferMatchCombined, on_delete=models.CASCADE)
    sent_on = models.DateTimeField(blank=True, null=True)
    is_success = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.method.name}"
