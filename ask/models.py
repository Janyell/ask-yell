from django.db import models
from django.contrib.auth.models import User, UserManager

class Author(User):
    """User with app settings."""
    rating = models.IntegerField()

    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

class Question(models.Model):
    title = models.CharField(max_length = 30)
    text = models.CharField(max_length = 350)
    author = models.ForeignKey(Author)
    rel_datetime = models.DateTimeField()
    rating = models.IntegerField()

class Answer(models.Model):
    text = models.CharField(max_length = 500)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(Author)
    rel_datetime = models.DateTimeField()
    right_answer = models.BooleanField()
    rating = models.IntegerField()

class LikeQuestion(models.Model):
    author = models.ForeignKey(Author)
    question = models.ForeignKey(Question)
    datetime = models.DateTimeField()
    like_dislike = models.IntegerField()

class LikeAnswer(models.Model):
    author = models.ForeignKey(Author)
    answer = models.ForeignKey(Answer)
    datetime = models.DateTimeField()
    like_dislike = models.IntegerField()

# Create your models here.
