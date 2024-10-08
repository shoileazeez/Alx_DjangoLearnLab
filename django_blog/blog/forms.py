from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Exclude 'author' from the form
        widgets = {
            'tags': TagWidget(),  # Use TagWidget to display tags more effectively
        }

    def __init__(self, *args, **kwargs):
        # Pass the logged-in user to the form
        self.user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super(PostForm, self).save(commit=False)
        if self.user and not post.pk:  # Set author only when creating a new post
            post.author = self.user
        if commit:
            post.save()
        return post
    
class CommentForm(forms.ModelForm):
    class meta:
        model = Comment
        fields = ['content']    
        
        
        
        def clean_content(self):
            content = self.cleaned_data.get('content')
            if len(content) < 5:
                raise forms.ValidationError('The comment is too short. Minimum 5 characters required.')
            return content