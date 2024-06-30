import ollama
response = ollama.chat(model='short_code', 
    messages=[
  {
    'role': 'user',
    'content': 'def fibonacci(',
  },
])
print(response['message']['content'])
