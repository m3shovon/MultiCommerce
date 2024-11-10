from django.db import models
from django.db.models import JSONField
import uuid
import os

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
    purchase_price = models.DecimalField(default=0, blank=True, max_digits=20, decimal_places=2)
    selling_price = models.DecimalField(default=0, blank=True, max_digits=20, decimal_places=2)
    discount_price = models.DecimalField(default=0, blank=True, max_digits=20, decimal_places=2)
    quantity = models.IntegerField(default=0)
    discount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    Location = models.CharField(max_length=255, null=True, blank=True)
    action_details = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title 
    
    def save(self, *args, **kwargs):
        # Generate a 12-digit barcode: 100000 + item ID
        if not self.barcode:
            super().save(*args, **kwargs)  # Save first to generate the ID
            self.barcode = f"{100000 + self.id:012d}"
        super().save(*args, **kwargs)
    
class ItemVariation(models.Model):
    Item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="ItemVariations", related_query_name="ItemVariations")
    AttributeTerm = models.ManyToManyField(AttributeTerm, blank=True, related_name="AttributeVariation", related_query_name="AttributeVariation")
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
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.Item) if self.Item else "No Item Assigned"

    def save(self, *args, **kwargs):
        # Generate a 12-digit barcode for ItemVariation
        if not self.barcode:
            super().save(*args, **kwargs)  # Save first to generate the ID
            item_id_part = f"{100000 + self.Item.id:06d}"

            # Fetch up to 2 AttributeTerm IDs and use them for barcode generation
            attribute_ids = list(self.AttributeTerm.values_list('id', flat=True)[:2])
            if len(attribute_ids) < 2:
                attribute_ids.extend([0] * (2 - len(attribute_ids)))  # Pad with zeros if less than 2

            attribute_part = f"{attribute_ids[0]:03d}{attribute_ids[1]:03d}"
            self.barcode = f"{item_id_part}{attribute_part}"
        
        super().save(*args, **kwargs)
    
class ItemImage(models.Model):
    photo = models.ImageField(null=True, upload_to=item_image_file_path)
    is_active = models.BooleanField(default=True, null=True, blank=True)
    Item = models.ForeignKey('Items', on_delete=models.CASCADE, null=True, blank=True)
    ItemVariation = models.ForeignKey('ItemVariation', on_delete=models.CASCADE, null=True, blank=True)
    AttributeTerm = models.ForeignKey('AttributeTerm', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.Item 
    
class Services(models.Model):
    Item = models.ForeignKey('Items', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.CharField(max_length=255, unique=True, null=True, blank=True) 
    costing = models.DecimalField(default=0, blank=True, max_digits=20, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    
    
