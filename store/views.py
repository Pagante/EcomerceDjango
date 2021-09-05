from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from carts.models import Cart, CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.


def home(request):
    products = Product.objects.all().filter(is_available=True)
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {
        'products': paged_products, 
    }
    return render(request, 'store/index.html', context)



def store(request):
    products = Product.objects.all().filter(is_available=True).order_by('id')
    paginator = Paginator(products, 8)
    product_count = products.count()
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    
    context = {
        'product': product,
        'in_cart': in_cart,
    }
    return render(request, 'store/single.html', context)


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    
    products = Product.objects.filter(category__in=category.get_descendants(include_self=True))
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    context = {
        'category': category,
        'products':paged_products,
    }
    return render(request, 'store/category.html', context)


def search(request,products=None):
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        
        product_count=0
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword)|Q(product_name__icontains=keyword))
            product_count = products.count()
        
    context = {
        'products':products,
        'product_count':product_count
    }
    return render(request,'store/store.html', context)