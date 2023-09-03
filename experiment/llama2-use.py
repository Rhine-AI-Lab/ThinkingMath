from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-13b-hf")
