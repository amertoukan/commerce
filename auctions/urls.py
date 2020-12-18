from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path ("category/<str:category>", views.category, name="category"),
    path("create/", views.create, name = "create"), 
    path ("submit", views.submit, name="submit"), 
    path ("listing/<int:id>", views.listing, name = "listing"), 
    path ("bidsubmit/<int:listing_id>", views.bidsubmit, name = "bidsubmit"), 
    path("comment/<int:listing_id>", views.comment, name="comment"), 
    path ("addwatchlist/<int:listing_id>", views.addWatchlist, name = "watchlist"), 
    path ('removewatchlist/<int:listing_id>', views.removeWatchlist, name="removewatchlist"),
    path ('watchlist/<str:username>', views.watchlist, name="watchlist"), 
    path("closebid/<int:listing_id>", views.closebid, name="closebid"), 
    path("won", views.winnings, name="won")
]

 