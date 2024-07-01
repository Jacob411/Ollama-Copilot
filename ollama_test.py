import ollama
import time
content = """<｜fim▁begin｜>#utils.py
import torch
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def load_data():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    # Standardize the data
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = <｜fim▁hole｜>
    # Convert numpy data to PyTorch tensors
    X_train = torch.tensor(X_train, dtype=torch.float32)
    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_train = torch.tensor(y_train, dtype=torch.int64)
    y_test = torch.tensor(y_test, dtype=torch.int64)
<｜fim▁end｜>"""
print(content)
print("Response:")
start = time.time()
response = ollama.chat(model='deepseek-coder:base', 
    messages=[
  {
    'role': 'user',
    'content': content,
  },
])
print("Time taken:", time.time() - start)
print(content + response["message"]["content"])
print(response)
