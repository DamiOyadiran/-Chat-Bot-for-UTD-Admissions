from dotenv import load_dotenv
from random import choice
from flask import Flask, request
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: Hi! I am a chatbot made to give you information regarding admissions at UTD! How can I help you today?\nAI: When is the deadline for FAFSA applications for 2023-2024?\nAI: You can complete a Free Application for Federal Student Aid (FAFSA®) form between Oct. 1, 2022, and 11:59 p.m. Central time (CT) on June 30, 2024.\n\nAI: Is there anything else I can help you with?\nHuman: What scholarships does UTD have for undergraduates?\n\nAI: UTD offers a variety of scholarships for undergraduates. You can find a list of our current scholarships here: https://www.utdallas.edu/enroll/scholarships/. Is there anything else I can help you with?\nHuman: When is the application deadline for 2023-24?\n\nAI: The deadline for the 2023-2024 academic year is June 30, 2024.\nHuman: When is the application deadline for 2023-24?\nAI:  The deadline is May 1, 2023. Anything else I can help with?\n\nAI: Is there anything else I can help you with?\nHuman: When is the application deadline for 2023-24?\nAI: The deadline for the 2023-2024 academic year is June 30, 2024. Is there anything else I can help you with?\nHuman: When is the application deadline for incoming freshman at UTD for the fall 2023 semester?\nAI: The deadline is May 1, 2023. Anything else I can help with?\nAI: Is there anything else I can help you with?\n\nHuman: When is the application deadline for incoming freshman at UTD for the fall 2023 semester?\n\nAI: The deadline for incoming freshmen at UTD for the fall 2023 semester is May 1, 2023. Is there anything else I can help you with?\nHuman: ",
  temperature=0.7,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0.6,
  stop=[" Human:", " AI:", "chatbot"]
)

def ask(question, chat_log=None):
 prompt_text = f’{chat_log}{restart_sequence}: {question}{start_sequence}:’
 response = openai.Completion.create(
 engine=”davinci”,
 temperature=0.8,
 max_tokens=150,
 top_p=1,
 frequency_penalty=0,
 presence_penalty=0.3,
 stop=[“\n”],
 )

 def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None: chat_log = session_prompt return f’{chat_log}{restart_sequence} {question}{start_sequence}{answer}’