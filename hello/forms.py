from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}))
    password = forms.CharField(label="Password", max_length = 200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}))

    #check = forms.BooleanField(required = False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
class PurposeForm(forms.Form):
    
    title_motivation = forms.CharField(required=False, label="Motivation",  widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))
    desc_motivation = forms.CharField(required=False, 
     label="The questions in this category are primarily intended to encourage dataset creators to clearly articulate their reasons for creating the dataset and to promote transparency about funding interests.", 
      widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))

    motivation_1 = forms.CharField(required=False,label="For what purpose was the dataset created?",
    help_text='Was there a specific task in mind? Was there a specific gap that needed to be filled? Please provide a description.', widget=forms.Textarea(attrs={'class': 'form-control'}))
    motivation_2 = forms.CharField(required=False,
    label="Who created the dataset (e.g., which team, research group) and on behalf of which entity (e.g., company, institution, organization)?", widget=forms.Textarea(attrs={'class': 'form-control'}))
    motivation_3 = forms.CharField(required=False,label="Who funded the creation of the dataset?",
    help_text='If there is an associated grant, please provide the name of the grantor and the grant name and number.', widget=forms.Textarea)
    
    motivation_4 = forms.CharField(required=False,label="Any other comments?",
    help_text='If there is an associated grant, please provide the name of the grantor and the grant name and number.', widget=forms.Textarea)

    title_composition = forms.CharField(required=False,label="Composition", 
     widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))

    desc_composition = forms.CharField(required=False,label="Most of these questions are intended to provide dataset consumers with the information they need to make informed decisions about using the dataset for specific tasks. The answers to some of these questions reveal information about compliance with the EU’s General Data Protection Regulation (GDPR) or comparable regulations in other jurisdictions.", 
     widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))

    composition_1 = forms.CharField(required=False,label="What do the instances that comprise the dataset represent (e.g., samples, images, people)?",
    help_text='Are there multiple types of instances (e.g., samples, images, and people), interactions (e.g., nodes and edges), resolutions (e.g., genetic data, single cell expression vs. tissue expression, cell counts, different image technologies, etc.)? Please provide a description.', max_length = 200, widget=forms.Textarea(attrs={'class': 'form-control','title':"MYMEGATITLE", 'style':'max-width : 200px;'}))



#dynamic form
class MyForm(forms.Form):
    #original_field = forms.CharField(required=False)
    extra_field_count = forms.CharField(widget=forms.HiddenInput())
    extra_feature_count = forms.CharField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)
        extra_feature = kwargs.pop('extra_feature', 0)
        super(MyForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields
        
        print("--------------------------------")
        print("--------------------------------")
        print("--------------------------------")
        print("extra_fields are gonna be iterated")
        print(extra_fields)
        print("--------------------------------")
        print("--------------------------------")
        print("--------------------------------")
        print("--------------------------------")
        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['subset_{index}_title'.format(index=index)] = \
                forms.CharField(required=False, label="Subset {index}".format(index = index),  widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))
            
            self.fields['subset_{index}_1'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the ID of the Subset?")
            self.fields['subset_{index}_2'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the Name of the Subset?")
        ######################
        self.fields['extra_feature_count'].initial = extra_feature
         
        for index in range(int(extra_feature)):
            # generate extra fields in the number specified via extra_fields
            self.fields['feature_{index}_title'.format(index=index)] = \
                forms.CharField(required=False, label="Feature {index}".format(index = index),  widget=forms.TextInput(attrs={'style':'visibility:hidden; height:0px; padding:0px;'}))
            self.fields['feature_{index}_1'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the ID of the Feature?")
            self.fields['feature_{index}_2'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the ID of the reference subset of the feature?")
            self.fields['feature_{index}_3'.format(index=index)] = \
                forms.CharField(required=False, label = "What is the introduction date of the feature?")