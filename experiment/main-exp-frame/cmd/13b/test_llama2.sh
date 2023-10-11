
export BASE_MODEL=./model/llama2-7b-nonlora

python test.py \
    --base_model $BASE_MODEL \
    --prompt_templare gzh_prompter \
