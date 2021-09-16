from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import (
    Category, 
    Product, 
    Variation, 
    ReviewRating, 
    ProductGallery
)
import admin_thumbnails


# Register your models here.

admin.site.register (
    Category,
    MPTTModelAdmin,
    prepopulated_fields = {
        'slug': ('name',)
    }
)


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'variation_value', 'variation_category','is_active']
    list_editable = ['is_active',]
    list_filter = ['product', 'variation_value', 'variation_category','is_active']


admin.site.register(ProductGallery)
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'slug', 'stock', 'price']
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [ProductGalleryInline,]


admin.site.register(ReviewRating)


