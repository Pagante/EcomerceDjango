from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, ProductImage


# Register your models here.

admin.site.register (
    Category,
    MPTTModelAdmin,
    prepopulated_fields = {
        'slug': ('name',)
    }
)

class ProductImageInline(admin.TabularInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline
    ]
    prepopulated_fields = {'slug':('product_name',)}
    list_display = ['product_name',]

