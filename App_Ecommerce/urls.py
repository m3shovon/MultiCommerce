from django.urls import path
from . import views

app_name = 'App_Ecommerce'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_list, name='category_list'),
    path("add-to-cart/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path('cart/', views.cart, name='cart'),
    # path('remove-from-cart/<int:variation_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/', views.order, name='order'),
    path('order-successful/', views.order_success, name='order_success'), 
    path('order-failure/', views.order_failed, name='order_failed'), 

]


