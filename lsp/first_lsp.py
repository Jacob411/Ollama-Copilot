from pygls.server import LanguageServer
from lsprotocol import types
import time
import ollama

server = LanguageServer("example-server", "v0.2")
# Print hello world to the console


# textDocument/didChange
@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
def did_change(params : types.DidChangeTextDocumentParams):
    # Apply the changes to the document
    # with open("log.txt", "a") as f:
    #     f.write(f"Document changed: {params}\n")
    pass
# Create a new feature for the server for textDocument/didOpen
@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(params: types.DidOpenTextDocumentParams):
    pass

# Create a new feature for the server for textDocument/definition
@server.feature(types.TEXT_DOCUMENT_DEFINITION)
def definition(params: types.DefinitionParams):
    document = server.workspace.get_text_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()
    # Write to a log file if this hits
    if current_line == "hello":
        return types.Location(
            uri=params.text_document.uri,
            range=types.Range(
                start=types.Position(line=0, character=0),
                end=types.Position(line=0, character=5),
            ),
        )
    return None

@server.feature(types.TEXT_DOCUMENT_COMPLETION)
def completions(params: types.CompletionParams):
    start = time.time()
    document = server.workspace.get_text_document(params.text_document.uri)
       #measure time taken to get text of document
    #get the text of the document
    lines = document.lines
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
    response = ollama.chat(model='deepseek-coder:base', 
        messages=[{
        'role': 'user',
        'content': content,
      },])
    return response["message"]["content"]

if __name__ == "__main__":
    #server.start_ws("localhost", 8080)
    server.start_io()
