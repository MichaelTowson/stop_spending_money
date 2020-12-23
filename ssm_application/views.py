from django.shortcuts import render, HttpResponse, redirect
from ssm_application.models import User, Goal, Transaction
from django.contrib import messages
import bcrypt

#Render Template Views
def index(request):
    return render(request, "index.html")

def register(request):
    return render(request, "register.html")

def dashboard(request): 
    if 'userid' in request.session:
        return render(request, "dashboard.html")
    return redirect("/")

def goals(request):
    if 'userid' in request.session:
        logged_user = User.objects.get(id=request.session['userid'])
        context = {
            'user': logged_user,
            'user_goals': logged_user.goals.all()
        }
        return render(request, "goals.html", context)

def about(request):
    return render(request, "about.html")

#Login/Registration Views
def register_user(request):
    errors = User.objects.registerUser_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/register")
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name = first_name, last_name = last_name, email = email, password= pw_hash)
    messages.success(request, "Successfully Register", extra_tags='reg_success')
    return redirect("/")

def log_in(request):
    errors = User.objects.loginValidator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect("/")
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/dashboard')
    messages.error(request, "Password doesn't match!", extra_tags='pw_not_match')
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect("/")

#Goals Page Views
def add_goal(request):
#Add validator check ---------------!
    #Get data from request
    userid = request.session['userid']
    user = User.objects.get(id=userid) 
    category = request.POST['category']
    amount = request.POST['amount']
    
    #Create goal
    Goal.objects.create(user=user, category=category, amount=amount)
    
    return redirect("/goals")


