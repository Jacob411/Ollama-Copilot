
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained('codellama/CodeLlama-7b-Python/tokenizer.model')
# Load model with memory-mapping
model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-7b-Python/consolidated.00.pth", low_cpu_mem_usage=True)
