from django.db import models
from django.contrib.auth.models import User

class CustomManager(models.Manager):
    #method
    def mobile_list(self):
        return self.filter(category__exact ="Mobile")
    def clothes_list(self):
        return self.filter(category__exact ="Clothes")
    def shoes_list(self):
        return self.filter(category__exact ="Shoes")
        
class Product(models.Model):
    userid = models.ForeignKey(User , on_delete = models.CASCADE , null = True , blank = True)
    productid = models.IntegerField(primary_key = True)
    product_name = models.CharField(max_length = 55)
    type = (("Mobile","Mobile"),("Clothes", "Clothes"),("Shoes","Shoes"))
    category = models.CharField(max_length = 50 ,choices = type , default = "")
    description = models.TextField(max_length = 100)
    price = models.FloatField()
    image=models.ImageField(upload_to='product/')
    objects = models.Manager()
    prod = CustomManager()

class Cart(models.Model):
    userid = models.ForeignKey(User , on_delete = models.CASCADE , null = True , blank = True)
    productid = models.ForeignKey(Product,on_delete = models.CASCADE , null = True , blank = True)
    quantity = models.PositiveIntegerField(default = 0)


class Order(models.Model):
    userid = models.ForeignKey(User , on_delete = models.CASCADE , null = True , blank = True)
    productid = models.ForeignKey(Product,on_delete = models.CASCADE , null = True , blank = True)
    orderid = models.IntegerField(primary_key = True)
    quantity = models.PositiveIntegerField(default = 0)
    status = (("Pending" , "Pending") , ("Out for Delivery","Out for Delivery") , ("Deliverd" , "Deliverd"))


