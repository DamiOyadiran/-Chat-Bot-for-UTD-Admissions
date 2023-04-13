import pandas as pd, os, openai, sys, time

INIT_FILE_NAME = './formatted_data/data_set_full.csv'
INTERMEDIATE_FILE_NAME = './formatted_data/data_set_with_answers_full.csv'
FINAL_FILE_NAME = './formatted_data/data_set_with_embed_full.csv'

num_embed_get = 0

df= pd.read_csv(os.path.join(os.path.dirname(__file__), INIT_FILE_NAME))
print(df)

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
        return response['choices'][0]['text']
    except:
        return ""
    
def get_embedding(text: str, model: str="text-embedding-ada-002") -> list[float]:
    global num_embed_get
    if (num_embed_get % 60 == 0):
        print(f'sleep {num_embed_get / 60 + 1} started')
        time.sleep(60) # Getting around rate limiting :/
        print(f'sleep {num_embed_get / 60 + 1} completed')

    result = openai.Embedding.create(
      model=model,
      input=text
    )

    num_embed_get += 1

    return result["data"][0]["embedding"]

def compute_doc_embeddings(df: pd.DataFrame) -> dict[tuple[str, str], list[float]]:
    return {
        idx: get_embedding(r.content) for idx, r in df.iterrows()
    }

if __name__ == "__main__":
    #df['questions']= df.context.apply(get_questions)
    #df['answers']= df.apply(get_answers, axis=1)
    #df.to_csv(os.path.join(os.path.dirname(__file__), INTERMEDIATE_FILE_NAME)) # File name passed as argument

    df2 = pd.DataFrame.from_dict(compute_doc_embeddings(pd.read_csv(os.path.join(os.path.dirname(__file__), INTERMEDIATE_FILE_NAME))))
    df2 = pd.concat([df.filter(items=['topic', 'title']), df2.T], axis="columns")
    df2.to_csv(os.path.join(os.path.dirname(__file__), FINAL_FILE_NAME))