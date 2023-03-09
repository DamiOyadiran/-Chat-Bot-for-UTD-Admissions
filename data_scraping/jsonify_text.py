import os, json

directory = '../results'

json_cont = { "input": "output" }

for filename in os.listdir(directory):
    file = open(os.path.join(directory, filename), 'r')
    file_cont = file.read()

    if (len(file_cont) < 2000):
        
        continue

    i = 0
    while (len(file_cont) - (i * 1000) > 1000):
        json_cont[file_cont[i*1000:i*1000+500] + " =>"] = file_cont[i*1000+500:i*1000+1000]
        i+=1
    #json_cont[file_cont[i*1000:round((i*1000 + len(file_cont))/2)] + " =>"] = file_cont[round((i*1000 + len(file_cont))/2):]

json_object = json.dumps(json_cont, indent=1)

with open("unstructured_data.json", "w") as outfile:
    outfile.write(json_object)