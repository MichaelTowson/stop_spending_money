from django.db import models
import bcrypt, re

class Manager(models.Manager):
    def registerUser_validator(self, postData):
        errors = {}
        # validating email
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern
            errors['email'] = "Invalid email address!"
        mailExist = User.objects.filter(email = postData['email'])
        if mailExist:
            errors["email"] = "Email already Exist"
        # validating the names
        if len(postData['first_name']) < 3:
            errors["first_name"] = "Should be at least 2 characters"
        if len(postData['last_name']) < 3:
            errors["last_name"] = "Should be at least 2 characters"
        #validating password characters
        if len(postData['password']) < 8:
            errors["password"] = "Please make sure password is at least 8 characters"
        return errors

    def loginValidator(self, postData):
        errors = {}
        # validating email
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern
            errors['not_email'] = "Invalid email address!"
            return errors
        mailExist = User.objects.filter(email = postData['email'])
        if not mailExist:
            errors['not_email'] = "Email doesn't Exist!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=80)
    password = models.CharField(max_length=255)
    plan_start_date = models.DateField(default='2020-01-01')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Manager()
    #goals = a list of goals that the user has made.

class Goal(models.Model):
    user = models.ForeignKey(User, related_name = "goals", on_delete = models.CASCADE)
    category = models.CharField(max_length=30)
    amount = models.FloatField()
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
    