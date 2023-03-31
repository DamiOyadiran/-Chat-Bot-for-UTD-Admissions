import openai, embedded_context

class ChatBot:
    def __init__(self, max_context = 4):
        self.max_context = max_context * 2
        self.context_array = []

    def format(self, input):
        # Stuff done that we'll figure out to maximalize its accuracy for the model

        # Remove last question-answer pairing from the context
        if (len(self.context_array) > self.max_context):
            self.context_array = self.context_array[2:]
        self.context_array.append(input)

        model_completion_prompt = self.create_question()
        print(model_completion_prompt)

        try:
            model_completion_prompt = embedded_context.find_context(input) + "\n\n" + input
        except:
            print("Context failure")
        
        output = self.model_completion(model_completion_prompt)
        self.context_array.append(output)
        
        return output

    def model_completion(self, input):
        return openai.Completion.create(
            model='ada:ft-cs-chatbot-t5-2023-03-09-03-56-59',
            prompt=input,
            echo=False,
            stop='\n'
        )['choices'][0]['text'].strip(" \n")

    def create_question(self):
        messages = [{"role": "system", "content": "You are a system made to create a question based off of the prior conversation."}]

        i = 0
        while (i < len(self.context_array) - 1):
            messages.append({"role": "user", "content": self.context_array[i]})
            messages.append({"role": "assistant", "content": self.context_array[i+1]})
            i += 2

        messages.append({"role": "user", "content": self.context_array[i]}) # Newest message provided by the user
        messages.append({"role": "user", "content": "Create a question based off the previous conversation we have had, or if there is only one previous question, turn it into a question if it is not already one."})

        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )['choices'][0]['message']['content']

# Testing without util of front-end
if __name__ == "__main__":
    q_a = ChatBot(6)
    while (True):
        user_prompt = input("Provide user input: ")
        if (user_prompt == "exit"):
            break

        print(q_a.format(user_prompt))