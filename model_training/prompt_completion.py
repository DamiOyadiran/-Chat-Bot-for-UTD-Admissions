import openai

def format(input):
    # Stuff done that we'll figure out to maximalize its accuracy for the model
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

def get_context(input):
    return ''