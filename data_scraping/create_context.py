import pandas as pd, os

from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
directory = 'C:/Users/Brooks/Documents/webscraping_test/Chat-Bot-for-UTD-Admissions/model_training/context'
token_limit = 500

outputs = []

for filename in os.listdir(directory):
    file = open(os.path.join(directory, filename), 'r')
    file_cont = file.read()

    tokens = tokenizer.encode(file_cont)
    token_cnt = len(tokens)

    i = 0
    file_struct = filename.split('.')[0].split('_')
    while i < token_cnt:
        reached_end = (i + token_limit > token_cnt)

        text_output = tokenizer.decode(tokens[i:]) if reached_end else tokenizer.decode(tokens[i:i+token_cnt])
        tokens_used = token_cnt - i if reached_end else 500

        outputs.append((file_struct[1], ' '.join(file_struct[1:]) + ' ' + str(int(i / 500) + 1), text_output, tokens_used))
        i+=500

df = pd.DataFrame(outputs, columns=["topic", "title", "content", "tokens"])
df = df[df.tokens>10]
df = df.drop_duplicates(['topic','title'])

df["context"] = df.title + "\n" + df.content

df.to_csv('model_training/tabled_data.csv', index=False)
