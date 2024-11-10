from django.shortcuts import render, get_object_or_404
from .models import Items, Category, Brand, Tag, AttributeTerm, ItemVariation
from django.core.paginator import Paginator

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
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    tag = request.GET.get('tag')

    if category:
        items = items.filter(Category__slug=category)
    if brand:
        items = items.filter(Brand__slug=brand)
    if tag:
        items = items.filter(Tag__slug=tag)

    paginator = Paginator(items, 12)  # Paginate with 12 items per page
    page_number = request.GET.get('page')
    page_items = paginator.get_page(page_number)

    context = {
        'items': page_items,
        'category': category,
        'brand': brand,
        'tag': tag,
    }
    return render(request, 'App_Ecommerce/product_list.html', context)

# Product Detail View
def product_detail(request, slug):
    item = get_object_or_404(Items, slug=slug)
    variations = ItemVariation.objects.filter(Item=item)
    related_items = Items.objects.filter(Category=item.Category).exclude(id=item.id)[:4]

    context = {
        'item': item,
        'variations': variations,
        'related_items': related_items,
    }
    return render(request, 'App_Ecommerce/product_details.html', context)

# Category View
def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = Items.objects.filter(Category=category)

    context = {
        'category': category,
        'items': items,
    }
    return render(request, 'App_Ecommerce/category_list.html', context)