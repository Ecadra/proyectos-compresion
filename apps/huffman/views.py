from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("El proyecto está inicializado aquí")

# Create your views here.
