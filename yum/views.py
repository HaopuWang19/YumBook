from django.shortcuts import render
from yum.models import *
from django.shortcuts import redirect



def index(request):
    return render(request, 'yum/index.html', context={})

def about(request):
    return render(request, 'yum/about.html', context={})


def privacy(request):
    return render(request, 'yum/privacy.html', context={})


def contact(request):
    return render(request, 'yum/contact.html', context={})
