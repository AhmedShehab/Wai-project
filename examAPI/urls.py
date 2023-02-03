
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .apis import *
from .views import *





urlpatterns = [
    path('',viewExam,name='view_exams'),
    path('new_exam/',newExam,name='new_exam'),
    path('exam_instance/<int:id>/',ExamDetailView,name='exam_instance'),
    path('add_questions/',addQuestions,name='add_questions')
]

router = DefaultRouter()
router.register('teacher', TeacherView, basename='teacher')
router.register('course', CourseView, basename='course')
router.register('chapter', ChapterView, basename='chapter')
router.register('question', QuestionView, basename='question')
router.register('exam_metadata', ExamMetadataView, basename='exam_metadata')
router.register('exam', ExamView, basename='exam')
# router.register('generate_exam',ExamGeneratorView,basename='generate_exam')
urlpatterns += router.urls