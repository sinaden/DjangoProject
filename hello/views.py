import requests

from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    #return HttpResponse('<pre>' + r.text + '</pre>')
    return render(request, "index.html")

def v1(request):

    return HttpResponse('<h1> Sina Denmark </h1>')



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
