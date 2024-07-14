import ollama
class CompletionEngine:
    def __init__(self, model : str, options = {}):
        self.model = model
        self.client = ollama.Client("http://localhost:11434")
        self.options = options

    def complete(self, lines, line, character):
        pre_cursor_text = "\n".join(lines[:line]) + "\n" + lines[line][:character]
        return self.client.chat(
            model= self.model, 
            messages=[{
            'role': 'user',
            'content': pre_cursor_text,
            }],                 
            stream=True,
            options = self.options 
        )
    
    def fim_complete(self, lines, line, character):
        lines[line] = lines[line][:character] + "<｜fim▁hole｜>" + lines[line][character:]
        content = '<｜fim▁begin｜>' + "\n".join(lines) + '<｜fim▁end｜>'
        return self.client.chat(
            model= self.model, 
            messages=[{
            'role': 'user',
            'content': content,
            }],                 
            stream=True,
            options = self.options
        )
