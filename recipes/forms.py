from django import forms

from .models import Comment, Recipe

class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'instructions', 'image']

class CommentForm(forms.ModelForm):
    text = forms.CharField(label="Add your comment: ", widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('text',)

