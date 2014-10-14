from django.forms import *
from ask.models import *

# Create the form class.
class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title','text']
        widgets = {
            'title': TextInput(attrs={'class': "inline span12", 'name': "title", 'id': "question_title", 'placeholder': "Type your title here", 'maxlength': 30, 'required': 1}),
            'text': Textarea(attrs={'class': "inline span12", 'name': "question", 'id': "question_text", 'placeholder': "Type your question here", 'style':"resize:none", 'rows': 8, 'maxlength': 350, 'required': 1}),
        }

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['text']
        widgets = {
        	'text': Textarea (attrs={'id':"answer", 'style': "resize: none; width: 100%; height: 100px;", 'required': 1, 'placeholder': "Type your answer here", 'maxlength': 500})
        }

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['email','username','password']
        widgets = {
            'username': TextInput(attrs={'class': "inline span12", 'name': "username", 'id': "author_username", 'placeholder': "Type your username here", 'maxlength': 30, 'required': 1}),
            'password': PasswordInput(attrs={'class': "inline span12", 'name': "password", 'id': "author_password", 'placeholder': "Type your password here", 'maxlength': 128, 'required': 1}),
        }