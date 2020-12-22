from django.shortcuts import render, HttpResponse, redirect

def index(request):
    return render(request, "index.html")

def goals(request):
    return render(request, "goals.html")