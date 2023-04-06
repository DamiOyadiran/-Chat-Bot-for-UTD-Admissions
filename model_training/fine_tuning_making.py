from sklearn.model_selection import train_test_split
import prompt_completion, pandas as pd, os, embedded_context

DF = pd.read_csv(os.path.join(os.path.dirname(__file__), 'tabled_data_with_answers_2.csv'))

train_df, test_df = train_test_split(DF, test_size=0.2, random_state=42)

def create_tuning_set(df, discrim=False):
    rows = []

    for row in df.iterrows():
        for q, a in zip(("1." + row.questions).split('\n'), ("1." + row.answers).split('\n')):
            if discrim:
                rows.append({"prompt":f"{row.context}\nQuestion: {q[2:].strip()}\n Related:", "completion":f" yes"})
            else:
                rows.append({"prompt":f"{row.context}\nQuestion: {q[2:].strip()}\nAnswer:", "completion":f" {a[2:].strip()}"})

        for q in ("1." + row.questions).split('\n'):
            for j in range(3):
                random_context = ""
                if j == 0:
                    subset = df[(df.title == row.title) & (df.context != row.context)]
                    if len(subset) < 1:
                            continue
                    random_context = subset.sample(1).iloc[0].context
                elif j == 1:
                    random_context = 1
                else:
                    continue

            if discrim:
                rows.append({"prompt":f"{random_context}\nQuestion: {q[2:].strip()}\n Related:", "completion":f" no"})
            else:
                rows.append({"prompt":f"{random_context}\nQuestion: {q[2:].strip()}\nAnswer:", "completion":f" No appropriate context found."})