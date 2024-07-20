import ollama
import time

content1 = """#utils.py
import torch
# check if cuda is available"""

content = """#utils.py
import torch
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def load_data():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    # Print out the shape of the data

    # Standardize the data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 
    # Convert numpy data to PyTorch tensors
    X_train = torch.tensor(X_train, dtype=torch.float32)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.int64)
    y_test = torch.tensor(y_test, dtype=torch.int64)
    # print length of y_test"""


#content = place_fim(content.split("\n"), 12, 0)
client = ollama.Client(host='http://localhost:11434')
models = [model['name'] for model in client.list()['models']]
for i, model in enumerate(models):
    print(f'{i}: {model}')
model = input("Enter the which num to use: ")
model = models[int(model)]

stream = client.generate(
    model=model, 
    prompt=content,
    options = {
            "num_predict" :40,
    },
    stream=True
)


output = ''

for chunk in stream:
    print(chunk)
    output += chunk['response']
    #print(chunk['response'], end='', flush=True)
print(output)
# print("\nTime taken: ", time.time()-start)
# print('<===========================>')

# Run the same prompt through ten times, time it and print the average time 
start = time.time()
for i in range(10):
    mid_time = time.time()
    stream = client.generate(
        model=model, 
        prompt=content,
        options = {
            "num_predict" :40,
        },
        stream=True
    )
    for chunk in stream:
        if 'context' in chunk:
            # print the times
            total_duration = chunk['total_duration'] / 10**9
            load_duration = chunk['load_duration'] / 10**9
            prompt_eval_duration = chunk['prompt_eval_duration'] / 10**9
            eval_count = chunk['eval_count']
            eval_duration = chunk['eval_duration'] / 10**9
            print(f"Total duration: {total_duration}, Load duration: {load_duration},  Prompt eval duration: {prompt_eval_duration}, Eval count: {eval_count}, Eval duration: {eval_duration}")
            print()

    print("Time taken: ", time.time()-mid_time)
print("Average time taken: ", (time.time()-start)/10)





