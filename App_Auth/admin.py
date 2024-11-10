from django.contrib import admin

# Register your models here.

from App_Auth import models

admin.site.register(models.User)
admin.site.register(models.CustomerProfile)