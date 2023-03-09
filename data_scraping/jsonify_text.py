import os, json

directory = '../results'

json_cont = { "input": "output" }

with open("unstructured_data_v3.jsonl", "a") as outfile:
    for filename in os.listdir(directory):
        file = open(os.path.join(directory, filename), 'r')
        file_cont = file.read()

        if (len(file_cont) < 2000):
            
            continue

        i = 0
        while (len(file_cont) - (i * 1000) > 1000):
            json_cont = {"prompt": file_cont[i*1000:i*1000+500] + " ->" }
            json_cont["completion"] = file_cont[i*1000+500:i*1000+1000]
            i+=1

            json_object = json.dumps(json_cont, indent=1)
            outfile.write(json_object)
            outfile.write('\n')