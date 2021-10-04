from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    # The meta class says which model to use and which fields to display
    class Meta:
        model = Comment
        # THIS COMMA BELOW IS V IMPORTANT, IT'S A TUPLE NOT A STRING
        fields = ('body',)

