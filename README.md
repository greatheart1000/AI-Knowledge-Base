## 文本提示词+全量参数
### 指定生成视频的宽高比为16:9，时长为 5 秒，帧率为 24 fps，分辨率为720p，包含水印，种子整数为11，不固定摄像头 参数使用简写

"""p"content": [
        {
            "type": "text",
            "text": "女孩抱着狐狸 --rs 720p --rt 16:9 --dur 5 --fps 24 --wm true --seed 11 --cf false"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/i2v_foxrgirl.png"
            }
        }
    ] """
## 图生视频首尾帧
curl -X POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "wan2-1-14b-flf2v-250417",
    "content": [
         {
            "type": "text",
            "text": "CG动画风格，一只蓝色的小鸟从地面起飞，煽动翅膀。小鸟羽毛细腻，胸前有独特的花纹，背景是蓝天白云，阳光明媚。镜跟随小鸟向上移动，展现出小鸟飞翔的姿态和天空的广阔。近景，仰视视角。--rs 720p  --dur 5"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/wan_input_first_frame.png"
            },
            "role": "first_frame"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/wan_input_last_frame.png"
            },
            "role": "last_frame"
        }
    ]
}'

## 图生视频 首帧
curl -X POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedance-1-0-lite-i2v-250428",
    "content": [
        {
            "type": "text",
            "text": "女孩抱着狐狸，女孩睁开眼，温柔地看向镜头，狐狸友善地抱着，镜头缓缓拉出，女孩的头发被风吹动  --ratio adaptive  --dur 5"
        },
        {
            "type": "image_url",
            "image_url": {
                "url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/i2v_foxrgirl.png"
            }
        }
    ]
}'

本接口支持文生视频（t2v）和图生视频（i2v）： 
doubao-seedance
文生视频：doubao-seedance-1-0-lite-t2v，根据您输入的文本提示词+参数（可选）生成目标视频。
图生视频：doubao-seedance-1-0-lite-i2v，根据您输入的首帧图片+文本提示词（可选）+参数（可选）生成目标视频。
doubao-seaweed
文生视频：doubao-seaweed，根据您输入的文本提示词+参数（可选）生成目标视频。
图生视频：doubao-seaweed，根据您输入的首帧图片+文本提示词（可选）+参数（可选）生成目标视频。
wan2.1-14b
文生视频：wan2-1-14b-t2v，根据您输入的文本提示词+参数（可选）生成目标视频。
图生视频：wan2-1-14b-i2v，根据您输入的首帧图片+文本提示词+参数（可选）生成目标视频。
图生视频-首尾帧：wan2-1-14b-flf2v，根据您输入的首帧图片+尾帧图片+文本提示词+参数（可选）生成目标视频。
    
