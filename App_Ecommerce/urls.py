from django.urls import path
from . import views

app_name = 'App_Ecommerce'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path('checkout/', views.checkout, name='checkout'),
]


