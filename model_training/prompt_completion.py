import openai

max_context = 6
context_array = []

def format(input):
    # Stuff done that we'll figure out to maximalize its accuracy for the model

    # Remove last question-answer pairing from the context
    if (len(context_array) > max_context):
        context_array = context_array[2:]
    context_array[len(context_array)] = input

    create_question()

    model_completion_prompt = input + " ->"
    context = ''
    
    output = model_completion(model_completion_prompt)
    return output

def model_completion(input):
    return openai.Completion.create(
        model='ada:ft-cs-chatbot-t5-2023-03-09-03-56-59',
        prompt=input,
        echo=False,
        stop='\n'
    )

def create_question():
    messages = [{"role": "system", "content": "You are a system made to create a question based off of the prior conversation."}]

    i = 0
    while (i < len(context_array) - 1):
        messages[i] = {"role": "user", "content": context_array[i]}
        messages[i+1] = {"role": "assistant", "content": context_array[i+1]}
        i += 2

    messages[i] = {"role": "user", "content": context_array[i]} # Newest message provided by the user
    messages[i+1] = {"role": "user", "content": "Create a question based off the previous conversation we have had, or if there is only one previous question, turn it into a question if it is not already one."}

    openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "You are are a ."},
                {"role": "user", "content": "Who won the world series in 2020?"},
                {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                {"role": "user", "content": "Where was it played?"}
            ]
    )
    return ''