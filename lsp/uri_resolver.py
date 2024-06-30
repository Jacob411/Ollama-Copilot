
from urllib.parse import urljoin 
from urllib.request import pathname2url
from pathlib import Path

def file_path_to_uri(file_path):
    # Convert to absolute path
    absolute_path = Path(file_path).resolve()
    print(f"Absolute Path: {absolute_path}")
    # Convert to file URI
    uri = urljoin('file:', pathname2url(str(absolute_path)))
    return uri

# Example usagp
file_path = './example.txt'
uri = file_path_to_uri(file_path)
print(f"File Path: {file_path}")
print(f"File URI: {uri}")
