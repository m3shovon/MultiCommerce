from django.contrib import admin
from App_Ecommerce import models
# Register your models here.

admin.site.register(models.Attribute)
admin.site.register(models.AttributeTerm)
admin.site.register(models.Category)
admin.site.register(models.Brand)
admin.site.register(models.Tag)
admin.site.register(models.Items) 
admin.site.register(models.ItemImage) 
admin.site.register(models.ItemVariation)
admin.site.register(models.Services)


