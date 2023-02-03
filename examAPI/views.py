from django.shortcuts import render
from .models import *
from django import forms
# Create your views here.

def home(request):
    return render(request,'examAPI/layout.html',{
        'questions':Question.objects.all()
    })


def newExam(request):
    if request.method == "GET":
        return render(request,'examAPI/create_exam.html')
    if request.method == "POST":
        # Exam id
        # Exam metadata 
        
        return render(request,'examAPI/create_exam.html')
        

def viewExam(request):
    if request.method == "GET":
        exams = Exam.objects.all()
        return render(request,'examAPI/view_exams.html',{
            "exams":exams
        })
    if request.method == "POST":
        return

def ExamDetailView(request,id):
    if request.method == "GET":
        exam = Exam.objects.get(id=id)
        return render(request,'examAPI/exam_instance.html',{
            "exam":exam
        })
    if request.method == "POST":
        return
def addQuestions(request):
    if request.method == "GET":
        return render(request,'examAPI/questions.html',{
        })