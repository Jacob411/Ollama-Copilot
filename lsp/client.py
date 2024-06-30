import json
import asyncio
import websockets
import time
init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "capabilities": {}
        }
    }
completion_request = {
  "jsonrpc": "2.0",
  "id": 2,
  "method": "textDocument/completion",
  "params": {
    "textDocument": {
      "uri": "file:///home/jacob/repos/Llama-3/lsp/example.txt"
    },
    "position": {
      "line": 2,
      "character": 0
    }
  }
}
definition_request = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "textDocument/definition",
    "params": {
        "textDocument": {
        "uri": "file:///home/jacob/repos/Llama-3/lsp/example.txt"
        },
        "position": {
        "line": 0,
        "character": 0
        }
    }
    }
request2 ={
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "capabilities": {}
}
}

did_open = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "textDocument/didOpen",
    "params": {
        "textDocument": {
        "uri": "file:///home/jacob/repos/Llama-3/lsp/example.txt",
        "languageId": "plaintext",
        "languageId": "plaintext",
        "version": 1,
        "text": "Hello, world!"
        }
    }
    }
input_map = {
    "init": init_request,
    "comp": completion_request,
    "def": definition_request,
    "open": did_open
    }

async def send_request(uri, request):
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(request))
        response = await websocket.recv()
        return json.loads(response)

async def main():
    uri = "ws://localhost:8080"  # Adjust the URI if necessary

    file = "file:///home/jacob/repos/Llama-3/lsp/example.txt"  
    # 
    # response = await send_request(uri, init_request)
    # print(response)
    # time.sleep(2)
    print()
    while True:
        print("Enter a command")
        command = input()
        if command == 'q':
            break
        response = await send_request(uri, input_map[command])
        print()
        print(response)
        time.sleep(2)
    
    input
if __name__ == "__main__":
    asyncio.run(main())
