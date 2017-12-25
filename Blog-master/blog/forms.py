from django import forms
from .models import Post, Comment, Heart

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

'''class Heart(forms.ModelForm):
		class Meta:
				model = Heart
				fields = ('lover',)'''