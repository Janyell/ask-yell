import sys, os

sys.path.append('/home/yell/ask_yell')
from models import *
from forms import QuestionForm
from datetime import datetime

def count_answer(ques_id):
    return Answer.objects.filter(question=ques_id).count()

def last_authors():
    return Author.objects.filter(is_superuser=0).order_by("-date_joined")[:10]

def question_form(form, author_id):
    if form.is_valid(): # All validation rules pass
        title = form.cleaned_data['title']
        text = form.cleaned_data['text']
        
        new_question = Question.objects.create(title = title, text = text, author_id = author_id, rel_datetime = datetime.now(), rating=0)
        new_question.save()
	return form
