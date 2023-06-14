from django import forms

from django.contrib.auth.models import User

from .models import News

from django.forms import ModelForm

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=65)
    email = forms.EmailField(help_text="Enter a valid email")
    password = forms.CharField(max_length=65, widget=forms.PasswordInput,help_text="Try to give a strong password")


   
class loginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class AddForm(forms.Form):
    title=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control title','placeholder':'News Title'}), max_length=200, required=True)
    content=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control content','placeholder':'News Content'}), max_length=1000, required=True)
    photo=forms.FileField(widget=forms.FileInput(attrs={'class':'form-control image','placeholder':'News Image'}),required=True)
    video=forms.FileField(widget=forms.FileInput(attrs={'class':'form-control video','placeholder':'News Video'}),required=True)


class UpdateForm(ModelForm):
    class Meta:
        model = News
        exclude = ['user_id']



