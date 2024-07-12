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
    end = time.time()
    
    output = output.replace("\n", "\\n")
    data = {'message': 'Completed', 'time_taken': end-start, 'suggestion': output, 'time' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
    requests.post('http://localhost:8000', json=data)
    
    return [
        types.CompletionItem(label="Completion Suggestion", insert_text=output, kind=types.CompletionItemKind.Text),

    ]
    


if __name__ == "__main__":
    server.start_io()

