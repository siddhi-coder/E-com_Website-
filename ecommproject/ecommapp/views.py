from django.shortcuts import render,redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from .models import Product , Cart , Order


def index(req):
    username = req.user.username
    allproducts = Product.objects.all()
    context = {"username":username , "allproducts":allproducts}
    return render(req, "index.html" ,context)


def loginuser(req):
    if req.method == "POST":  # Corrected method to lowercase "post"
        uname = req.POST.get("uname")
        passwd = req.POST.get("passwd")
        context = {}
        if not (uname and passwd):
            context['errormessage'] = "Fields can't be empty"
            return render(req, "loginuser.html", context)
        else:
            username = uname
            userdata = authenticate(username=uname, password=passwd)
            context = {"username" : username}
            if userdata is not None:
                login(req, userdata)
                return render(req,"index.html",context)
            else:
                context['errormessage'] = "Invalid username or password"
                return render(req, "loginuser.html", context)
    else:
        return render(req, "loginuser.html")


def registeruser(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        passwd = req.POST["passwd"]
        cpasswd = req.POST["cpasswd"]
        context = {}
        if uname == "" or passwd == "" or cpasswd == "":
            context['errormessage'] = "Field can't be empty"
            return render(req,"registeruser.html" , context)
        elif passwd != cpasswd :
            context['errormessage'] ="Password doesn't match"
            return render(req,"registeruser.html" , context)
        else:
            try:
                # Create the user if everything is fine
                userdata = User.objects.create(username=uname, password=passwd)
                userdata.set_password(passwd)
                userdata.save()
                return redirect("loginuser")
            except:
                context["errormessage"] = "User Already exists"
                return render(req, "registeruser.html" , context)
    else:
        return render(req, "registeruser.html")


def aboutus(req):
    return render(req, "aboutus.html")


def contactus(req):
    return render(req, "contactus.html")

def userlogout(req):
    logout(req)
    return redirect("/")

def mobile_list_view(req):
    if req.method == "GET":
        allproducts = Product.prod.mobile_list()
        context = {"allproducts":allproducts}
        return render(req,"index.html", context)
    else :
        allproducts = Product.objects.all()
        context = {"allproducts":allproducts}
        return render(req,"index.html", context)

def clothes_list_view(req):
    if req.method == "GET":
        allproducts = Product.prod.clothes_list()
        context = {"allproducts":allproducts}
        return render(req,"index.html", context)
    else :
        allproducts = Product.objects.all()
        context = {"allproducts":allproducts}
        return render(req,"index.html", context)

def shoes_list_view(req):
    if req.method == "GET":
        allproducts = Product.prod.shoes_list()
        context = {"allproducts":allproducts}
        return render(req,"index.html", context)
    else :
        allproducts = Product.objects.all()
        context = {"allproducts":allproducts}
        return render(req,"index.html", context)
