from django.shortcuts import render, get_object_or_404
from .models import Items, Category, Brand, Tag, AttributeTerm, ItemVariation, Order, Cart, CartItem
from .forms import CheckoutForm, AddToCartForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
# from .forms import OrderForm
import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect




def decimal_to_float(obj):
    """Helper function to convert Decimal to float for JSON serialization."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# Home Page
def home(request):
    items = Items.objects.filter(quantity__gt=0).order_by('-created')[:10]
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories,
    }
    return render(request, 'App_Ecommerce/home.html', context)

# def product_list(request):
#     items = Items.objects.filter(is_available=True)
#     return render(request, 'App_Ecommerce/product_list.html', {'items': items})

# Category View
def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = Items.objects.filter(Category=category)

    context = {
        'category': category,
        'items': items,
    }
    return render(request, 'App_Ecommerce/category_list.html', context)


# Product List View
def product_list(request):
    items = Items.objects.filter(quantity__gt=0)

    # Get filter parameters from the request
    selected_categories = request.GET.getlist('category')
    selected_brands = request.GET.getlist('brand')
    selected_tags = request.GET.getlist('tag')
    selected_colors = request.GET.getlist('color')
    selected_sizes = request.GET.getlist('size')
    selected_attributes = request.GET.getlist('attribute')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Apply filters based on request parameters
    if selected_categories:
        items = items.filter(Category__slug__in=selected_categories)
    if selected_brands:
        items = items.filter(Brand__slug__in=selected_brands)
    if selected_tags:
        items = items.filter(Tag__slug__in=selected_tags)
    if selected_attributes:
        items = items.filter(AttributeTerm__slug__in=selected_attributes)

        # Filter by color
    if selected_colors:
        # Filter items by the selected colors
        items = items.filter(ItemVariations__color__slug__in=selected_colors)

    # Filter by size
    if selected_sizes:
        items = items.filter(ItemVariations__size__slug__in=selected_sizes)

    if min_price:
        items = items.filter(selling_price__gte=min_price)
    if max_price:
        items = items.filter(selling_price__lte=max_price)

    # Pagination (12 items per page)
    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_items = paginator.get_page(page_number)

    # Get filter options for the form
    categories = Category.objects.all()
    brands = Brand.objects.all()
    tags = Tag.objects.all()
    attributes = AttributeTerm.objects.all()
    colors = AttributeTerm.objects.filter(Attribute__name__iexact="Color")
    sizes = AttributeTerm.objects.filter(Attribute__name__iexact="Size")

    context = {
        'items': page_items,
        'categories': categories,
        'brands': brands,
        'tags': tags,
        'attributes': attributes,
        'selected_categories': selected_categories,
        'selected_brands': selected_brands,
        'colors': colors,
        'sizes': sizes,
        'selected_colors': selected_colors,
        'selected_sizes': selected_sizes,
        'selected_tags': selected_tags,
        'selected_attributes': selected_attributes,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'App_Ecommerce/product_list.html', context)


def product_detail(request, slug):
    item = get_object_or_404(Items, slug=slug)
    # Grouping variations by color
    color_variations = {}
    for variation in item.ItemVariations.all():
        color_name = variation.color.name if variation.color else "N/A"
        if color_name not in color_variations:
            color_variations[color_name] = []
        color_variations[color_name].append({
            'size': variation.size.name if variation.size else "N/A",
            'quantity': variation.quantity,
        })
    
    context = {
        'item': item,
        'color_variations': color_variations,
    }
    return render(request, 'App_Ecommerce/product_details.html', context)

@login_required
def add_to_cart(request, item_id):
    if request.method == "POST":
        form = AddToCartForm(request.POST)
        if form.is_valid():
            # Extract data from form
            color_name = form.cleaned_data["color"]
            size_name = form.cleaned_data["size"]
            quantity = form.cleaned_data["quantity"]

            # Find the item variation
            item_variation = get_object_or_404(
                ItemVariation,
                Item__id=item_id,
                color__name=color_name,
                size__name=size_name,
            )

            # Get or create cart for the user
            cart, created = Cart.objects.get_or_create(user=request.user)

            # Add item to cart or update existing cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_variation=item_variation,
                defaults={"quantity": quantity},
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return redirect("App_Ecommerce:cart")

        else:
            return JsonResponse({"error": "Invalid form data"}, status=400)

    return redirect("App_Ecommerce:home")


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {"cart": cart}
    print(cart)
    return render(request, "App_Ecommerce/cart.html", context)

@csrf_protect
def checkout(request):
    # Fetch the cart associated with the logged-in user
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None  # Handle the case where the user doesn't have a cart yet

    if not cart or not cart.items.exists():
        return redirect('App_Ecommerce:cart')  # Redirect if no cart or cart is empty

    return render(request, 'App_Ecommerce/order.html', {'cart': cart})
@csrf_protect
def order(request):
    if request.method == 'POST':
        # Retrieve the user's cart
        cart = get_object_or_404(Cart, user=request.user)

        # Create the order
        order = Order.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            order_note=request.POST.get('order_note', ''),
            total_price=cart.total_price(),
        )

        # Add cart items to the order
        order.items.add(*cart.items.all())  # Use add() with unpacked querysets

        # Clear the cart
        # cart.items.set([])  # Correctly clear the many-to-many relation

        cart.total_price = 0  # Reset the cart's total price
        cart.save()

        return redirect('App_Ecommerce:order_success')  # Redirect to success page

    return redirect('App_Ecommerce:cart') 

def order_success(request):
    return render(request, 'App_Ecommerce/order_successful.html')

def order_failed(request):
    return render(request, 'App_Ecommerce/order_failure.html')