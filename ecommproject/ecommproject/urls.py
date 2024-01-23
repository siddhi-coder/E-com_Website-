"""
URL configuration for ecommproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecommapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),
    path("loginuser/", views.loginuser, name="loginuser"),
    path("registeruser/", views.registeruser, name="registeruser"),
    path("userlogout/", views.userlogout, name="userlogout"),
    path("aboutus/", views.aboutus, name="aboutus"),
    path("contactus/", views.contactus, name="contactus"),
    path("shoes_list_view/", views.shoes_list_view, name="shoes_list_view"),
    path("clothes_list_view/", views.clothes_list_view, name="clothes_list_view"),
    path("mobile_list_view/", views.mobile_list_view, name="mobile_list_view"),
    path("range_view/", views.range_view, name="range_view"),
    path("allsortorderview/", views.allsortorderview, name="allsortorderview"),
    path("searchproduct/", views.searchproduct, name="searchproduct"),
    path("cart/", views.cart, name="cart"),
    path('addtocart/<int:productid>/', views.addtocart, name='addtocart'),
    path("cart/removecart/<productid>", views.removecart, name="removecart"),
    path("cart/updateqty/<qv>/<productid>", views.updateqty, name="updateqty"),
    path("placeorder/", views.placeorder, name="placeorder"),
]+static(settings.MEDIA_URL , document_root  = settings.MEDIA_ROOT)
