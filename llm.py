# llm.py

from transformers import AutoTokenizer, AutoModelForCausalLM

# Load DeepSeek R1 (or a distill variant) from Hugging Face
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-0528", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-0528", trust_remote_code=True)

def expand_prompt(prompt: str) -> str:
    """
    Use DeepSeek to creatively expand the user prompt.
    """
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=100, temperature=0.7)
    expanded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return expanded
