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


def listing(request, id): 
    try: 
        item = Listing.objects.get(id = id)
    except: 
        return redirect('index')
    try: 
        comments = Comment.objects.filter(listing_id = id)
    except: 
        comments = None 
    if request.user.username: 
        try: 
            if Watchlist.objects.get(user = request.user.username, listing_id = id): 
                added = True 
        except: 
            added = False 
        try: 
            l = Listing.objects.get(id = id)
            if l.listed_by == request.user.username:
                owner = True 
            else: 
                owner = False 
        except: 
            return redirect ('index')
    else: 
        added = False 
        owner = False 
    try: 
        w = Watchlist.objects/get(user = request.user.username)
        count = len(w) 
    except: 
        count = None 
    return render (request, "auctions/listing.html", {
        "i": item, 
        "error": request.COOKIES.get('error'), 
        "errorgreen": request.COOKIES.get('errorgreen'), 
        "comments": comments, 
        "added": added, 
        "count": count, 
        "listed_by": owner
    })

def bidsubmit(request, listing_id): 
    currentBid = Listing.objects.get(id = listing_id)
    currentBid = currentBid.price
    if request.method == "POST": 
        newBid = int(request.POST.get("bid"))
        if newBid > currentBid: 
            listing = Listing.objects.get(id=listing_id)
            listing.price = newBid
            listing.save()
            try: 
                if Bid.objects.filter(id = listing_id): 
                    bid_row = Bid.objects.filter(id = listing_id)
                    bid_row.delete() 
                bid_table = Bid() 
                bid_table.user = request.user.username 
                bid_table.title = listing.title 
                bid_table.listing_id = listing_id
                bid_table.bid = newBid
                bid_table.save() 
            except: 
                bid_table = Bid() 
                bid_table.user = request.user.username 
                bid_table.title = listing.title 
                bid_table.listing_id = listing_id
                bid_table.bid = newBid
                bid_table.save() 
            response = redirect('listing', id = listing_id)
            response.set_cookie("errorgreen", "STOP THE COUNT! Your bid is now the highest bid.", max_age = 3)
            return response 
        else: 
            response = redirect("listing", id = listing_id)
            response.set_cookie("error", "Oh uh! It seems your bid is lower than the current bid. Please select a higher bid.", max_age=3)
            return response 
    else: 
        return redirect('index')

def comment(request,listing_id):
    if request.method == "POST":
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        c = Comment()
        c.comment = request.POST.get('comment')
        c.user = request.user.username
        c.time = dt
        c.listing_id = listing_id
        c.save()
        return redirect('listing',id=listing_id)
    else :
        return redirect('index')

def addWatchlist(request,listing_id):
    if request.user.username:
        w = Watchlist()
        w.user = request.user.username
        w.listing_id = listing_id
        w.save()
        return redirect('listing',id=listing_id)
    else:
        return redirect('index')

def removeWatchlist(request, listing_id): 
    if request.user.username:
        try:
            w = Watchlist.objects.get(user=request.user.username,listing_id=listing_id)
            w.delete()
            return redirect('listing',id=listing_id)
        except:
            return redirect('listing',id=listing_id)
    else:
        return redirect('index')

def watchlist(request, username):
    if request.user.username: 
        try: 
            w = Watchlist.objects.filter(user = username) 
            items = []
            for item in watchlist: 
                items.append(Listing.objects.filter(id = item.listing_id))
            try: 
                w = Watchlist.objects.filter(user = request.user.username )
                count = len(w) 
            except:
                count = None 
            return render (request, "auctions/watchlist.html", {
                "items": items, 
                "count": count
            })
        except: 
            try: 
                w = Watchlist.objects.filter(user = request.user.username)
                count = len (w)
            except: 
                count = None 
            return render(request, "auctions/watchlist.html", {
                "items": items, 
                "count": count
            })
    else: 
        return redirect('index')


def closebid(request, listing_id): 
    if request.user.username: 
        try: 
            l = Listing.objects.get(id = listing_id)
        except: 
            return redirect('index')
        cb = ClosedBid() 
        title = l.title 
        cb.listed_by = l.listed_by
        cb.listing_id = listing_id
        try: 
            b = Bid.objects.get(listing_id = listing_id, bid = l.price)
            cb.winner = b.user 
            cb.price - b.bid 
            b.delete() 
        except: 
            cb.winner = l.listed_by
            cb.price = l.price 
            cb.save() 
        try: 
            if Watchlist.objects.filter(listing_id = listing_id): 
                w = Watchlist.objects.get(listing_id = listing_id)
                w.delete() 
            else: 
                pass 
        except: 
            pass
        try: 
            comment = Comment.objects.filter(listing_id = listing_id)
            comment.delete() 
        except: 
            pass 
        try: 
            Bid.objects.filter(listing_id = listing_id).delete() 
        except: 
            pass 
        try: 
            cb_list = ClosedBid.objects.filter(listing_id = listing_id)
        except: 
            cb.owner = l.listed_by 
            cb.winner = l.listed_by
            cb.listing_id = listing_id
            cb.price = l.price 
            cb.save() 
            cb_list = ClosedBid.objects.get(listing_id = listing_id)
            l.delete() 
        try: 
            w = Watchlist.object.filter(user = request.user.username)
            count = len(w) 
        except:  
            count = None 
        return render(request, "auctions/winnings.html", {
            "cb": cb_list, 
            "title": title, 
            "count": count
        })

def winnings(request): 
    if request.user.username: 
        items = []
        try: 
            won_items = ClosedBid.objects.filter(winner = request.user.username)
            for w in won_items: 
                items.append(Alllistings.objects.filter(listing_id = listing_id))
        except: 
            won_items = None 
            items = None 
        try: 
            w = Watchlist.objects.filter(user = request.user.username)
            count = len(w) 
        except: 
            count = None 
        return render (request, "auctions/winnings.html", {
            "items": items, 
            "count": count, 
            "wonitems": won_items
        })
            
        
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

