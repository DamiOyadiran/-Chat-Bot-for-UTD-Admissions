import os, json, jsonlines as jsl

directory = '../results'

json_cont = { "input": "output" }, {"input2": "output2"}, {"input2": "output2"}

print(type(json_cont))


for filename in os.listdir(directory):
    file = open(os.path.join(directory, filename), 'r')
    file_cont = file.read()

    if (len(file_cont) < 2000):
        
        continue

    i = 0
    while (len(file_cont) - (i * 1000) > 1000):
        json_cont += ({"prompt": file_cont[i*1000:i*1000+500] + " ->", "completion": file_cont[i*1000+500:i*1000+1000]}, )
        i+=1

with jsl.open("unstructured_data_v4.jsonl", "w") as outfile:
        outfile.write_all(json_cont)