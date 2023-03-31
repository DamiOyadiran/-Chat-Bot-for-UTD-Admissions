import pandas as pd, os, openai, sys

df= pd.read_csv(os.path.join(os.path.dirname(__file__), './tabled_data_with_answers_2.csv'))

def get_questions(context):
    try:
        response = openai.Completion.create(
            engine = "davinci-instruct-beta-v3",
            prompt = f"Write questions based on the text below\n\nText: {context}\n\nQuestions:\n1.",
            temperature = 0.5,
            max_tokens = 100,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0,
            stop=["\n\n"]
        )
        print("finished step")
        return response['choices'][0]['text']
    except:
        return ""
    
def get_answers(row):
    try:
        response = openai.Completion.create(
            engine = "davinci-instruct-beta-v3",
            prompt = f"Write answer based on the text below\n\nText: {row.context}\n\nQuestions:\n{row.questions}\n\nAnswers:\n1.",
            temperature = 0.5,
            max_tokens = 200,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0,
            stop=["\n\n"]
        )
        print("finished step")
        return response['choices'][0]['text']
    except:
        return ""
    
def get_embedding(text: str, model: str="text-embedding-ada-002") -> list[float]:
    result = openai.Embedding.create(
      model=model,
      input=text
    )
    return result["data"][0]["embedding"]

if __name__ == "__main":
    df['questions']= df.context.apply(get_questions)
    df['answers']= df.apply(get_answers, axis=1)
    df["embedding"] = df.context.apply(lambda x: get_embedding(x, model="text-embedding-ada-002"))
    #print(df)
    df.to_csv(sys.argv[1]) # File name passed as argument