from django.shortcuts import render, HttpResponse, redirect

#Render Routes
def index(request):
    return render(request, "index.html")

def register(request):
    return render(request, "register.html")

def goals(request):
    return render(request, "goals.html")

def dashboard(request):
    return render(request, "dashboard.html")

def about(request):
    return render(request, "about.html")