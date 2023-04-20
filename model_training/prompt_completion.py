import openai, embedded_context, os, pandas as pd

MAX_SEC_LEN = 1000
SEPARATOR = "\n* "

DF = pd.read_csv(os.path.join(os.path.dirname(__file__), 'formatted_data\\data_set_with_answers_full.csv'))

COMPLETION_MODEL = "curie:ft-utd-senior-design-project-2023-04-15-03-22-09"
DISCRIM_MODEL = "ada:ft-utd-senior-design-project-2023-04-15-03-04-13"

def format(input):
    # Stuff done that we'll figure out to maximalize its accuracy for the model

    # Remove last question-answer pairing from the context
    #if (len(context_array) > max_context):
        #context_array = context_array[2:]
    #context_array.append(input)

   # model_completion_prompt = create_question()

    top_context = embedded_context.find_context(input)[0]

    #chosen_sections = []
    sects_len = 0
    sects_indices = []

    document_section = DF.loc[DF['title'] == top_context[1][1]].values

    #for _, section_index in top_context:
    #    document_section = DF.loc[DF['title'] == section_index[1]].values
    #    sects_len += document_section[0][3]
    #    if sects_len > MAX_SEC_LEN:
    #        break

    #    chosen_sections.append(SEPARATOR + document_section[0][2].replace("\n", " "))
    #    sects_indices.append(str(section_index))

    model_completion_prompt = document_section[0][3].replace("\n", " ") + "\nQuestion: " + input + "\nAnswer: "
    
    while (1):
        if (check_discrim(model_completion_prompt)):
            output = model_completion(model_completion_prompt)
            if (output['choices'][0]["finish_reason"] == 'stop' and output['choices'][0]['text'].replace(" ", "") != ""):
                print('owned')
                break
            return output['choices'][0]['text']
        else:
            return "No context found according to discrim."

def model_completion(input):
    return openai.Completion.create(
        model=COMPLETION_MODEL,
        prompt=input,
        echo=False,
        max_tokens=200
    )

def check_discrim(input):
    logprobs = openai.Completion.create(
        model=DISCRIM_MODEL,
        prompt=input,
        echo=False,
        max_tokens=1,
        logprobs = 10
    )['choices'][0]['logprobs']['top_logprobs'][0]
    print(logprobs)
    yes = logprobs[' yes'] if ' yes' in logprobs else -100
    no = logprobs[' no'] if ' no' in logprobs else -100
    print (f' {yes} {no}')
    return (yes > no)

def create_question(context_array):
    messages = [{"role": "system", "content": "You are a system made to create a question based off of the prior conversation."}]

    i = 0
    while (i < len(context_array) - 1):
        messages.append({"role": "user", "content": context_array[i]})
        messages.append({"role": "assistant", "content": context_array[i+1]})
        i += 2

    messages.append({"role": "user", "content": context_array[i]}) # Newest message provided by the user
    messages.append({"role": "user", "content": "Create a question based off the previous conversation we have had, or if there is only one previous question, turn it into a question if it is not already one."})

    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )['choices'][0]['message']['content']

# Testing without util of front-end
if __name__ == "__main__":
    while (True):
        user_prompt = input("Provide user input: ")
        if (user_prompt == "exit"):
            break

        print(format(user_prompt))