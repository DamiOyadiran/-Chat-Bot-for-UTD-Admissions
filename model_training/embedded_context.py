import pandas as pd, numpy as np, openai

embedding_file_name = './data_set_with embed.csv'

def get_embedding(text: str, model: str="text-embedding-ada-002") -> list[float]:
    result = openai.Embedding.create(
      model=model,
      input=text
    )
    return result["data"][0]["embedding"]

def load_embeddings(fname: str) -> dict[tuple[str, str], list[float]]:
    
    df = pd.read_csv(fname, header=0)
    max_dim = max([int(c) for c in df.columns if c != "topic" and c != "title"])
    return {
           (r.topic, r.title): [r[str(i)] for i in range(max_dim + 1)] for _, r in df.iterrows()
    }

def vect_similarity(x, y):
    return np.dot(np.array(x), np.array(y))

def order_documents_by_similarity(query, contexts):
    query_embedding = get_embedding(query)

    document_similarities = sorted([
        (vect_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ], reverse=True)

    return document_similarities

def find_context(query):
    order_documents_by_similarity(query, load_embeddings(embedding_file_name))

    return ""