from django.shortcuts import render

# Rest related modules
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from .models import *
from .serializers import *
import json
from django.http.response import JsonResponse

class TeacherView(viewsets.ModelViewSet):
    # Filters
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'

    # Ordering
    ordering_fields = '__all__'
    ordering = ['-id']

    search_fields = ['name']
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

class CourseView(viewsets.ModelViewSet):
    # Filters
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'

    # Ordering
    ordering_fields = '__all__'
    ordering = ['-id']

    search_fields = ['name']
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

class ChapterView(viewsets.ModelViewSet):
    # Filters
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'

    # Ordering
    ordering_fields = '__all__'
    ordering = ['-id']

    search_fields = ['name']
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()

class QuestionView(viewsets.ModelViewSet):
    # Filters
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'

    # Ordering
    ordering_fields = '__all__'
    ordering = ['-id']

    search_fields = ['content']
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

class ExamView(viewsets.ModelViewSet):
    # Filters
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'

    # Ordering
    ordering_fields = '__all__'
    ordering = ['-id']

    search_fields = ['questions']
    serializer_class = ExamSerializer
    queryset = Exam.objects.all()

class ExamMetadataView(viewsets.ModelViewSet):
    # Filters
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'

    # Ordering
    ordering_fields = '__all__'
    ordering = ['-id']

    search_fields = ['name']
    serializer_class = ExamMetadataSerializer(many = True)
    queryset = ExamMetadata.objects.all()
    
    def create(self,request):
        data = request.data
        exam = Exam.objects.get(id=int(data['exam']))
        for object in data['metadata']:
            chapter_id = object['chapter']
            easy =  int(object['no_of_easy_questions']),
            difficult = int(object['no_of_difficult_questions'])
            chapter = Chapter.objects.get(id=chapter_id)
            chapter_easy_questions = chapter.questions.filter(difficulty = "easy")[:easy[0]]
            chapter_difficult_questions = chapter.questions.filter(difficulty = 'difficult')[:difficult]
            exam.questions.add(*list(chapter_easy_questions))
            exam.questions.add(*list(chapter_difficult_questions))
        exam.save()
        return JsonResponse({
            "exam":exam.id
        })


class ExamGeneratorView(viewsets.ModelViewSet):
    # Filters
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'

    # Ordering
    ordering_fields = '__all__'
    ordering = ['-id']

    search_fields = ['questions']