import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from dotenv import load_dotenv
from random import choice
import openai
from django.views import View

# Create your views here.

def chatbot(request):
    return render(request, 'chatbot/chatbot.html')
