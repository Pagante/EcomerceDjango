from django.urls import path
from .import views

app_name='store'

urlpatterns = [
    path('', views.home, name='home' ),
    path('category/<slug:category_slug>/', views.category_list, name='category_list'),
    path('store/', views.store, name='store'),
    path('category/<slug:slug>', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]
