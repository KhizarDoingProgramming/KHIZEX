from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Team, Project, Task, Post, Comment, Message


class GENZAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'your username',
        'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'your password'
    }))


class GENZUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'pick a unique username',
        'autofocus': True
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'your@email.com'
    }))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'first name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'last name'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'create a strong password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'confirm your password'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'tell us about yourself...',
                'rows': 4
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-input'
            }),
        }


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'members']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'team name'
            }),
            'members': forms.SelectMultiple(attrs={
                'class': 'form-input'
            }),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'team']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'project name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'what is this project about?',
                'rows': 4
            }),
            'team': forms.Select(attrs={
                'class': 'form-input'
            }),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assignee', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'describe the task...',
                'rows': 3
            }),
            'assignee': forms.Select(attrs={
                'class': 'form-input'
            }),
            'status': forms.Select(attrs={
                'class': 'form-input'
            }),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'whats on your mind? share updates, ideas, or vibes...',
                'rows': 4
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'drop a comment...',
            }),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'receiver': forms.Select(attrs={
                'class': 'form-input'
            }),
            'content': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'type your message...',
            }),
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'your@email.com'
    }))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'first name'
    }))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'last name'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
