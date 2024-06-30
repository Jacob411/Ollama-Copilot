import torch
import torchvision
from transformers import pipeline

print(torch.__version__)
print(torchvision.__version__)
sentiment_pipeline = pipeline('sentiment-analysis')
result = sentiment_pipeline('We love you')
print(result)
