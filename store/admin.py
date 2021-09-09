from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, Variation


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
# class ProductImageInline(admin.TabularInline):
#     model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'slug', 'stock', 'price']
    prepopulated_fields = {'slug':('product_name',)}

