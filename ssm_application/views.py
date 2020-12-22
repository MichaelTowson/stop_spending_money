from django.shortcuts import render, HttpResponse, redirect

def goals(request):
    return render(request, "goals.html")