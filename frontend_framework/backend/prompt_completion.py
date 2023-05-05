import openai, backend.embedded_context as embedded_context, os, pandas as pd

MAX_SEC_LEN = 1000
SEPARATOR = "\n* "

DF = pd.read_csv(os.path.join(os.path.dirname(__file__), 'formatted_data\\data_set_with_answers_full.csv'))

COMPLETION_MODEL = "curie:ft-utd-senior-design-project-2023-04-15-03-22-09"
DISCRIM_MODEL = "ada:ft-utd-senior-design-project-2023-04-15-03-04-13"

SORRY_MESSAGE = "Sorry, this Chatbot isn't equipped to answer this question. Make sure your question is specifically defined and about financial aid at UT Dallas."

def format(input):
    input += '?' if input[-1] != '?' else ''

    # Grab context that best matches the input w/ embedding library
    top_context = embedded_context.find_context(input)[0]

    document_section = DF.loc[DF['title'] == top_context[1][1]].values

    context = document_section[0][5].replace("\n", " ")
    context = context[0:1500] if len(context) > 1500 else context

    # Construct the prompt to feed into the models, which is further modified at each file
    header = """Provide a single answer. Do not repeat the question.\n\n"""
    model_completion_prompt = context + "\nQuestion: " + input + "\n"

    # Loop allows multiple attempts at answering question in case the first try fails
    # Variability of responses
    i = 0
    while (i < 1):
        # Check with discriminator model if the context appropriately answers the question
        if (check_discrim(model_completion_prompt + "Related:")):
            # Produce output from completion model
            output = model_completion(header + model_completion_prompt + "Answer:")
            if (output['choices'][0]["finish_reason"] == 'stop' and output['choices'][0]['text'].replace(" ", "") != ""):
                return output['choices'][0]['text'][1:] # Returns model output with the starting space removed
            
            i+=1
        else:
            return SORRY_MESSAGE + '*'
    
    return SORRY_MESSAGE

def model_completion(input):
    return openai.Completion.create(
        model=COMPLETION_MODEL,
        prompt=input,
        echo=False,
        max_tokens=200,
        stop=["Question", "\n\n"],
        temperature = 0.7 # Lower variablity -> more objective responses
    )

def check_discrim(input):
    result = openai.Completion.create(
        model=DISCRIM_MODEL,
        prompt=input,
        echo=False,
        max_tokens=1,
        logprobs = 10
    )
    # logprobs uses discrim model to determine what the most appropriate response to the question is
    logprobs = result['choices'][0]['logprobs']['top_logprobs'][0]
    yes = logprobs[' yes'] if ' yes' in logprobs else -10
    no = logprobs[' no'] if ' no' in logprobs else -10

    return (yes > no)

# Testing without util of front-end
if __name__ == "__main__":
    while (True):
        user_prompt = input("Provide user input: ")
        if (user_prompt == "exit"):
            break

        print(format(user_prompt))