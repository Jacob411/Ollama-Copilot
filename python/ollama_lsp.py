from pygls.server import LanguageServer
from lsprotocol import types
import time
import ollama
import requests
from completion_engine import CompletionEngine
# TODO: Get suggestion to appear in editor always.
# ------------------ LSP Server ----------------

class OllamaServer:

    def __init__(self):
        self.server = LanguageServer("example-server", "v0.2")
        self.engine = CompletionEngine("deepseek-coder:base", {"stop": ["\n"], "num_predict": 40, "temperature": 0.4})
        self.curr_suggestion = {'line' : 0, 'character' : 0, 'suggestion': ''}
        self.register_features()
    
    def register_features(self):
        @self.server.feature(types.INITIALIZE)
        def initialize(params: types.InitializeParams):
            return self.on_initialize(params)
        
        @self.server.feature(types.TEXT_DOCUMENT_COMPLETION)
        def completions(params: types.CompletionParams):
            return self.on_completion(params)
        
        @self.server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
        def change(params: types.DidChangeTextDocumentParams):
            return self.on_change(params)

    def on_initialize(self, params: types.InitializeParams):
        headers = {'Content-type': 'application/json'}
        requests.post("http://localhost:8000",headers=headers, json={"message": "Initialized the ollama LSP server", "time":  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})
        return {
            "capabilities": {
                "textDocumentSync": types.TextDocumentSyncKind.Incremental,
                "completionProvider": {
                    "resolveProvider": True,
                    "triggerCharacters": ["."]
                }
            }
        }

    def on_completion(self, params: types.CompletionParams):
        start = time.time()
        headers = {'Content-type': 'application/json'}
        requests.post("http://localhost:8000",headers=headers, json={"message": "Completion requested", "file" : params.text_document.uri, "line": params.position.line, "character": params.position.character })
        document = self.server.workspace.get_text_document(params.text_document.uri)
        lines = document.lines
        
        suggestion_stream = self.engine.complete(lines, params.position.line, params.position.character)
        self.curr_suggestion = {'line' : params.position.line + 1, 'character' : params.position.character, 'suggestion': ''}
        output = ""
        for chunk in suggestion_stream:
            self.curr_suggestion['suggestion'] += chunk['message']['content']
            self.server.send_notification('$/tokenStream', {
                'line' : self.curr_suggestion['line'],
                'character' : self.curr_suggestion['character'],
                'completion': {
                    'total': self.curr_suggestion['suggestion'],
                    'type' : 'stream',
                }
            })
        end = time.time()
        
        data = {'message': 'Completed', 'time_taken': end-start, 'suggestion': self.curr_suggestion['suggestion'], 'line': params.position.line, 'character': params.position.character}
        requests.post('http://localhost:8000', headers=headers, json=data)
        
        return [types.CompletionItem(label="Completion Suggestion", insert_text=output, kind=types.CompletionItemKind.Text),]
         
    def on_change(self, params: types.DidChangeTextDocumentParams):
        change = params.content_changes[0]
        if change.text == self.curr_suggestion['suggestion'][0:len(change.text)] and len(change.text) > 0: 
            self.curr_suggestion['suggestion'] = self.curr_suggestion['suggestion'][len(change.text):]
            self.curr_suggestion['character'] += len(change.text)
            self.server.send_notification('$/tokenStream', {
                'line' : self.curr_suggestion['line'],
                'character' : self.curr_suggestion['character'] + len(change.text) - 1,
                'completion': {
                    'total': self.curr_suggestion['suggestion'],
                    'type' : 'fill_suggestion',
                }
            })
            return
        else:
            self.curr_suggestion = {'line' : 1, 'character' : 0, 'suggestion': ''}
            self.server.send_notification('$/tokenStream', {
                'line' : 1,
                'character' : 0,
                'completion': {
                    'total': '',
                    'type' : 'clear_suggestion',
                }
            })
            return
            
    
    def start(self):
        self.server.start_io()

if __name__ == "__main__":
    server = OllamaServer()
    server.start()


