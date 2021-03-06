from django.shortcuts import render, HttpResponse, redirect
from ssm_application.models import User, Goal, Transaction
from django.contrib import messages
import datetime
import bcrypt

#Render Template Views
def index(request):
    return render(request, "index.html")

def register(request):
    return render(request, "register.html")

def dashboard(request): 
    if 'userid' in request.session:
        logged_user = User.objects.get(id=request.session['userid'])
        user_goal = logged_user.goals.all()
        
        #Calculate the remaining time in the plan, which will be displayed on the render.
        selected_date = logged_user.plan_start_date #datetime object
        selected_date = datetime.datetime.strftime(selected_date, '%Y-%m-%d')
        selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
        end_date = selected_date + datetime.timedelta(days=7)
        time_remaining = end_date - datetime.datetime.now() #timedelta
        
        #Nicky's code for storing transactions
        trans_dict = {}
        bal_trans = {}
        for val in user_goal:
            sum = 0
            for trans in val.transactions.all():
                sum += trans.amount
            trans_dict[val.category] = sum
            bal_trans[val.category] = val.amount - sum
        print(trans_dict)
        
        #Context we are passing to webpage
        context = {
            'user': logged_user,
            'user_goals': user_goal,
            'time_remaining': time_remaining,
            'goal_trans': trans_dict,
            'goal_bal': bal_trans,
            # 'trans': user_goal.transactions.all()
        }
        return render(request, "dashboard.html", context)
    return redirect("/")

def goals(request):
    if 'userid' in request.session:
        logged_user = User.objects.get(id=request.session['userid'])
        plan_start_date = str(logged_user.plan_start_date)
        if(plan_start_date == "2020-01-01"): #This is the default date for a new user. It determines if the "goals" page should display the start date for the plan or not.
            valid_start = 0
        else:
            valid_start = 1
        print(valid_start)
        context = {
            'user': logged_user,
            'user_goals': logged_user.goals.all(),
            'valid_start': valid_start
        }
        return render(request, "goals.html", context)
    return redirect("/")

def about(request):
    return render(request, "about.html")

def log_trans(request):
    if 'userid' in request.session:
        goal_id = request.POST['category']
        goal = Goal.objects.get(id = goal_id)
        purchase_date = request.POST['purchase_date']
        amt_spent = request.POST['amt_spent']
        desc = request.POST['desc']
        Plan_or_not = request.POST['Plan_or_not']
        how_happy = request.POST['how_happy']
        Transaction.objects.create(goal = goal, date = purchase_date, amount = amt_spent, description = desc, planned = Plan_or_not, happiness = how_happy)
        return redirect("/dashboard")
    return redirect("/")

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
    amount = float(amount)
    amount = round(amount, 2)
    
    #Create goal
    Goal.objects.create(user=user, category=category, amount=amount)
    
    return redirect("/goals")

def delete_goal(request, id):
    this_goal = Goal.objects.get(id=id)
    if(request.session['userid'] == this_goal.user.id):
        this_goal.delete()
    return redirect("/goals")

def delete_trans(request, trans_id):
    if 'userid' in request.session:
        this_trans = Transaction.objects.get(id = trans_id)
        this_trans.delete()
        return redirect("/dashboard")
    return redirect("/")



def add_start_date(request):
    user = User.objects.get(id=request.session['userid'])
    selected_date = request.POST['selected_date']
    print('Here is the first selected date:')
    print(selected_date)
    
    selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
    print('Here is the modified selected date:')
    print(selected_date)
    
    dateDifference = selected_date - datetime.datetime.now() #Subtracts the current time from the selected date.
    dateDifference = dateDifference.total_seconds()
    dateDifference = int(dateDifference)
    print(dateDifference)
    if(dateDifference <= -86400): #86400 is the amount of seconds in a day. So, this checks to see if the date was within 24 hours of "now".
        print("Invalid: Date is in the past")
    elif(dateDifference >= -86400):
        print("Date is valid.")
        user.plan_start_date = request.POST['selected_date']
        user.save()
    return redirect("/goals")