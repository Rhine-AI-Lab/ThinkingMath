export BASE_MODEL=NousResearch/Llama-2-13b-chat-hf

export DATA_PATH=./data/think_math_data/think_math_1500x4.jsonl
export DATA_NAME=sft-data
export CACHE_DIR=NONE

export OUTPUT_DIR=./model/think_math_model
export DEEPSPEED_STAGE=3

export NUM_GPUS=$GPU_NUM

deepspeed --num_gpus=$NUM_GPUS lora-finetune.py \
    --base_model $BASE_MODEL \
    --data_path $DATA_PATH \
    --output_dir $OUTPUT_DIR'/'$DATA_NAME'/'$BASE_MODEL \
    --batch_size 128 \
    --micro_batch_size 4 \
    --num_epochs 3 \
    --learning_rate 1e-4 \
    --cutoff_len 512 \
    --lora_r 8 \
    --lora_alpha 16 \
    --lora_dropout 0.05 \
    --lora_target_modules "['q_proj', 'v_proj']" \
    --val_set_size 10 \
    --group_by_length \
    --cache_dir $CACHE_DIR \
    --deepspeed_stage $DEEPSPEED_STAGE
