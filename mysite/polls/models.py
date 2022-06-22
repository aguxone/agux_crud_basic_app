from django.db import models
import datetime
from django.utils import timezone


# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # We add the famous "__str__" that finally gives de description
    # of the object when we call with django
    def __str__(self):
        return self.question_text

    # And also a method for this class which will retrieve if the pubdate
    # is recent or not (True or false)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
