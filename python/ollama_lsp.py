from pygls.server import LanguageServer
from lsprotocol import types
#import requests
from completion_engine import CompletionEngine
import re
import asyncio

# TODO: Add logging
# TODO: update so that on change events like clear are not held up by on going completions (maybe client side)
# TODO: add async for onChange


# ------------------ LSP Server ----------------
def send_log(message, line, col, file="f/na"): 
    #headers = {'Content-type': 'application/json'}
    #requests.post("http://localhost:8000",headers=headers, json={"message": message, "file": file.split('/')[-1], "line" : line, "col" : col})
    return
async def async_generator_wrapper(generator):
    for item in generator:
        yield item

class OllamaServer:

    def __init__(self):
        self.server = LanguageServer("example-server", "v0.2")
        self.engine = None # Wait for initialization 
        self.curr_suggestion = {'line' : 0, 'character' : 0, 'suggestion': ''}
        self.cancel_suggestion = False
        self.debounce_time = 0.5  # Debounce time in seconds
        self.last_completion_request = None
        self.debounce_task = None
        self.register_features()
    
    def register_features(self):
        @self.server.feature(types.INITIALIZE)
        def initialize(params: types.InitializeParams):
            return self.on_initialize(params)
        
        @self.server.feature(types.TEXT_DOCUMENT_COMPLETION)
        def completions(params: types.CompletionParams):
            return []

        @self.server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
        def change(params: types.DidChangeTextDocumentParams):
            return self.on_change(params)


    def on_initialize(self, params: types.InitializeParams):
        headers = {'Content-type': 'application/json'}
        send_log(f"Initialized, Opts: {params.initialization_options}", 0, 0)
        init_options = params.initialization_options

        self.engine = CompletionEngine(init_options.get('model_name', "deepseek-coder:base"), init_options.get("ollama_url", None), options=init_options.get('ollama_model_opts', {}))
        self.stream_suggestion = params.initialization_options.get('stream_suggestion', False)

        return {
            "capabilities": {
                "textDocumentSync": types.TextDocumentSyncKind.Incremental,
                "completionProvider": {
                    "resolveProvider": True,
                    "triggerCharacters": [' ']
                }
            }
        }

    def debounce_completion(self, params: types.CompletionParams):
        self.last_completion_request = params
        if self.debounce_task:
            self.debounce_task.cancel()
        self.debounce_task = asyncio.create_task(self.handle_debounce())
        return []

    async def handle_debounce(self):
        await asyncio.sleep(self.debounce_time)
        if self.last_completion_request:
            params = self.last_completion_request
            self.last_completion_request = None
            await self.on_completion(params)

    async def on_completion(self, params: types.CompletionParams):

        document = self.server.workspace.get_text_document(params.text_document.uri)
        lines = document.lines
        suggestion_stream = async_generator_wrapper(self.engine.complete(lines, params.position.line, params.position.character))

        self.curr_suggestion = {'line' : params.position.line + 1, 'character' : params.position.character, 'suggestion': ''}
        timing_str = ''

        async for chunk in suggestion_stream:
            if self.cancel_suggestion:
                self.cancel_suggestion = False
                return []

            self.curr_suggestion['suggestion'] += chunk['response']
            if 'context' in chunk:
                total_duration = chunk['total_duration'] / 10**9
                load_duration = chunk['load_duration'] / 10**9
                prompt_eval_duration = chunk['prompt_eval_duration'] / 10**9
                eval_count = chunk['eval_count']
                eval_duration = chunk['eval_duration'] / 10**9
                timing_str = f"""
                    Total duration: {total_duration},
                    Load duration: {load_duration},
                    Prompt eval duration: {prompt_eval_duration},
                    Eval count: {eval_count},
                    Eval duration: {eval_duration}"""
            if self.stream_suggestion:
                self.send_suggestion(self.curr_suggestion['suggestion'],
                                     self.curr_suggestion['line'],
                                     self.curr_suggestion['character'],
                                     suggestion_type='stream')
            
        self.send_suggestion(self.strip_suggestion(self.curr_suggestion['suggestion']),
                             self.curr_suggestion['line'], self.curr_suggestion['character'],
                             suggestion_type='completion')
        
        send_log(f"{timing_str}: {self.curr_suggestion['suggestion']}",
                   params.position.line,
                   params.position.character,
                   params.text_document.uri)
        
        return [] 
         
    def on_change(self, params: types.DidChangeTextDocumentParams):
        change = params.content_changes[0]
        #send_log(f"Change: {change.text}", change.range.start.line, change.range.start.character, params.text_document.uri)

        lines = self.server.workspace.get_text_document(params.text_document.uri).lines
        line = lines[change.range.start.line][change.range.start.character + 1:]
        contains_non_whitespace = bool(re.search(r'[^\s]', line))

        if contains_non_whitespace:
            return

        if change.text == self.curr_suggestion['suggestion'][0:len(change.text)] and len(change.text) > 0: 
            self.curr_suggestion['suggestion'] = self.curr_suggestion['suggestion'][len(change.text):]
            self.curr_suggestion['character'] += len(change.text)
            self.send_suggestion(self.curr_suggestion['suggestion'],
                                 self.curr_suggestion['line'],
                                 self.curr_suggestion['character'],
                                 suggestion_type='fill_suggestion')
            return
        else:
            self.curr_suggestion = {'line' : 1, 'character' : 0, 'suggestion': ''}
            self.clear_suggestion()
            # Trigger a new completion
            position = types.Position(line=change.range.end.line, character=change.range.end.character + 1)
            completion_params = types.CompletionParams(
                text_document=params.text_document,
                position=position,
                context=types.CompletionContext(trigger_kind=types.CompletionTriggerKind.Invoked)
            )
            # Here we can add logic for when to trigger a completion, 
            # For now, only dont trigger if the change is a deletion
            if len(change.text) == 0:
                return
            self.debounce_completion(completion_params)
        return
            
    def clear_suggestion(self):
        self.server.send_notification('$/clearSuggestion',{'message' : "clear current"})

    def send_suggestion(self, suggestion, line, col, suggestion_type='miscellaneous'):
        self.server.send_notification('$/tokenStream', {
            'line' : line,
            'character' : col,
            'completion': {
                'total': suggestion,
                'type' : suggestion_type,
            }}
            )


    def strip_suggestion(self, text):
      stripped_text = text.rstrip('\n')
      return re.sub(r'\n{2,}', '\n', stripped_text)

    
    def start(self):
        self.server.start_io()

if __name__ == "__main__":
    server = OllamaServer()
    server.start()


