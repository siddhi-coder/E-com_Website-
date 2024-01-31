from django import forms
from django.contrib.auth.models import User
from .models import Product

class ViewProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = [ 'product_name', 'category', 'description', 'price', 'image']

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)  
    #     super(ViewProduct, self).__init__(*args, **kwargs)

    #     if user:
    #         self.fields['userid'].initial = user.id
    #         self.fields['userid'].queryset = User.objects.filter(pk=user.id)

