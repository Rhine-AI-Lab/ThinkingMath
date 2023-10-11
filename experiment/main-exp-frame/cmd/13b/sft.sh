export BASE_MODEL=NousResearch/Llama-2-7b-chat-hf
export CACHE_DIR=./model/llama2-7b-nonlora
export OUTPUT_DIR=./model/llama2-7b-nonlora-sft-exp3
#export DATA_PATH=./data/think_math_10k2k1k.jsonl
export DATA_PATH=./data/think_math_8k4k3k.jsonl
export DATA_NAME=sft-data

export DEEPSPEED_STAGE=3
export NUM_GPUS=$GPU_NUM

deepspeed --num_gpus=$NUM_GPUS nonlora-finetune.py \
    --base_model $BASE_MODEL \
    --data_path $DATA_PATH \
    --output_dir $OUTPUT_DIR'/'$DATA_NAME'/'$BASE_MODEL \
    --batch_size 128 \
    --micro_batch_size 4 \
    --num_epochs 3 \
    --learning_rate 1e-4 \
    --cutoff_len 512 \
    --val_set_size 2000 \
    --group_by_length \
    --cache_dir $CACHE_DIR \
    --deepspeed_stage $DEEPSPEED_STAGE
