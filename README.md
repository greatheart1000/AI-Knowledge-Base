## 懂车帝项目
OSError: image file is truncated报错解决  <br>
解决办法：  <br>
from PIL import ImageFile  <br>
ImageFile.LOAD_TRUNCATED_IMAGES = True <br>

git地址: http://139.159.201.66:8888/dcp-platform-group/isoftstone-dcarpai-ai  <br>
git 账号:1352744183@qq.com  密码: P@ssw0rd!Qw3rTy#ZxCu98&JkLm@12   <br>


autodl 数据上传 scp远程拷贝文件的指令为：scp -rP 35394 <本地文件/文件夹> root@region-1.autodl.com:/root/autodl-tmp
bash run_scripts/muge_finetune_vit-b-14.sh   <br>
后台运行 nohup bash run_scripts/muge_finetune_vit-b-14.sh > app.log 2>&1 &  <br>

python tools/train.py configs/resnet/resnet101_8xb16_cifar10.py<br>
https://verl.readthedocs.io/en/latest/examples/multi_modal_example.html

merge.sh脚本 
swift export \
    --model /root/autodl-tmp/QwenVLmerged \
    --adapters /root/autodl-tmp/checkpoint0613 \
    --model_type qwen2_5_vl \
    --merge_lora true

push_to_hub.sh 推送模型至modelscope脚本 <br>
swift export \
    --adapters /root/autodl-tmp/checkpoint0613 \
    --model /root/autodl-tmp/QwenVLmerged \
    --push_to_hub true \
    --hub_model_id 'greatheart/qwen2.5vl' \
    --model_type qwen2_5_vl \
    --hub_token 'e333fcb9-d4cb-452d-9ae6-59ab02f7b227' \
    --use_hf false

vllm serve QwenVL0613 --port 8000 --served-model-name gpt-4 部署模型命令 <br>
nohup python batch_msg.py > app.log 2>&1 <br>
聊天接口 <br>
curl -X POST http://127.0.0.1:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
           "model": "gpt-4",
           "messages": [
{"role": "system", "content": "You are a helpful assistant."},
 {"role": "user",   "content": "今天天气怎样？"}
],
           "max_tokens": 200
         }'

文本补全接口 <br>
curl -X POST http://127.0.0.1:8000/v1/completions \
     -H "Content-Type: application/json" \
     -d '{
           "model": "gpt-4",
           "prompt": "写一段关于春天的诗：",
           "max_tokens": 100,
           "temperature": 0.8
         }' <br>
发送带图片和文本的请求 <br>
 curl -X POST http://127.0.0.1:8000/v1/chat/completions      -H "Content-Type: application/json"      -d '{
          "model": "gpt-4",
          "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {
              "role": "user",
              "content": [
                {"type": "text", "text": "这张图片里有什么？"},
                {
                  "type": "image_url",
                  "image_url": {
                    "url": "https://dcp-upload-pro.tos-accelerate.volces.com/2025-03-06/d1faed82-ae66-4029-a8df-ad3da9f81cce.jpg"
                  }
                }
              ]
            }
          ],
          "max_tokens": 300
        }' 

