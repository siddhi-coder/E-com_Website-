from datetime import timezone
import random
import uuid
from django.shortcuts import render,redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from .models import Product , Cart , Order
from django.db.models import Q
import razorpay
from ecommapp.forms import ViewProduct


def index(req):
    username = req.user.username
    allproducts = Product.objects.all()
    context = {"username":username , "allproducts":allproducts}
    return render(req, "index.html" ,context)


def loginuser(req):
    if req.method == "POST":  # Corrected method to lowercase "post"
        uname = req.POST.get("uname")
        passwd = req.POST.get("passwd")
        allproducts = Product.objects.all()
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
                # return render(req,"index.html",context)
                return redirect("/")
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
    username = req.user.username
    context = {"username":username }
    return render(req, "aboutus.html",context)


def contactus(req):
    username = req.user.username
    context = {"username":username }
    return render(req, "contactus.html" , context)

def userlogout(req):
    logout(req)
    return redirect("/")

def mobile_list_view(req):
    username = req.user.username
    if req.method == "GET":
        allproducts = Product.prod.mobile_list()
        context = {"allproducts":allproducts , "username":username}
        return render(req,"index.html", context)
    else :
        allproducts = Product.objects.all()
        context = {"allproducts":allproducts , "username":username}
        return render(req,"index.html", context)

def clothes_list_view(req):
    username = req.user.username
    if req.method == "GET":
        allproducts = Product.prod.clothes_list()
        context = {"allproducts":allproducts , "username":username}
        return render(req,"index.html", context)
    else :
        allproducts = Product.objects.all()
        context = {"allproducts":allproducts , "username":username}
        return render(req,"index.html", context)

def shoes_list_view(req):
    username = req.user.username
    if req.method == "GET":
        allproducts = Product.prod.shoes_list()
        context = {"allproducts":allproducts , "username":username}
        return render(req,"index.html", context)
    else :
        allproducts = Product.objects.all()
        context = {"allproducts":allproducts , "username":username}
        return render(req,"index.html", context)
    
def range_view(req):
    username = req.user.username
    if req.method == 'GET':
        return render(req,'index.html')
    else:
        r1 = req.POST.get("min")
        r2 = req.POST.get("max")
        if r1 is not None and r2 is not None and r1.isdigit() and r2.isdigit():
            allproducts=Product.prod.get_price_range(r1,r2)
            context = {'allproducts':allproducts , "username":username}
            return render(req,'index.html',context)
        else :
            allproducts=Product.objects.all()
            context = {'allproducts':allproducts , "username":username}
            return render(req,'index.html',context)

def allsortorderview(req):
    sort_option = req.GET.get("sort")
    if sort_option =="high_to_low":
        allproducts =Product.prod.order_by("-price")
    elif sort_option =="low_to_high":
        allproducts =Product.prod.order_by("price")
    else:
        allproducts =Product.objects.all()
    
    context = {'allproducts' :allproducts}
    return render(req , "index.html" , context)

# search product
def searchproduct(req):
    query = req.GET.get('q')
    errormessage = ""

    if query:
        allproducts = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(category__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )
        if len(allproducts) == 0 :
            errormessage = "No result found"

    else:
        allproducts = Product.objects.all()

    context = {"allproducts": allproducts, "query": query, "errormessage": errormessage}
    return render(req, "index.html", context)

# cart
def cart(req):
    if req.user.is_authenticated:
        username = req.user.username
        allcarts = Cart.objects.filter(userid = req.user.id)
        totalprice = 0
        for i in allcarts:
            totalprice += i.productid.price * i.quantity
        length = len(allcarts)
        context = {'allcarts':allcarts , 
                "items" :length ,
                "total" : totalprice , 
                "username":username}
        return render(req, "cart.html",context)
    else:
        allcarts = Cart.objects.filter(userid = req.user.id)
        totalprice = 0
        for i in allcarts:
            totalprice += i.productid.price * i.quantity
        length = len(allcarts)
        context = {'allcarts':allcarts , 
                "items" :length ,
                "total" : totalprice }
        return render(req, "cart.html",context)

def addtocart(request, productid):
        if request.user.is_authenticated:
            user = request.user
        else :
            user = None
        # Assuming productid is the field that uniquely identifies a product
        allproducts = get_object_or_404(Product, productid=productid )

        # Use the correct field to filter the cart item
        cartitem, created = Cart.objects.get_or_create(productid=allproducts , userid=user)

        if not created:
            cartitem.quantity += 1
        else:
            cartitem.quantity = 1

        cartitem.save()
        return redirect("/cart")

def removecart(req, productid):
    cartitem = Cart.objects.filter(productid=productid)
    cartitem.delete()
    return redirect("/cart")

def updateqty(req,qv,productid):
    allcarts=Cart.objects.filter(productid=productid)
    if qv=="1":
        total=allcarts[0].quantity + 1
        allcarts.update(quantity=total)
    else:
        if allcarts[0].quantity>1:
            total=allcarts[0].quantity - 1
            allcarts.update(quantity=total)
        else:
            allcarts=Cart.objects.filter(productid=productid)
            allcarts.delete()

    return redirect('/cart')    


def placeorder(req):
        if req.user.is_authenticated:
            user = req.user
            allcarts = Cart.objects.filter(userid = user)
            totalprice = 0
            orderid = 0
            # Iterate over cart items, calculate total price, and delete cart items
            for cart_item in allcarts:
                orderid = random.randrange(1000,9000)
                orderdata = Order.objects.create(
                    orderid = orderid , productid = cart_item.productid , quantity = cart_item.quantity , userid = cart_item.userid
                )
                orderdata.save()
                totalprice += cart_item.productid.price * cart_item.quantity
                cart_item.delete()

            # Convert totalprice to paise
            totalprice_in_paise = int(totalprice * 100)

            # Get the user associated with the request (assuming you have user authentication)
            user = req.user if req.user.is_authenticated else None

            # Create Razorpay order
            client = razorpay.Client(auth=("rzp_test_ABvnCoddVobUGU", "xqaY5agbv5y2fcuL5Bblt7vV"))
            data = {"amount": totalprice_in_paise, "currency": "INR", "receipt": "order_rcptid_11"}
            payment = client.order.create(data=data )
            length = len(allcarts)
            # Add payment details to the context
            context = {"username":user,"payment": payment, "data": payment ,"allcarts":allcarts, "items" :length ,
                    "total" : totalprice }

            # Render the template with the context
            return render(req, "placeorder.html", context)
        else :
            user = None 
            return redirect("/loginuser")


def showorders(req):
    if req.user.is_authenticated:
        user = req.user
        allorders = Order.objects.filter(userid = user)
        length = len(allorders)
        totalprice = 0
        orderid = 0
            # Iterate over cart items, calculate total price, and delete cart items
        for cart_item in allorders:
                totalprice += cart_item.productid.price * cart_item.quantity

            # Convert totalprice to paise
        totalprice_in_paise = int(totalprice * 100)
        context={'username': user , 'allorders' : allorders ,"items" :length ,
                    "total" : totalprice }
        return render(req,'orders.html',context)
    else : 
        user = None
        return redirect("/loginuser")
    
def registerproduct(req):
    if req.user.is_authenticated:
        user = req.user
        if req.method =="GET":
            form = ViewProduct()
            return render(req,"registerproduct.html" , {'form':form ,'username':user})
        else : 
            form = ViewProduct(req.POST ,  req.FILES or None)
            if form.is_valid():
                form.save()
                return redirect("/")
            else : 
                return render(req,"registerproduct.html" , {'form':form ,'username':user})
    else:
        return redirect("/loginuser")