import ollama
import time
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
    y_test = torch.tensor(y_test, dtype=torch.int64)"""

# def function that gets the plain text of a file from the dictionary
def get_suggestion(lines, line, character):
    # Place fim hole at the cursor position
    print("\n".join(lines))
    lines[line] = lines[line][:character] + "<｜fim▁hole｜>" + lines[line][character:]
    text = "\n".join(lines)
    content = '<｜fim▁begin｜>' + text + '<｜fim▁end｜>'
    print('<=====================>')
    print(content)
    print('<=====================>')
    response = ollama.chat(model='deepseek-coder:base', 
        messages=[{
        'role': 'user',
        'content': content,
      },])
    return response["message"]["content"]

suggestion = get_suggestion(content.split("\n"), 12, 5)
print()
print('SUGGESTION:')
print(suggestion)
