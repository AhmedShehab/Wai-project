from django.test import TestCase
from .models import *
# Create your tests here.
# test for teacher
class TeacherTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(name="teacher1")
        self.teacher.save()
    def test_teacher(self):
        self.assertEqual(self.teacher.name,"teacher1")
# test for course
class CourseTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="course1")
        self.course.save()
    def test_course(self):
        self.assertEqual(self.course.name,"course1")
# test for chapter
class ChapterTest(TestCase):
    def setUp(self):
        self.chapter = Chapter.objects.create(name="chapter1",course = 1)
        self.chapter.save()
    def test_chapter(self):
        self.assertEqual(self.chapter.name,"chapter1")