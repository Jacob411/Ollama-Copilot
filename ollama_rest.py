import requests
import json
url = "http://localhost:11434/api/generate"

data = {
    "model": "custom-deepseek",
    "prompt": "import torch",
    "stream": True,
    "options" : {
        "temperature": 0.5,
        "num_predict": 40,
    }
}

headers = {"Content-Type": "application/json"}  # Set content type header

response = requests.post(url, json=data, headers=headers, stream=True)

if response.status_code == 200:
    # Iterate through the streaming response
    for line in response.iter_content(1024):  # Adjust chunk size as needed
        if line:  # Filter out keep-alive new chunks
            # Decode the JSON chunk (assuming each chunk is a complete JSON object)
            data = json.loads(line.decode("utf-8"))
            print(data["response"], end="")  # Process the generated

            if "eval_count" in data:
                print(f"\n Eval Duration: {data['eval_duration'] / 1000000000}s")
                print(data)





