from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    listed_by = models.CharField(max_length = 64)
    title = models.CharField(max_length = 64)
    category = models.CharField(max_length = 64)
    price = models.IntegerField()
    description = models.CharField(max_length = 150)
    link = models.CharField (max_length = 64, default = None, blank = True, null = True)
    time = models.CharField (max_length = 64)

class Bid (models.Model): 
    user = models.CharField(max_length = 64)
    bid = models.IntegerField()
    title = models.CharField(max_length = 64)
    listing_id = models.IntegerField()

class Comment (models.Model): 
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    comment = models.TextField()
    listing_id = models.IntegerField()

class Watchlist (models.Model): 
    user = models.CharField(max_length=64)
    listing_id = models.IntegerField()

class ClosedBid(models.Model): 
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listing_id = models.IntegerField()
    price = models.IntegerField()

class Alllistings (models.Model): 
    listing_id = models.IntegerField()
    title = models.CharField(max_length = 64)
    description = models.TextField()
    link = models.CharField(max_length=64, default = None, blank = True, null = True)