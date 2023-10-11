
export BASE_MODEL=./model/llama2-7b-nonlora-sft-exp1/sft-data/NousResearch/Llama-2-7b-chat-hf/checkpoint-200

python test.py \
    --base_model $BASE_MODEL \
    --prompt_templare gzh_prompter \

# CMD
# python test.py --prompt_templare gzh_prompter --base_model ./model/llama2-7b-nonlora-sft-exp1/sft-data/NousResearch/Llama-2-7b-chat-hf/checkpoint-200
