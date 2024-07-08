
# Ollama Copilot
## Overview
Ollama Copilot is a work in progress. The goal is to allow users to integrate their Ollama code completion models into their IDEs, giving GitHub Copilot-like completions. First integration will be in Neovim.

## Features
- [x] Language server which can provide completions from an Ollama model for a given prefix
- [x] Manually requested ghost text completions which can be inserted into the editor (OllamaSuggestion User Command)
- [ ] Automatic ghost text completions which can be inserted into the editor, which update as the user types
- [ ]  
- [ ] Ghost text completions which can be inserted into the editor
- [ ] Integration with Neovim (in progress)
- [ ] Integration with other IDEs

## Installation
To use Ollama-Copilot, you need to have Ollama installed [https://github.com/ollama/ollama](https://github.com/ollama/ollama):  
```bash
curl -fsSL https://ollama.com/install.sh | sh
```
Clone this repository:
```bash
git clone https://github.com/Jacob411/Ollama-Copilot.git
cd Ollama-Copilot
```
Currently, the project is in the experimental stage and is not yet ready for use. But the main Language server is in the lsp directory. 
## Usage
To run the language server, run the following command:

```python
python lsp/ollama_lsp.py
```
## Contributing
Contributions are welcome! If you have any ideas for new features, improvements, or bug fixes, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
