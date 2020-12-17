from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment,Watchlist, ClosedBid, Alllistings
from datetime import datetime

from .models import User


def index(request):
    items = Listing.objects.all()
    try: 
        w = Watchlist.objects.get(user = request.user.username)
        count = len(w)
    except: 
        count = None
    return render(request, "auctions/index.html", {
        "items": items, 
        "count": count
    })

def categories(request): 
    items = Listing.objects.raw("SELECT * FROM auctions_listing GROUP BY category")
    try: 
        w = Watchlist.objects.get(user = request.user.username)
        count = len(w)
    except: 
        count = None
    return render(request, "auctions/categories.html", {
        "items": items,
    })

def category(request, cat):
    cat_items: Listing.objects.filter(category=cat)
    try: 
        w = Watchlist.objects.get(user=request.user.username)
        count=len(w)
    except: 
        count = None
    return render(request, "auctions/category.html", {
        "items" : cat_items, 
        "cat": cat, 
        "count": count
    })

def create(request): 
    try: 
        w = Watchlist.objects.get(user = request.user.username)
        count = len(w) 
    except: 
        count = None 
    return render (request, "auctions/create.html", {
        "count": count
    })

def submit(request):
    if request.method == "POST":
        listtable = Listing()
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        listtable.listed_by = request.user.username
        listtable.title = request.POST.get('title')
        listtable.description = request.POST.get('description')
        listtable.price = request.POST.get('price')
        listtable.category = request.POST.get('category')
        if request.POST.get('link'):
            listtable.link = request.POST.get('link')
        else :
            listtable.link = "https://images.digi.com/image-not-available.png"
        listtable.time = dt
        listtable.save()
        all = Alllistings()
        items = Listing.objects.all()
        for i in items:
            try:
                if Alllistings.objects.get(listingid=i.id):
                    pass
            except:
                all.listing_id=i.id
                all.title = i.title
                all.description = i.description
                all.link = i.link
                all.save()

        return redirect('index')
    else:
        return redirect('index')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

