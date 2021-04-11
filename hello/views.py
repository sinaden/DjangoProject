import requests
from django.http import JsonResponse

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Greeting
from .models import ToDoList, Item

from .forms import CreateNewList, PurposeForm, MyForm

from .purpose_converter import PurposeConverter

from datetime import datetime

from github import GithubException
import base64
from github import Github




# Create your views here.
def index(request):
    #return HttpResponse('Hello from Python!')
    user = request.user
    if not user.is_authenticated:
        print("Yes")
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return render(request, "home2.html", {"name" : "test"})

def memeber_area(request):
    user = request.user
    
    if not user.is_authenticated:
        index(request)
    
    return render(request, "memeber_area.html", {"name" : user.get_username()})

def new_repo(request):
    user = request.user
    
    if not user.is_authenticated:
        index(request)
    
    return render(request, "new_repository.html", {"name" : user.get_username()})


def check_name_availability(request):
    '''Gets the name of the new repository from member_area.html and creates a new repository on github account.
    If the name was not unique otherwise ask for a new one '''

    #breakpoint()
    if request.method == 'POST':
        name = request.POST.get('repo_name')
        
        g = Github("ba98060c376542a75c234171d9576de043534a84")
        try:
            repo = g.get_repo("sinaden/"+name)
            if not repo:
                print(repo)
                print("was not outside")
                print("was not outside") 
                return JsonResponse({'message':'Name was unique'})
            else:
                print(repo)
                return JsonResponse({'message':'Repo already exists'})
        except Exception as e:
            print(e)
            user = g.get_user()
            new_repo = user.create_repo(name, description = "Created on heroku")
            new_repo.create_file("README.md", "first commit", "Repo was created on heroku")

            
            return JsonResponse({'message':'Name was unique, repo created'})

        
    return JsonResponse({'message':'request was not valid'})

def new_repo_name(request, repo_name):
    '''
    Should change the name of this method later to "new repository" and remove the other "new_repository" method.
    
    '''
    #print(repo_name)
    #return HttpResponse('<h1> Repo name is: %s </h1>' % repo_name)
        #ls = ToDoList.objects.get(id=1)
    #im = ls.item_set.get(id=id)

     # if this is a POST request we need to process the form data
    user = request.user
    
    if not user.is_authenticated:
        index(request)
    
    return render(request, "new_repository.html", {"name" : user.get_username(), "repo_name": repo_name})


def new_subsetfeature(request, repo_name):
    '''
    code copied from stackoverflow https://stackoverflow.com/questions/6142025/dynamically-add-field-to-a-form

    '''
    print("hello")
    
    print("FFFFF")
    
    if request.method == 'POST':
        form = MyForm(request.POST, extra=request.POST.get('extra_field_count'), extra_feature = request.POST.get('extra_feature_count'))
        #form = MyForm(request.POST,  s_or_f = request.POST.get('subset_or_feature'))
        print(form)
        print("new")
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                print(key)
                print(value)
                print("------")
            
            print ("valid!") 
            print ("valid!") 

            
    else:
        form = MyForm()
    return render(request, "new_subsetfeature.html", { 'form': form })


def new_datasheet_name(request, repo_name):
    '''
    Todo:
        1. Form paramters and their value should be put in the proper xml format and uploaded to github. Name should be "Purpose.xml"
        2. Find a way to get the xml converted to a form element and then we could edit it via a different form. 
        3. make interactive form, such that we can add a new field and a new subfield. Try with adding a new field from the template. 
    '''
    #ls = ToDoList.objects.get(id=1)
    #im = ls.item_set.get(id=id)

     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print("This one "+ repo_name)
        print("This one "+ repo_name)
        user = request.user 
        converter = PurposeConverter(user.get_username())

        # create a form instance and populate it with data from the request:
        form = PurposeForm(request.POST)
        # check whether it's valid:
        
        #name = request.POST.get('repo_name')
        #print(name)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            #print(name)
            print("congrats")
            
            for key, value in form.cleaned_data.items():
                if not (("title_" in key) or ("desc_" in key)):
                    print(key)
                    print(value)
                    print("------")
                    converter.form_xml(key, value)
                    print("------")
            file_name = converter.save()
            print(".................::::::: SUCCESSFULLY converted to " + file_name)


            upload_to_github(file_name)

            print(".................::::::::::::::::: DONE uploading to github :::::::::::::::....................")
            '''
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

            # redirect to a new URL:'''
            
            #return HttpResponse('it is unique')
            return JsonResponse({'result':'ok bood'})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PurposeForm()
    return render(request, "new_datasheet.html",{ "form":form, "repo_name":repo_name})

def new_datasheet(request):
    #ls = ToDoList.objects.get(id=1)
    #im = ls.item_set.get(id=id)

     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PurposeForm(request.POST)
        # check whether it's valid:
        
        name = request.POST.get('repo_name')
        print(name)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            print(name)
            print("congrats")
            '''
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

            # redirect to a new URL:'''
            #return HttpResponse('it is unique')
            return JsonResponse({'result':'ok bood'})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PurposeForm()
    return render(request, "new_datasheet.html",{ "form":form})


def v1(request, id):
    ls = ToDoList.objects.get(id=1)
    im = ls.item_set.get(id=id)
    return HttpResponse('<h1> Sina \'s Task is: %s </h1>' %im.text)

def upload_to_github(file_name):
    g = Github("ba98060c376542a75c234171d9576de043534a84")

    # change it to a dynamic input later
    repo = g.get_repo("sinaden/connect_heroku")

    #now = datetime.now()
    #dt_string = now.strftime(form.cleaned_data['name'] + "\n" + form.cleaned_data['password'] + "\n recorded at %H:%M:%S in %Y-%m-%d")

    #f = open("records.txt", "a")
    #f.write("\n" + dt_string)
    #f.close()

    with open("assets\\"+file_name, 'r') as file:
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
    git_file = git_prefix + file_name
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "updating a file:" + file_name, content, contents.sha, branch="main")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "creating a new file:" + file_name, content, branch="main")
        print(git_file + ' CREATED')

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


