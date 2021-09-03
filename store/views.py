from django.shortcuts import render, get_object_or_404
from .models import Category, Product

# Create your views here.


def home(request):
    products = Product.objects.all().filter(is_available=True)
    
    context = {
        'products': products,
    }
    return render(request, 'store/index.html', context)



def store(request):
    products = Product.objects.all().filter(is_available=True)
    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    context = {
        'product': product,
    }
    return render(request, 'store/single.html', context)


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category__in=category.get_descendants(include_self=True))

    context = {
        'category': category,
        'products':products,
    }
    return render(request, 'store/category.html', context)