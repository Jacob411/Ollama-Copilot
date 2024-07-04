import requests

url = 'http://localhost:8000'
data = {'message': 'value number 1'}

try:
    response = requests.post(url, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    print(response.json())  # Print the response JSON
except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')

