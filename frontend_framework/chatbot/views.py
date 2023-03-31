import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from dotenv import load_dotenv
from random import choice
import openai
from django.views import View
from model_training.prompt_completion import format
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(f"data: {data}")
        prompt = data['prompt']
        print(f"prompt: {prompt}")
        response = format(prompt)
        print(f"response: {response}" )
        print("response slit: " +response.choices[0].text.strip())
        return JsonResponse({'output': response['choices'][0]['text']})
    else:
        return render(request, 'chatbot/chatbot.html')