from django.contrib import admin
from .models import Cart , Order , Product

# Register your models here.
class AdminProduct (admin.ModelAdmin):
    list_display = (
        "userid" , 
        "productid",
        "product_name",
        "category" , 
        "description",
        "price",
        "image",
    )


class AdminCart (admin.ModelAdmin):
    list_display = (
        "userid" , 
        "productid",
        "quantity",
    )

class AdminOrder (admin.ModelAdmin):
    list_display = (
        "userid" , 
        "productid",
        "orderid",
        "quantity",
        "status",
        "receipt",
    )

admin.site.register(Product,AdminProduct)
admin.site.register(Cart,AdminCart)
admin.site.register(Order,AdminOrder)