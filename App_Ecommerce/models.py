from django.db import models
from django.db.models import JSONField
import uuid
import os
from django.utils.text import slugify
from Core import settings
from App_Auth.models import CustomerProfile

# FUNCTIONS 
def item_image_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("uploads/items/", filename)

# Attributes
class Attribute(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
    
#  Attributes Term
class AttributeTerm(models.Model):
    Attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name 
    
#  Category
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    is_addons = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    data = JSONField(null=True, blank=True)
    Category_parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name 
    
# Brand
class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name    

class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, null=True, blank=True) 
    created = models.DateTimeField(auto_now_add=True)
    Tag_parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name 
    
class Items(models.Model):
    AttributeTerm = models.ManyToManyField(AttributeTerm, blank=True, related_name="Attribute_Term", related_query_name="Attribute_Term",)
    Category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="Item_Category", related_query_name="Item_Category")
    Sub_Category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="Product_Sub_Category", related_query_name="Product_Sub_Category")
    Brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name="Brand", related_query_name="Brand")
    Tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True, related_name="Tag", related_query_name="Tag")
    related_Items = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    sku = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, unique=True, null=True, blank=True) 
    barcode = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    product_details = models.TextField(null=True, blank=True)
    purchase_price = models.DecimalField(default=0, blank=True, max_digits=20, decimal_places=2)
    selling_price = models.DecimalField(default=0, blank=True, max_digits=20, decimal_places=2)
    discount_price = models.DecimalField(default=0, blank=True, max_digits=20, decimal_places=2)
    quantity = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    Location = models.CharField(max_length=255, null=True, blank=True)
    action_details = models.CharField(max_length=255, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.Category} | {self.title} " 
    
    def save(self, *args, **kwargs):
        # Generate a 12-digit barcode: 100000 + item ID
        if not self.barcode:
            super().save(*args, **kwargs)  # Save first to generate the ID
            self.barcode = f"{100000 + self.id:012d}"
            
        if not self.slug:
            self.slug = slugify(self.title) 
        super().save(*args, **kwargs)
    
class ItemVariation(models.Model):
    Item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="ItemVariations", related_query_name="ItemVariations")
    # AttributeTerm = models.ManyToManyField(AttributeTerm, blank=True, related_name="AttributeVariation", related_query_name="AttributeVariation")
    Location = models.CharField(max_length=255, null=True, blank=True)
    Supplier = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    purchase_price = models.DecimalField(default=0, blank=True, max_digits=20, decimal_places=2)
    selling_price = models.DecimalField(default=0, blank=True, max_digits=20, decimal_places=2)
    discount_price = models.DecimalField(default=0, blank=True, max_digits=20, decimal_places=2)
    quantity = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    action_details = models.CharField(max_length=255, null=True, blank=True)
    color = models.ForeignKey(AttributeTerm, on_delete=models.SET_NULL, null=True, blank=True, related_name="color_variations")
    size = models.ForeignKey(AttributeTerm, on_delete=models.SET_NULL, null=True, blank=True, related_name="size_variations")
    product_details = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.Item.title} - {self.color.name if self.color else 'No Color'} - {self.size.name if self.size else 'No Size'}"


    def save(self, *args, **kwargs):
        # Auto-generate barcode if not provided
        if not self.barcode:
            color_name = self.color.name if self.color else "NoColor"
            size_name = self.size.name if self.size else "NoSize"
            self.barcode = f"{self.Item.id}-{color_name}-{size_name}".upper()

        super().save(*args, **kwargs)
    
class ItemImage(models.Model):
    photo = models.ImageField(null=True, upload_to=item_image_file_path)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    Item = models.ForeignKey('Items', on_delete=models.CASCADE, null=True, blank=True)
    ItemVariation = models.ForeignKey('ItemVariation', on_delete=models.CASCADE, null=True, blank=True)
    AttributeTerm = models.ForeignKey('AttributeTerm', on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def __str__(self):
        return self.Item 
    

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    item_variation = models.ForeignKey(ItemVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"