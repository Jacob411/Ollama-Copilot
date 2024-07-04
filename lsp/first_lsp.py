from pygls.server import LanguageServer
from lsprotocol import types
import time
import ollama
import requests

# Print hello world


server = LanguageServer("example-server", "v0.2")
with open("log.txt", "w") as f:
    f.write("Starting LSP")


client = ollama.Client("http://localhost:11434")

@server.feature(types.TEXT_DOCUMENT_COMPLETION)
def completions(params: types.CompletionParams):
    start = time.time()
    # Send log to the server at port 8000
    response = requests.post("http://localhost:8000", data={"value": "Completion requested"},headers={"Content-Type": "application/json"}, verify=False)

    document = server.workspace.get_text_document(params.text_document.uri)
       #measure time taken to get text of document
    #get the text of the document
    lines = document.lines
    with open('log.txt', 'a') as f:
        f.write(f'completion requested {response}\n')
    # Get suggestion    
    suggestion = get_suggestion(lines, params.position.line, params.position.character)
    end = time.time()
    with open("log.txt", "a") as f:
        f.write(f"Time: {end - start}\n, Suggestion: {suggestion}\n")
    return [
        types.CompletionItem(label=suggestion, kind=types.CompletionItemKind.Text),
    ]

# def function that gets the plain text of a file from the dictionary
def get_suggestion(lines, line, character):
    # Place fim hole at the cursor position
    lines[line] = lines[line][:character] + "<｜fim▁hole｜>" + lines[line][character:]
    text = "\n".join(lines)
    content = '<｜fim▁begin｜>' + text + '<｜fim▁end｜>'
    response = client.chat(model='deepseek-coder:base', 
        messages=[{
        'role': 'user',
        'content': content,
      },])
    return response["message"]["content"]

if __name__ == "__main__":
    server.start_io()
