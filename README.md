## 阿里云镜像加速器地址
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://q34m72kp.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker

## 怎么提高结构化数据召回准确率？怎么提高非结构化数据召回准确率？ bm25+向量检索 还有什么其他方法优化吗

要提升结构化和非结构化数据的检索／召回准确率，单纯依赖 BM25 + 向量检索是个很好的起点，但在生产环境里，你还可以从以下几方面做深入优化和扩展。

---

## 一、结构化数据召回优化

1. 索引和字段优化  
   - 对常用筛选／排序字段建立**复合索引**、**分区**或**列存储**  
   - 利用搜索引擎（如 Elasticsearch）对每个字段做**Field-level Boosting**，将业务重要字段权重抬高  
   - 对数值／范围查询多用倒排+B‐tree 混合索引，避免扫描

2. 同义词／标准化  
   - 预处理：字段值做**同义词映射**（比如 “手机”＝“移动电话”）  
   - 针对关键枚举字段（品牌、型号、颜色等）维护**字典表**或**知识图谱**，查询时先做标准化

3. 精细化匹配策略  
   - 对不同字段选择匹配模式：关键词字段用**精确匹配**或**前缀搜索**；文本描述字段用**N-gram／分词搜索**  
   - 对数值或日期字段用**范围查询**＋**Function Score**（比如离目标值越近分越高）

4. 规则引擎＋机器学习排序  
   - 先用布尔／倒排索引做**粗筛**，再用轻量级模型（LR、GBDT）根据业务信号（点击率、销量、库存等）做**二次排序**  
   - 定期离线训练**Learning to Rank** 模型，在线做实时更新

5. 业务上下文与过滤  
   - 基于用户角色、权限、地域、时间段做**预过滤**，剔除明显不相关数据  
   - 用**缓存**（Redis）存热点回答，提高召回速度

---

## 二、非结构化数据召回优化

除了 BM25 + 向量检索（Dense+Sparse Hybrid）外，还可以：

1. 伪反馈（Pseudo Relevance Feedback）  
   - 用 Top-k 初检文档自动扩充 query（取其中最显著的 n 个 term），再做二次检索  
   - Elasticsearch 支持 **“more_like_this”** 或 PRF 插件

2. 查询扩展与重写  
   - 同义词、拼写纠错、实体识别（NER）＋链接（EL）后，把实体名加入检索  
   - 用户历史/会话上下文做**动态扩展**，保证多轮检索一致性

3. 多粒度切分  
   - 把长文档切成段落／片段（passage），先检段落，再聚合文档级分  
   - Passage-level Dense Retriever（如 SPLADE、TAS-B）对长文本更友好

4. 更强的 Dense Retriever  
   - Bi-encoder：DPR、ANCE、ColBERT  
   - Sparse-aware embedding：SPLADE、SPARTA  
   - 针对业务数据做**领域微调**，提升召回率

5. Cross-encoder 复排  
   - 初检（BM25+Dense）后，用 BERT/GPT 类 Cross-Encoder 做**精排**  
   - 结合**点对点打分**和**顺序打分**，显著提升前 k 的准确率

6. Knowledge Graph／Entity Retrieval  
   - 将文档中的实体／关系抽取构图，把图检索结果反馈到全文检索  
   - 基于图谱做**路径查询**或**子图匹配**，增强语义召回

7. 在线学习与反馈闭环  
   - 收集点击、停留、转化等信号，在线微调检索模型（强化学习或带反馈的 LTR）  
   - 实时更新词表／向量索引，慢慢适应用户口味变化

---

## 三、端到端架构建议

1. **Hybrid Retrieval Pipeline**  
   1. 语法层面粗筛：布尔/BM25  
   2. 语义层面粗筛：Dense Retriever  
   3. 二次排序：Cross-Encoder + 商业规则  
   4. 召回后融合：根据业务打分、实时信号加权融合

2. **离线＋在线分层**  
   - 离线构建 Dense Embedding、LTR 模型  
   - 在线用缓存、精排服务快速响应

3. **监控＆A/B 测试**  
   - 关键指标：召回率（Recall@k）、准确率（Precision@k）、CTR、用户满意度  
   - 新策略或模型做灰度／A/B，对比线上效果

4. **资源权衡**  
   - 排序模型越强，延迟越高。可采用**Coarse-to-Fine**策略：先高 QPS、背后低延迟检索；再精排

---

通过以上手段，结合你具体业务的**数据规模**、**查询特性**和**可用算力**，逐步打磨召回管道，就能在结构化和非结构化场景都拿到更高的召回与排序准确率。

















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

