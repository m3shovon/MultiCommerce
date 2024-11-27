from django.shortcuts import render, get_object_or_404
from .models import Items, Category, Brand, Tag, AttributeTerm, ItemVariation
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

# Home Page
def home(request):
    items = Items.objects.filter(quantity__gt=0).order_by('-created')[:10]
    categories = Category.objects.all()
    context = {
        'items': items,
        'categories': categories,
    }
    return render(request, 'App_Ecommerce/home.html', context)

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

# Product Detail View
def product_detail(request, slug):
    # Fetch the item based on the slug
    item = get_object_or_404(Items, slug=slug)

    # Fetch all variations for this item
    variations = ItemVariation.objects.filter(Item=item, is_available=True)

    # Group variations by color
    color_variations = {}
    for variation in variations:
        color_name = variation.color.name if variation.color else "No Color"
        size_name = variation.size.name if variation.size else "No Size"
        
        if color_name not in color_variations:
            color_variations[color_name] = {
                "color_id": variation.color.id if variation.color else None,
                "sizes": []
            }

        color_variations[color_name]["sizes"].append({
            "size_name": size_name,
            "size_id": variation.size.id if variation.size else None,
            "barcode": variation.barcode,
            "purchase_price": variation.purchase_price,
            "selling_price": variation.selling_price,
            "discount_price": variation.discount_price,
            "quantity": variation.quantity,
            "is_available": variation.is_available,
        })

    context = {
        "item": item,
        "color_variations": color_variations,
    }

    return render(request, "App_Ecommerce/product_details.html", context)

# Category View
def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = Items.objects.filter(Category=category)

    context = {
        'category': category,
        'items': items,
    }
    return render(request, 'App_Ecommerce/category_list.html', context)




def checkout(request):
    # if request.method == "POST":
    #     color_id = request.POST.get('color_id')
    #     size_id = request.POST.get('size_id')
    #     quantity = int(request.POST.get('quantity', 1))

    #     # Logic for saving order details and handling checkout

    #     # Redirect to checkout page
    #     return JsonResponse({"checkout_url": reverse('App_Ecommerce:checkout')})
    # return redirect("App_Ecommerce:product_list")
    return render(request, 'App_Ecommerce/checkout.html')