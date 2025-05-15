from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Profile(models.Model) :
    avatar = models.ImageField()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)


class Answer(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.PROTECT)
    user_id = models.ForeignKey('Profile', on_delete=models.PROTECT)
    title = models.CharField()
    text = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return self.title

class Question(models.Model):
    user_id = models.ForeignKey('Profile', on_delete=models.PROTECT)
    title = models.CharField()
    text = models.TextField()
    tag_id = models.ForeignKey('Tag', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

class AnswerLike(models.Model):
    answer_id = models.ForeignKey('Answer', on_delete=models.PROTECT)
    user_id = models.ForeignKey('Profile', on_delete=models.PROTECT)


class QuestionLike(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.PROTECT)
    user_id = models.ForeignKey('Profile', on_delete=models.PROTECT)

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name