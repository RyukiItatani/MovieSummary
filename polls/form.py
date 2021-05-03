from django import forms

class UserForm(forms.Form):
    url = forms.URLField(label="URL",required=False,widget=forms.URLInput(attrs={'size':50}))