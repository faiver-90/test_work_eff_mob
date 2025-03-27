from django.contrib import admin

# Register your models here.
from orders.models import Items, Order

admin.site.register(Order)
admin.site.register(Items)
