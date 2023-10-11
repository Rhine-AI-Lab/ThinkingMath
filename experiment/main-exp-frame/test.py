import fire
import gradio as gr
import torch

# from peft import PeftModel
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig, AutoTokenizer, AutoModelForCausalLM, \
    BloomForCausalLM
from prompter_setting.Prompter import Prompter


DEFAULT_BASE_MODEL = './model/exp2'
# DEFAULT_BASE_MODEL = './model/Llama-2-7b-chat-hf'
device = "cuda" if torch.cuda.is_available() else "cpu"


def main(
        load_8bit: bool = False,
        base_model: str = DEFAULT_BASE_MODEL,
        cache_dir: str = "NONE",
        lora_weights: str = "NONE",
        prompt_template: str = "gzh_prompter",
):
    # 设置Tokenizer
    prompter = Prompter(prompt_template)
    if 'NONE' in cache_dir: cache_dir = None

    if 'llama' in base_model.lower():
        tokenizer = LlamaTokenizer.from_pretrained(base_model, cache_dir=cache_dir)
    else:
        tokenizer = AutoTokenizer.from_pretrained(base_model, cache_dir=cache_dir)

    causalLM = LlamaForCausalLM if 'llama' in base_model.lower() else BloomForCausalLM if 'bloom' in base_model.lower() else AutoModelForCausalLM
    # 设置模型
    if device == 'cuda':
        model = causalLM.from_pretrained(base_model, load_in_8bit=load_8bit, torch_dtype=torch.float16,
                                         device_map='auto', cache_dir=cache_dir)
        # if 'NONE' not in lora_weights:
        #     if lora_weights: model = PeftModel(model, lora_weights, torch_dtype=torch.float16)

    elif device == 'mps':
        model = causalLM.from_pretrained(base_model, torch_dtype=torch.float16, device_map={"": device},
                                         cache_dir=cache_dir)
        # if 'NONE' not in lora_weights:
        #     if lora_weights: model = PeftModel(model, lora_weights, torch_dtype=torch.float16, device_map={"": device})

    else:
        model = causalLM.from_pretrained(base_model, low_cpu_mem_usage=True, device_map={"": device},
                                         cache_dir=cache_dir)
        # if 'NONE' not in lora_weights:
        #     if lora_weights: model = PeftModel(model, lora_weights, device_map={"": device})

    model.config.pad_token_id = tokenizer.pad_token_id = 0
    model.config.bos_token_id = 1
    model.config.eos_token_id = 2
    if not load_8bit: model.half()
    model.eval()

    def inference(
        instruction, input=None, temperature=0.1, top_p=0.75,
        top_k=40, num_beams=4, max_new_tokens=128, **kwargs
    ):
        generation_config = GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_beams=num_beams,
            **kwargs
        )
        with torch.no_grad():
            prompt = prompter.generate_prompt(instruction, input)

            for i in range(6):
                # print(f'\nPrompt-{i}: \n{prompt}\n\n-----------------')
                inputs = tokenizer(prompt, return_tensors="pt")
                input_ids = inputs['input_ids'].to(device)
                generation_output = model.generate(
                    input_ids=input_ids, generation_config=generation_config,
                    return_dict_in_generate=True, output_scores=True, max_new_tokens=max_new_tokens
                )
                prompt = tokenizer.decode(generation_output.sequences[0])
                print(f'Inference-{i+1}: discuss length {len(prompt)}')
                if '</s>' in prompt:
                    print('Inference finished.\n')
                    # print(f'Hole discuss:\n{prompt}')
                    break
                prompt = prompt[4:]

            discuss = prompter.get_response(prompt)
            if '</s>' in discuss:
                discuss = discuss.split('</s>')[0]
            return discuss

    use_inner = input('是否开始执行内置任务？(y/n)')
    if 'y' in use_inner.lower():

        for instruction in [
            "Tell me about alpacas.",
            "告诉我中文和英文有什么区别？"
            "Tell me about the president of Mexico in 2019.",
            "List all Canadian provinces in alphabetical order.",
            "Write a Python program that prints the first 10 Fibonacci numbers.",
            "Tell me five words that rhyme with 'shock'.",
            "Translate the sentence 'I have no mouth but I must scream' into Spanish.",
            "Count up from 1 to 500.",
        ]:
            print(f'Instruction: {instruction}')
            print(f'Response: {inference(instruction)}', end='\n\n')

        print('\n内置问题回答结束 进入自由问答\n')

    history = ''
    while True:
        q = input('Instruction: ')
        if 'ctn' in q.lower() or 'continue' in q.lower():
            a = inference(history)
            history += a
            print("Continue:", a, end='\n\n')
        else:
            a = inference(q)
            history += q + a
            print("Response:", a, end='\n\n')


if __name__ == '__main__':
    fire.Fire(main)
