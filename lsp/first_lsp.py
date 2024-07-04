from pygls.server import LanguageServer
from lsprotocol import types
import time
import ollama
import requests
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# Print hello world

server = LanguageServer("example-server", "v0.2")
p
client = ollama.Client("http://localhost:11434")

@server.feature(types.TEXT_DOCUMENT_COMPLETION)
def completions(params: types.CompletionParams):
    start = time.time()
    # Send log to the server at port 8000
    response = requests.post("http://localhost:8000", data={"message": "Completion requested", "line": params.position.line, "character": params.position.character})


    document = server.workspace.get_text_document(params.text_document.uri)
       #measure time taken to get text of document
    #get the text of the document
    lines = document.lines
 
    # Get suggestion    
    suggestion = get_suggestion_with_timeout(lines, params.position.line, params.position.character, 5)
    end = time.time()
    
    data = {'message': 'Completed', 'time_taken': end-start, 'suggestion': suggestion}
    response = requests.post('http://localhost:8000', json=data)

    return [
        types.CompletionItem(label=suggestion, kind=types.CompletionItemKind.Text),
    ]

# def function that gets the plain text of a file from the dictionary
def get_suggestion(lines, line, character):
    lines_above = max(0, line - 5)  # Ensure not to go negative
    pre_cursor_text = "\n".join(lines[lines_above:line]) + "\n" + lines[line][:character]
    # Place fim hole at the cursor position
    lines[line] = lines[line][:character] + "<｜fim▁hole｜>" + lines[line][character:]
    text = "\n".join(lines)
    content = '<｜fim▁begin｜>' + text + '<｜fim▁end｜>'

    response = client.chat(model='custom-deepseek', 
        messages=[{
        'role': 'user',
        'content': pre_cursor_text,
      },])
    return response["message"]["content"]


def get_suggestion_with_timeout(lines, line, character, timeout_duration):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(get_suggestion, lines, line, character)
        try:
            suggestion = future.result(timeout=timeout_duration)
            return suggestion
        except TimeoutError:
            response = requests.post('http://localhost:8000', json={'message' : 'TIMED OUT'})
            return f"No suggestion, for line: {line}, character: {character}"
if __name__ == "__main__":
    server.start_io()
