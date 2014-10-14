# Create your views here.
from django import forms
from datetime import datetime
from ask.models import * 
from ask.forms import *
from ask.func import *
from django.http import *
from django.shortcuts import render, render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout

def question_list(request, sort='new', author_pk=None):
    if request.method == 'POST': # If the form has been submitted...
        form = QuestionForm(request.POST) # A form bound to the POST data
        form = question_form(form,request.user.pk)
    else:
        form = QuestionForm()

    if author_pk is not None:
        if not request.user.is_active:
            return HttpResponseRedirect('/login/')
        author = Author.objects.get(pk=author_pk)
        if sort == 'new':
            question_list = Question.objects.filter(author=author_pk).order_by('-rel_datetime')
        else:
            question_list = Question.objects.filter(author=author_pk).order_by('-rating')
        count_question = Question.objects.filter(author_id=author_pk).count()
        count_answer = Answer.objects.filter(author_id=author_pk).count()
        out = {"count_question": count_question,
               "count_answer": count_answer }
    else:
        author = None
        if sort == 'new':
            question_list = Question.objects.order_by('-rel_datetime')
        else:
            question_list = Question.objects.order_by('-rating')
        out = {}
    paginator = Paginator(question_list, 20) # Show 20 contacts per page

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)
    #count_answer = {}
    #for question in questions:
    #    count_answer.update({question.id: Answer.objects.filter(question=question.id).count()})
    out.update({
        "questions": questions,
    #    "count_answer": count_answer,
        "last_authors": last_authors(),
        "question_form": form
    })
    if author is not None:
        out.update({"author": author})
    return render(request, 'question_list.html', out)


def question_detail(request, question_pk):
    try:
        question = Question.objects.get(pk=question_pk)
    except Question.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        if 'title' in request.POST:
            ques_form = QuestionForm(request.POST)
            answer_form = AnswerForm()
            ques_form = question_form(ques_form,request.user.pk)
        else:
            answer_form = AnswerForm(request.POST)
            ques_form = QuestionForm()
            if answer_form.is_valid():
                text = answer_form.cleaned_data['text']

                new_answer = Answer.objects.create(text = text, question_id = question_pk, author_id = request.user.pk, rel_datetime = datetime.now(), right_answer = 0, rating=0)
                new_answer.save()    
    else:
        answer_form = AnswerForm()
        ques_form = QuestionForm()
    answer_list = Answer.objects.filter(question = question).order_by('-rating','-rel_datetime')
    paginator = Paginator(answer_list, 30) # Show 30 questions per page

    page = request.GET.get('page')
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answers = paginator.page(paginator.num_pages)
    out = {"question": question, 
           "answers": answers, 
           "last_authors": last_authors(), 
           "answer_form": answer_form,
           "question_form": ques_form
    } 
    return render(request, 'question_detail.html', out)


def registration(request):
    if not request.user.is_active:
        if request.method == 'POST':
            form = AuthorForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']

                new_author = Author.objects.create(username = username, email = email, is_staff = 0, is_active = 1, date_joined = datetime.now(), rating=0)
                new_author.set_password(password)
                new_author.save()

                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')    
        else:
            form = AuthorForm()
        out = {'author_form': form, 'last_authors': last_authors()} 
        return render(request, "registration.html", out)
    else:
        return HttpResponseRedirect('/')


def log_in(request):
    if not request.user.is_active:
        out={}
        if request.method == 'POST':
            form = AuthorForm(request.POST)
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                out.update({"error": 1})
        else:
            form = AuthorForm()
        out.update({'author_form': form})
        out.update({'last_authors': last_authors()}) 
        return render(request, "login.html", out)
    else:
        return HttpResponseRedirect('/')


def log_out(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    logout(request)
    return HttpResponseRedirect("/")


def answer_list(request, author_pk, sort='new'):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if sort == 'new':
        answer_list = Answer.objects.filter(author=author_pk).order_by('-rel_datetime')
    else:
        answer_list = Answer.objects.filter(author=author_pk).order_by('-rating')
    paginator = Paginator(answer_list, 30) # Show 30 answers per page

    page = request.GET.get('page')
    try:
        answers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        answers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        answers = paginator.page(paginator.num_pages)
    count_question = Question.objects.filter(author_id=author_pk).count()
    count_answer = Answer.objects.filter(author_id=author_pk).count()
    out = {
        "answers": answers,
        "author": Author.objects.get(pk=author_pk),
        "last_authors": last_authors(),
        "count_question": count_question,
        "count_answer": count_answer 
    }
    if request.method == 'POST': # If the form has been submitted...
        form = QuestionForm(request.POST) # A form bound to the POST data
        form = question_form(form,request.user.pk)
    else:
        form = QuestionForm()
    out.update({"question_form": form})           
    return render(request, 'answer_list.html', out)


def right_answer(request,answer_pk):
    if request.method == 'POST':
        answer = Answer.objects.get(pk=answer_pk)
        if answer.right_answer == 0:
            answer.right_answer = 1
        else:
            answer.right_answer = 0
        answer.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect('/')

def page_not_found(request):
    return render(request, '404.html', {'error404': 1})    

#def like_question(request, question_pk):
#   if request.method == 'POST':
#        old_like = LikeQuestion.objects.filter(question_id=question_pk, author_id=request.user.pk).annotate(Count(like_dislike))
#        if old_like[0].entry__count == 0:
#            new_like = LikeQuestion.objects.create(question_id = question_pk, author_id=request.user.pk, datetime = datetime.now(), like_dislike = 1)
#            question = Question.objects.get(pk=question_pk)
#            question.author.rating += 3
#            new_like.save()
#            question.author.save()
#        else:
#            new_like = LikeQuestion.objects.create(question_id = question_pk, author_id=request.user.pk, datetime = datetime.now(), like_dislike = 0)
#            question = Question.objects.get(pk=question_pk)
#            question.author.rating += 3
#            new_like.save()
#            question.author.save()
#        return HttpResponseRedirect(request.META['HTTP_REFERER'])
#    else:
#        return HttpResponseRedirect('/') 