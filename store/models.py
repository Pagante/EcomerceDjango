from django.db import models
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from accounts.models import Account
from django.db.models import Avg,Count


# Create your models here.
class Category(MPTTModel):
    """
    Category Table implement with MPTT
    """
    name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"),
        max_length=255,
        unique=True
    )
    slug = models.SlugField(verbose_name=_("Category safe URL"),max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE,blank=True,null=True,related_name="children")
    image = models.ImageField(upload_to='photo/category/images', blank=True)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=255, blank=True)
    price = models.IntegerField()
    discount_price = models.IntegerField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to='photos/product/images')
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.product_name



    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status = True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])

        return avg

    def countReviews(self):
        reviews = ReviewRating.objects.filter(product=self, status = True).aggregate(count=Count('id'))
        if reviews['count'] is not None:
            count = float(reviews['count'])

        return count


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size',is_active=True)

VARIATION_CATEGORY_CHOICES = (
    ('color','color'),
    ('size', 'size'),
)
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=VARIATION_CATEGORY_CHOICES)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

# class ProductImage(models.Model):
#     """Product Image Table.
#     """
#     product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="product_image")
#     # image = models.ImageField(upload_to="photo/images/", verbose_name=_("Images"),default="images/default.png"),
#     image = models.ImageField(upload_to = "photo/Images", null=True)
#     alt_text = models.CharField(
#         verbose_name=_("Alternative text"),
#         help_text=_("Please add alternative text"),
#         max_length=255,
#         null=True,
#         blank=True,
#     )
#     is_feature = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True, editable=False)

#     class Meta:
#         verbose_name = _("Product Image")
#         verbose_name_plural = _("Product Images")