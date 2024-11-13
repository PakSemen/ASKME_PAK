import copy

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

QUESTIONS = [
    {
        'title': f'Title{i}',
        'id': i,
        'text': f'text {i}'
    } for i in range(1,20)
]
def index(request):
    return render(
        request, 'index.html',
        context={'questions': QUESTIONS}
    )

def hot(request):
    hot_questions = copy.deepcopy(QUESTIONS)
    hot_questions.reverse()
    return render(
        request, 'hot.html',
        context={'questions': hot_questions}
    )

def question(request, question_id):
    one_question = QUESTIONS[question_id]
    return render(request, 'one_question.html',
                  context={'questions': one_question}
    )

def login(request):
    return render(request, 'login.html'
    )

def register(request):
    return render(request, 'signup.html'
    )

def ask(request):
    return render(request, 'ask.html'
    )