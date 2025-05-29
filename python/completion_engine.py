import ollama
from ollama import generate
class CompletionEngine:
    def __init__(self, model : str, client_url="http://localhost:11434", options = {}):
        self.model = model
        self.client = ollama.Client(client_url)
        self.options = options

    def complete(self, lines, line, character):
        pre_cursor_text = "\n".join(lines[:line]) + "\n" + lines[line][:character]
        return self.client.generate(
            model= self.model,
            prompt = pre_cursor_text,
            stream=True,
            options = self.options 
        )
    
    def fim_complete(self, lines, line, character):
        lines[line] = lines[line][:character] + "<｜fim▁hole｜>" + lines[line][character:]
        content = '<｜fim▁begin｜>' + "\n".join(lines) + '<｜fim▁end｜>'
        return self.client.generate(
            model= self.model, 
            prompt= content,
            stream=True,
            options = self.options
        )

    
