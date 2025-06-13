python tools/train.py configs/resnet/resnet101_8xb16_cifar10.py<br>
https://verl.readthedocs.io/en/latest/examples/multi_modal_example.html

merge.sh脚本 
swift export \
    --model /root/autodl-tmp/QwenVLmerged \
    --adapters /root/autodl-tmp/checkpoint0613 \
    --model_type qwen2_5_vl \
    --merge_lora true

push_to_hub.sh 推送模型至modelscope脚本
swift export \
    --adapters /root/autodl-tmp/checkpoint0613 \
    --model /root/autodl-tmp/QwenVLmerged \
    --push_to_hub true \
    --hub_model_id 'greatheart/qwen2.5vl' \
    --model_type qwen2_5_vl \
    --hub_token 'e333fcb9-d4cb-452d-9ae6-59ab02f7b227' \
    --use_hf false
