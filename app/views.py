from tkinter.messagebox import QUESTION

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'text for question = {i}. Blalabla some text: '
                f'Hard frost and sunshine – a day of pleasure!'
                f'You are still drowsy at your leisure'
                f'It’s time, my beauty, ope your eyes!'

    } for i in range(20)
]

def index(request):
    page = paginate(QUESTIONS,request,5)
    return render(request, 'index.html', context={'questions':page.object_list,'page_object' : page})

def hot(request):
    page = paginate(QUESTIONS, request, 5)
    return render(request, 'hot.html', context={'questions':page.object_list,'page_object' : page})

def tag(request):
    page = paginate(QUESTIONS, request, 5)
    return render(request, 'tag.html', context={'questions':page.object_list,'page_object' : page})

def question(request, question_id):
    return render(request, 'question.html', context={'question':QUESTIONS[question_id]})

def login(request):
    return render(request, 'login.html', context={'questions':QUESTIONS})

def signup(request):
    return render(request, 'signup.html', context={'questions':QUESTIONS})

def ask(request):
    return render(request, 'ask.html', context={'questions':QUESTIONS})

def paginate(objects_list, request, per_page=5):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list,per_page)
    page = paginator.page(page_num)
    return page