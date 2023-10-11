
export BASE_MODEL=./model/llama2-13b-nonlora-sft-exp1

python test.py \
    --base_model $BASE_MODEL \
    --prompt_templare gzh_prompter \
