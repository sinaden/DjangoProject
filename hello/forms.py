from django import forms

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length = 200, widget=forms.TextInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}))
    password = forms.CharField(label="Password", max_length = 200, widget=forms.PasswordInput(attrs={'class': 'form-control', 'style':'max-width : 200px;'}))

    #check = forms.BooleanField(required = False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))