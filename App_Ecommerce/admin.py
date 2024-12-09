from django.contrib import admin
from App_Ecommerce import models
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']

    def items_display(self, obj):
        return ", ".join([f"{item.item_variation.Item.title} (Qty: {item.quantity})" for item in obj.items.all()])
    items_display.short_description = "Ordered Items"

admin.site.register(models.Attribute)
admin.site.register(models.AttributeTerm)
admin.site.register(models.Category)
admin.site.register(models.Brand)
admin.site.register(models.Tag)
admin.site.register(models.Items) 
admin.site.register(models.ItemImage) 
admin.site.register(models.ItemVariation)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Order, OrderAdmin)


