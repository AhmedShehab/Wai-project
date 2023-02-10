from django.shortcuts import render
import random
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

    def create(self, request):
        course = Course.objects.get(id=request.data.pop('course'))
        metadata = request.data.pop('metadata')
        questions = []
        total_accuracy = 0
        no_of_chapters = 0
        for chapter_data in metadata:
            no_of_chapters += 1
            chapter_questions,accuracy = select_questions(chapter_data)
            total_accuracy += accuracy
            questions.append(chapter_questions)
        total_accuracy = round((total_accuracy / no_of_chapters) * 100,2) if no_of_chapters > 0 else 0
        exam = Exam.objects.create(course=course,accuracy=total_accuracy)
        for question in questions:
            exam.questions.add(*question)
        exam.save()
        return JsonResponse({
            "msg": "Exam Created Successfully",
            'id': exam.id,
        })

# a function to get the questions for a chapter using genitic algorithm

def select_questions(data):
    # Solution Format
    # solution = [2, 0, 1, 2, 1, 0,]
    # solution = [easy-reminding, easy-understanding, easy-creativity,
    #          difficult-reminding, difficult-understanding, difficult-creativity]
    questions = []
    optimal_solution = genetic_algorithm(data)
    accuracy = fitness(optimal_solution,data)

    chapter = Chapter.objects.get(id=data['chapter'])
    chapter_questions = chapter.questions.all()
    # Get all possible questions
    easy_reminding_questions = list(chapter_questions.filter(difficulty='easy', objective='reminding'))
    easy_understanding_questions = list(chapter_questions.filter(difficulty='easy', objective='understanding'))
    easy_creativity_questions = list(chapter_questions.filter(difficulty='easy', objective='creativity'))
    difficult_reminding_questions = list(chapter_questions.filter(difficulty='difficult', objective='reminding'))
    difficult_understanding_questions = list(chapter_questions.filter(difficulty='difficult', objective='understanding'))
    difficult_creativity_questions = list(chapter_questions.filter(difficulty='difficult', objective='creativity'))
    
    # Get the selected questions
    for i in range(0, optimal_solution[0]):
        questions.append(easy_reminding_questions[i])
    for i in range(0, optimal_solution[1]):
        questions.append(easy_understanding_questions[i])
    for i in range(0, optimal_solution[2]):
        questions.append(easy_creativity_questions[i])
    for i in range(0, optimal_solution[3]):
        questions.append(difficult_reminding_questions[i])
    for i in range(0, optimal_solution[4]):
        questions.append(difficult_understanding_questions[i])
    for i in range(0, optimal_solution[5]):
        questions.append(difficult_creativity_questions[i])
    return questions,accuracy

    

def genetic_algorithm(data):
    # Population Generating
    # Gene Format gene1 = [2, 0, 1, 2, 1, 0,]
    # gene1 = [easy-reminding, easy-understanding, easy-creativity,
    #          difficult-reminding, difficult-understanding, difficult-creativity]
    population = get_population()
    generaion_No = 0
    while fitness(population[0],data) < 1 and generaion_No < 100:
        generaion_No += 1
        for _ in range(0, 6):
            # Parent Selection
            father = get_parent(population,data)
            mother = get_parent(population,data)
            # Make sure father and mother are different
            while father == mother:
                mother = get_parent(population,data)
            # Crossover
            child1,child2 = crossover(father,mother)
            # Mutation
            child1 = mutation(child1)
            child2 = mutation(child2)
            # Add to population
            population.append(child1)
            population.append(child2)
        # Selection
        population = selection(population,data)
    return population[0]

def get_population():
    population = []
    for i in range(0, 10):
        gene = []
        for j in range(0, 6):
            gene.append(random.randint(0, 2))
        population.append(gene)
    return population

def fitness(child,data):
    # gene = [easy-reminding, easy-understanding, easy-creativity,
    #          difficult-reminding, difficult-understanding, difficult-creativity]
    # Input Data
    no_of_questions = int(data['no_of_questions'])
    easy_questions = int(data['no_of_easy_questions'])
    difficult_questions = int(data['no_of_difficult_questions'])
    reminding_questions = int(data['no_of_reminding_questions'])
    understanding_questions = int(data['no_of_understanding_questions'])
    creativity_questions = int(data['no_of_creativity_questions'])
    # Generated data
    total_no_of_easy_questions = child[0] + child[1] + child[2]
    total_on_of_difficult_questions = child[3] + child[4] + child[5]
    total_no_of_questions = total_no_of_easy_questions + total_on_of_difficult_questions
    total_no_of_reminding_questions = child[0] + child[3]
    total_no_of_understanding_questions = child[1] + child[4]
    total_no_of_creativity_questions = child[2] + child[5]
    # Accuracy of generated data
    ratio = total_no_of_questions/no_of_questions if no_of_questions != 0 else 0
    accuracy1 = ratio if ratio < 1 else 1/ratio
    ratio = total_no_of_easy_questions/easy_questions if easy_questions != 0 else 0
    accuracy2 = ratio if ratio < 1 else 1/ratio
    ratio = total_on_of_difficult_questions/difficult_questions if difficult_questions != 0 else 0
    accuracy3 = ratio if ratio < 1 else 1/ratio
    ratio = total_no_of_reminding_questions/reminding_questions if reminding_questions != 0 else 0
    accuracy4 = ratio if ratio < 1 else 1/ratio
    ratio = total_no_of_understanding_questions/understanding_questions if understanding_questions != 0 else 0
    accuracy5 = ratio if ratio < 1 else 1/ratio
    ratio = total_no_of_creativity_questions/creativity_questions if creativity_questions != 0 else 0
    accuracy6 = ratio if ratio < 1 else 1/ratio
    total_accuracy = (3 * accuracy1 + accuracy2 + accuracy3 + accuracy4 + accuracy5 + accuracy6)/8
    return total_accuracy

def crossover(father,mother):
    # Crossover
    crossover_point = random.randint(0, 5)
    child1 = father[:crossover_point] + mother[crossover_point:]
    child2 = mother[:crossover_point] + father[crossover_point:]
    return child1,child2

def get_parent(population,data):
    # get parent using tournament selection
    parent1 = population[random.randint(0, 9)]
    parent2 = population[random.randint(0, 9)]
    while parent1 == parent2:
        parent2 = population[random.randint(0, 9)]
        parent2 = mutation(parent2)
    if fitness(parent1,data) > fitness(parent2,data):
        return parent1
    else:
        return parent2

def selection(population,data):
    fintess_element_list =[]
    for gene in population:
        fintess_element_list.append((fitness(gene,data),gene))
    fintess_element_list.sort(reverse=True)
    fintess_element_list = fintess_element_list[:10]
    for i in range(0, 10):
        population[i] = fintess_element_list[i][1]
    return population[:10]

def mutation(child):
    mutation_point = random.randint(0, 5)
    child[mutation_point] = random.randint(0, 2)
    return child