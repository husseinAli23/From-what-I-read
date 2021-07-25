from django.forms import ModelForm
from .models import Book, Profile , Comment
from django import forms
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from .models import Profile
from django.contrib.auth.forms import UserCreationForm , UserChangeForm , PasswordChangeForm


def __init__(self, user, *args, **kwargs):
    self.user = user
    super(RSVPForm, self).__init__(*args, **kwargs)

class PasswordChangeingForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control input-lg"})),
    new_password1=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': "form-control input-lg" })),
    new_password2=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class': "form-control input-lg" })),
    class Meta: 
        model = User
        fields =('old_password ','new_password1','new_password2')

class BookForm(ModelForm):
    
    class Meta:
        model = Book
        fields = ('name','image','description', 'book_type', 'name_auther', 'release_date')

class RegisterForm(UserCreationForm):
    name = forms.CharField( max_length= 20)

    class Meta: 
        model = User
        fields =(
            'username',
            'email')

class UserForm(UserCreationForm):

    class Meta: 
        model = User
        fields ="__all__"

YEARS= [x for x in range(1940,2021)]

class ProfileForm(forms.ModelForm):
    birth_date= forms.DateField(label='What is your birth date?', initial="1990-06-21", widget=forms.SelectDateWidget(years=YEARS))


    class Meta: 
        model = Profile
        fields =('image','About_me','birth_date','Gender' ,'countries','name')
   

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    exclude = ['user','book','status']

class SettingForm(ModelForm):
  
    class Meta:
        model = User
        fields=['first_name','last_name','email']
       
        



