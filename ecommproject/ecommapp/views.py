from django.shortcuts import render,redirect , get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
# Create your views here.


def index(req):
    return render(req, "index.html")


def loginuser(req):
    if req.method == "POST":  # Corrected method to lowercase "post"
        uname = req.POST.get("uname")
        passwd = req.POST.get("passwd")
        context = {}
        if not (uname and passwd):
            context['errormessage'] = "Fields can't be empty"
            return render(req, "loginuser.html", context)
        else:
            userdata = authenticate(username=uname, password=passwd)
            if userdata is not None:
                login(req, userdata)
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
                return redirect("/")
            except:
                context["errormessage"] = "User Already exists"
                return render(req, "registeruser.html" , context)
    else:
        return render(req, "registeruser.html")


def aboutus(req):
    return render(req, "aboutus.html")


def contactus(req):
    return render(req, "contactus.html")
