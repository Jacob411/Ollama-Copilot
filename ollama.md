# Ollama
Olama is a platform which allows you to download and run LLMs locally. It is used as a basis of this project and is a required download. 
It can be found [here](https://github.com/ollama/ollama)

## Installation
To install Ollama, you can use the following command:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Also required is the python package `ollama` which can be installed using the following command:
```bash
pip install ollama
```

## Models
A full list of models can be found [here](https://ollama.com/library)
This project requires the use of a code completion specific model. 

Here are some examples of models that can be used:

- deepseek-coder:1.3b (Recommended) This is a lightweight model that is very fast even without a GPU. It is recommended for use in this project.

- starcoder:3b: a good option which is slightly heavier

NOTE: If you have a larger amount of RAM or vRAM, you can use a larger models which will provide better results. The tradeoff is the resources required to run the model.
