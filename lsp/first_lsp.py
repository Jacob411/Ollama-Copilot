from pygls.server import LanguageServer
from lsprotocol import types

server = LanguageServer("example-server", "v0.2")
# Create a new feature for the server for textDocument/didOpen
@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
def did_open(params: types.DidOpenTextDocumentParams):
    print("Document opened")
    with open("log.txt", "a") as f:
        f.write(f"Document opened: {params.text_document.uri}\n")
    print(params.text_document.uri)
    print(params.text_document.text)
    print("\n")
    return None

# Create a new feature for the server for textDocument/definition
@server.feature(types.TEXT_DOCUMENT_DEFINITION)
def definition(params: types.DefinitionParams):
    document = server.workspace.get_text_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()
    # Write to a log file if this hits
    with open("log.txt", "a") as f: 
        f.write(f'Checking definition for: {current_line}')
    print(f'Checking definition for: {current_line}\n')
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
    document = server.workspace.get_text_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()
    # Write to a log file if this hits
    with open("log.txt", "a") as f:
        f.write(f'Completing for: {current_line}\n')
    print(f'Completing for: {current_line}\n')
    if not current_line.endswith("hello."):
        return [
            types.CompletionItem(label="random_completion")
        ]

    return [
        types.CompletionItem(label="world"),
        types.CompletionItem(label="friend"),
    ]


if __name__ == "__main__":
    server.start_ws("localhost", 8080)
