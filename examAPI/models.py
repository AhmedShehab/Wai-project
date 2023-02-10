from django.db import models
from django.contrib.auth import get_user_model
from django.core import serializers
# Create your models here.

class Teacher(models.Model):
    credentials =models.ForeignKey(get_user_model(), on_delete=models.CASCADE) 

    def __str__(self) :
        return self.credentials.username


class Course(models.Model):
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE,related_name='courses')

    @property
    def number_of_chapters (self):
        return self.chapters.all().count()
    def get_chapters(self):
        return Chapter.objects.filter(course = self).values_list('id','name')
    def __str__(self):
        return self.name

class Chapter(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE,related_name='chapters')
    name = models.CharField(max_length=50)
    
    def get_questions(self):
        return Question.objective.filter(chapter = self)
    def __str__(self):
        return self.name

class Question(models.Model):
    difficulty_choices = [
        ('difficult','difficult'),
        ('easy','easy')
    ]   
    objective_choices = [
        ('reminding','reminding'),
        ('understanding','understanding'),
        ('creativity','creativity')
    ]
    chapter = models.ForeignKey("Chapter", on_delete=models.CASCADE,related_name='questions')
    difficulty = models.CharField(max_length=10,choices= difficulty_choices)
    objective = models.CharField(max_length=15,choices= objective_choices)
    content = models.CharField( max_length=250)
    wrongAnswer1 = models.CharField(max_length=250)   
    wrongAnswer2 = models.CharField(max_length=250)   
    rightAnswer = models.CharField(max_length=250)   

    def __str__(self):
        return f'Chapter: {self.chapter} content: {self.content}'

class Exam(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE,related_name='exams')
    questions = models.ManyToManyField("Question",blank=True)
    accuracy = models.FloatField()
    def __str__(self):
        return self.course.name

