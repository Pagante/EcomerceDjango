from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Category, Product, ReviewRating, ProductGallery
from carts.models import Cart, CartItem
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct, Order
from accounts.models import UserProfile


# Create your views here.


def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('id')
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product__id=product.id, status=True)
    
    context = {
        'products': paged_products, 
        'reviews': reviews
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
    try:
        userprofile = UserProfile.objects.get(user_id = request.user.id)
        product = get_object_or_404(Product, slug=slug, is_available=True)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
        
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
        
    #Get Review
    reviews = ReviewRating.objects.filter(product__id=product.id, status=True)

    #Get Product Gallery
    product_gallery = ProductGallery.objects.filter(product_id = product.id)
    context = {
        'product': product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'userprofile': userprofile,
        'product_gallery': product_gallery,
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



def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


