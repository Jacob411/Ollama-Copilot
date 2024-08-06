import ollama
from sklearn.metrics.pairwise import cosine_similarity

models = [model['name'] for model in ollama.list()['models']]
for i, model in enumerate(models):
    print(f'{i}: {model}')
model = input("Enter the which num to use: ")
model = models[int(model)]

default_input = "Hello"
input_text1 = input("Enter the input text1: ")
input_text2 = input("Enter the input text2: ")

embedding1 = ollama.embeddings(
        model=model,
        prompt=input_text1
    )
embedding2 = ollama.embeddings(
        model=model,
        prompt=input_text2
    )

# Calculate the cosine similarity between the two embeddings
cosine_similarity = cosine_similarity(embedding1['embedding'], embedding2['embedding'])


print(f"The cosine similarity between the two embeddings is: {cosine_similarity[0][0]}")
print('<===========================>')
print(cosine_similarity)


