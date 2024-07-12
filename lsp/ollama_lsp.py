from pygls.server import LanguageServer
from lsprotocol import types
import time
import ollama
import requests
from completion_engine import CompletionEngine
# TODO: Get suggestion to appear in editor always.
# ------------------ LSP Server ----------------


server = LanguageServer("example-server", "v0.2")
engine = CompletionEngine("deepseek-coder:base", {"stop" : ["\n"], "num_predict" :40, "temperature" : 0.4})



@server.feature(types.TEXT_DOCUMENT_COMPLETION)
def completions(params: types.CompletionParams):

    start = time.time()
    requests.post("http://localhost:8000", data={"message": "Completion requested", "file" : params.text_document.uri, "line": params.position.line, "character": params.position.character, "time":  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
    document = server.workspace.get_text_document(params.text_document.uri)
    lines = document.lines
    
    suggestion_stream = engine.complete(lines, params.position.line - 1, params.position.character)
    output = ""
    for chunk in suggestion_stream:
        output += chunk['message']['content']
        server.send_notification('$/tokenStream', {
            'line' : params.position.line,
            'character' : params.position.character,
            'completion': {
                'total': output,
                'curr_token': chunk['message']['content'],
                'percentage': 0,
            }
        })
        # token = time.time()
        # server.send_notification('$/tokenStream', types.ProgressParams(
        #     token=token,
        #     value=types.WorkDoneProgressBegin(
        #         title=chunk['message']['content'],
        #         percentage=0,
        #         message=output
        #     )
        # ))
        #

    end = time.time()
    
    output = output.replace("\n", "\\n")
    data = {'message': 'Completed', 'time_taken': end-start, 'suggestion': output, 'time' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
    requests.post('http://localhost:8000', json=data)
    
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
    stream = client.chat(
        model= model_name, 
        messages=[{
        'role': 'user',
        'content': pre_cursor_text,
        }],                 
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

