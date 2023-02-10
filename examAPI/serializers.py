from rest_framework import serializers as serial
from .models import *

class TeacherSerializer(serial.ModelSerializer):
    class Meta:
        model = Teacher
        fields= "__all__"

class CourseSerializer(serial.ModelSerializer):
    class Meta:
        model = Course
        fields= "__all__"
    

class ChapterSerializer(serial.ModelSerializer):
    class Meta:
        model = Chapter
        fields= "__all__"

class QuestionSerializer(serial.ModelSerializer):
    class Meta:
        model = Question
        fields= "__all__"

class ExamSerializer(serial.ModelSerializer):
    class Meta:
        model = Exam
        fields= "__all__"