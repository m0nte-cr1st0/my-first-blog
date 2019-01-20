from django import forms
from .models import Profile, Post, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime

class SignupForm(UserCreationForm):
    city = forms.CharField(label='Город')
    contacts = forms.CharField(label='Контакты', widget=forms.Textarea, required=False)
    biography = forms.CharField(label='Биография', widget=forms.Textarea, required=False)
    other_info = forms.CharField(label='Другая информация', widget=forms.Textarea, required=False)
    avatar = forms.ImageField(label='Аватар', required=False)
    SEX = [
        ("Женский","Женский"),
        ("Мужской","Мужской")
    ]
    sex = forms.ChoiceField(label=u'Пол', choices = SEX)

    class Meta:
        model = User
        fields = ('username', 'avatar', 'first_name', 'last_name', 'email',
            'password1', 'password2', 'city', 'sex',
             'biography', 'contacts', 'other_info')


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    class Meta:
        model = Profile
        exclude = ('user', )

class ContactForm(forms.Form):
    subject = forms.CharField(required=True, label="Тема")
    contact_name = forms.CharField(required=True, label="Имя")
    contact_email = forms.EmailField(required=True, label="Email")
    content = forms.CharField(widget=CKEditorUploadingWidget(), required=True, label="Сообщение")


class PostForm(forms.ModelForm):        
    class Meta:
        model = Post
        fields = ['title', 'body', 'logo']


class CommentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, label='')
    class Meta:
        model = Comment
        fields = ['description']
