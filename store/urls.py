from django.urls import path
from .import views

app_name='store'

urlpatterns = [
    path('', views.home, name='home' ),
    path('Shop/<slug:category_slug>/', views.category_list, name='category_list'),
    path('store/', views.store, name='store'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
]
