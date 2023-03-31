import pandas as pd, os, openai, sys

df= pd.read_csv(os.path.join(os.path.dirname(__file__), 'model_training/tabled_data_with_answers_2.csv'))

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
    print('a')
    return result["data"][0]["embedding"]

def compute_doc_embeddings(df: pd.DataFrame) -> dict[tuple[str, str], list[float]]:
    """
    Create an embedding for each row in the dataframe using the OpenAI Embeddings API.
    
    Return a dictionary that maps between each embedding vector and the index of the row that it corresponds to.
    """
    return {
        idx: get_embedding(r.content) for idx, r in df.iterrows()
    }

if __name__ == "__main__":
    #df['questions']= df.context.apply(get_questions)
    #df['answers']= df.apply(get_answers, axis=1)
    pass
    #df2.to_csv(sys.argv[1]) # File name passed as argument

df2 = pd.DataFrame.from_dict(compute_doc_embeddings(df))
df2 = pd.concat([df.filter(items=['topic', 'title']), df2.T], axis="columns")
    #print(df)
df2.to_csv('./data_set_with_embed.csv')