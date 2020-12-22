from django.db import models
import bcrypt, re

class Manager(models.Manager):
    def registerUser_valiadtor(self, postData):
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Manager()
    #goals = a list of goals that the user has made.

class Goal(models.Model):
    user = models.ForeignKey(User, related_name = "goals", on_delete = models.CASCADE)
    category = models.CharField(max_length=30)
    balance = models.FloatField()
    start_date = models.DateField()
    #transactions - a list of transactions underneath each goal.

class Transaction(models.Model):
    goal = models.ForeignKey(Goal, related_name = "transactions", on_delete = models.CASCADE) 
    date = models.DateField()
    amount = models.FloatField()
    description = models.CharField(max_length = 50)
    planned = models.CharField(max_length = 3)
        #OPTIONS: (1) Yes, (2) No
    happiness = models.CharField(max_length = 20)
        #OPTIONS: (1) Very Happy, (2) Briefly Happy, (3) The Same, (4) Less Happy/Regret
    