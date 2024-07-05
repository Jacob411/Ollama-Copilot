from pygls.server import LanguageServer
from lsprotocol import types
import time
import ollama
import requests
# TODO: Get suggestion to appear in editor always.
# ------------------ LSP Server ----------------
# 


server = LanguageServer("example-server", "v0.2")
client = ollama.Client("http://localhost:11434")
@server.feature(types.TEXT_DOCUMENT_COMPLETION)
def completions(params: types.CompletionParams):
    start = time.time()
    requests.post("http://localhost:8000", data={"message": "Completion requested", "line": params.position.line, "character": params.position.character, "time":  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
    document = server.workspace.get_text_document(params.text_document.uri)
    #get the text of the document
    lines = document.lines
    # Get suggestion    
    suggestion_stream = get_suggestion(lines, params.position.line, params.position.character)
    output = ""
    for chunk in suggestion_stream:
        # if len(output) > 30:
        #     break
        output += chunk['message']['content']
    end = time.time()
    
    output = output.replace("\n", "\\n")
    data = {'message': 'Completed', 'time_taken': end-start, 'suggestion': output, 'time' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
    requests.post('http://localhost:8000', json=data)
    
    
    # Create a text edit to apply to the doc
    text_edit = types.TextEdit(range=types.Range(start=params.position, end=params.position), new_text=output)
    
    return [
        types.CompletionItem(label="Completion Suggestion", insert_text=output, kind=types.CompletionItemKind.Text),
    ]
    

# def function that gets the plain text of a file from the dictionary
def get_suggestion(lines, line, character):
    lines_above = max(0, line - 5)  # Ensure not to go negative
    pre_cursor_text = "\n".join(lines[:line]) + "\n" + lines[line][:character]
    # Place fim hole at the cursor position
    lines[line] = lines[line][:character] + "<｜fim▁hole｜>" + lines[line][character:]
    text = "\n".join(lines)
    content = '<｜fim▁begin｜>' + text + '<｜fim▁end｜>'
    stream = client.chat(model='custom-deepseek', 
        messages=[{
        'role': 'user',
        'content': pre_cursor_text,
      },
    ],
                         
    stream=True,
    options = {
        "stop" : ["\n"],
        "num_predict" :40,
        "temperature" : 0.4
    }
    )
    return stream



if __name__ == "__main__":
    server.start_io()
