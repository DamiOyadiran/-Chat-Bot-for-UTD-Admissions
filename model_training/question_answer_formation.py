import pandas as pd, os, openai

df = pd.read_csv(os.path.join(os.path.dirname(__file__), './tabled_data.csv'))

df_filtered = df[df.topic == 'maintaining-aid']

def get_questions(context):
    try:
        response = openai.Completion.create(
            engine="davinci-instruct-beta-v3",
            prompt=f"Write questions based on the text below\n\nText: {context}\n\nQuestions:\n1.",
            temperature=0.5,
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"]
        )
        print("finished step")
        return response['choices'][0]['text']
    except:
        return ""
    
df_filtered['questions']= df.context.apply(get_questions)
print(df_filtered['questions'])

df_filtered.to_csv('model_training/tabled_data_with_answers.csv', index=False)