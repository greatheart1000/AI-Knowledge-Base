# 最新即插即用注意力机制+ffn层

https://mp.weixin.qq.com/s/cMbYNWGfZe6hBFigoFvM1w





图像分类和检测任务

## **ASSA模块**

### ** **** **** **** ****定义与结构**

**- 双分支模式：**ASSA模块采用双分支模式，包括稀疏自注意力分支（SSA）和密集自注意力分支（DSA）。SSA用于过滤掉低查询-键匹配分数的负面影响，而DSA则确保足够的信息流通过网络，以学习判别性表示。**- 自适应加权：**通过自适应的加权机制，将SSA和DSA的输出进行融合。这种设计使模型能够动态调整稀疏与密集注意力的权重，从而根据具体的任务和输入内容有效地平衡信息流，既能过滤掉无关特征，又保留必要的信息。

### **工作原理**

**- 稀疏自注意力（SSA）：**使用基于ReLU的稀疏注意力机制，过滤掉查询与键之间低匹配的无关交互，减少无效特征的参与，帮助聚焦在最有价值的信息交互上。**- 密集自注意力（DSA）：**采用标准的softmax密集注意力机制，补充SSA，以确保在稀疏处理过程中不会丢失关键信息。

### **应用场景**

**- 图像恢复任务：**ASSA最早应用于图像恢复任务，通过减少噪声交互并保留重要的特征信息，显著提升了模型的处理效率。**- 目标检测：**在YOLOv11模型中引入ASSA机制，可以优化特征提取过程，减少特征冗余或噪声干扰，进一步提升模型对复杂场景的适应性和检测性能。**- 时间序列预测：**将ASSA机制和LSTM处理后的特征输入到Transformer网络进行预测，可以进一步提高预测的准确性和效率，在顶刊ETTh开源数据集达到了不错的效果**- 医疗影像处理：**对于需要从复杂的医学图像中提取关键特征的任务，如癌症检测、CT或MRI图像分析，ASSA能够有效过滤无用信息，提升对病灶区域的关注和检测精度。





### **义与结构**

特征细化前馈网络（Feature Refinement Feed-forward Network, FRFN）是一种专门设计的深度学习结构，旨在提高图像处理任务中的特征表示能力。其核心设计理念是通过逐层细化和优化特征图，从而实现更高的分类和检测精度。

**- 线性层1：**将输入特征维度扩展到隐藏维度的两倍，并通过激活函数进行非线性变换。**- 深度可分离卷积：**对扩展后的特征进行深度可分离卷积操作，进一步提取局部特征。**- 线性层2：**将特征维度压缩回原始维度。**- 部分卷积：**对部分特征通道进行卷积操作，以增强特征中的有用元素。**- 门控机制：**通过门控机制减少冗余信息的处理负担，提升特征的纯净度。

### **工作原理**

FRFN模块的工作原理可以概括为以下几个步骤：**- 特征扩展：**通过线性层将输入特征的维度扩展到隐藏维度的两倍，增加特征的表达能力。**- 深度可分离卷积：**对扩展后的特征进行深度可分离卷积操作，提取局部特征，同时减少计算量。**- 特征压缩：**通过线性层将特征维度压缩回原始维度，减少特征冗余。**- 部分卷积：**对部分特征通道进行卷积操作，增强特征中的有用元素。**- 门控机制：**通过门控机制减少冗余信息的处理负担，提升特征的纯净度。





### **应用场景**

**- 图像恢复任务：**在去噪、去雨滴、去雾、超分辨率等场景中，FRFN能够有效减少通道维度上的冗余信息，提升重要特征的表达，从而提高恢复图像的质量和细节还原能力。

**- 图像分类和检测任务：**在处理复杂图像时，FRFN可以通过精炼和增强有价值的特征，帮助模型更准确地分类或检测目标，特别是在多类或高维度特征的任务中表现出色。

**- 高分辨率图像处理：**在高分辨率图像或视频处理中，FRFN能够减少不必要的信息流，增强重要特征的表达，使模型更高效地处理大规模图像数据。

**- 医学图像分析：**在处理复杂的医学影像时，FRFN有助于减少噪声和干扰，聚焦于病变区域的关键特征，提升医疗影像分析的精度和效率。

### **集成到YOLOv11和RT-DETR**

将FRFN模块集成到YOLOv11和RT-DETR模型中的步骤如下：

1. 创建脚本文件：在`ultralytics->nn`路径下创建`blocks.py`脚本，用于存放模块代码。
2. 复制代码：将上述FRFN模块的代码复制到`blocks.py`脚本中。
3. 更改`task.py`文件：在`ultralytics->nn->modules->task.py`中导入FRFN模块。
4. 修改模型配置：在模型配置文件中添加FRFN模块的配置。
5. 训练模型：创建训练脚本，使用修改后的模型配置进行训练。



## CVPR 2024 | 单头注意力机制(SHSA)，即插即用，涨点起飞！

AI前沿速递 [AI前沿速递](javascript:void(0);) *2025年01月15日 11:47* *安徽*

**标题：**SHViT: Single-Head Vision Transformer with Memory Efficient Macro Design

**论文链接：**https://arxiv.org/pdf/2401.16456

**代码链接：**https://github.com/ysj9909/SHViT



## **代码实现**

**ASSA模块代码**

```python
import torchimport torch.nn as nnfrom timm.models.layers import trunc_normal_from einops import repeat
class LinearProjection(nn.Module):    def __init__(self, dim, heads=8, dim_head=64, bias=True):        super().__init__()        inner_dim = dim_head * heads        self.heads = heads        self.to_q = nn.Linear(dim, inner_dim, bias=bias)        self.to_kv = nn.Linear(dim, inner_dim * 2, bias=bias)        self.dim = dim        self.inner_dim = inner_dim
    def forward(self, x, attn_kv=None):        B_, N, C = x.shape        if attn_kv is not None:            attn_kv = attn_kv.unsqueeze(0).repeat(B_, 1, 1)        else:            attn_kv = x        N_kv = attn_kv.size(1)        q = self.to_q(x).reshape(B_, N, 1, self.heads, C // self.heads).permute(2, 0, 3, 1, 4)        kv = self.to_kv(attn_kv).reshape(B_, N_kv, 2, self.heads, C // self.heads).permute(2, 0, 3, 1, 4)        q = q[0]        k, v = kv[0], kv[1]        return q, k, v
class WindowAttention_sparse(nn.Module):    def __init__(self, dim, win_size, num_heads=8, token_projection='linear', qkv_bias=True, qk_scale=None, attn_drop=0., proj_drop=0.):        super().__init__()        self.dim = dim        self.win_size = win_size  # Wh, Ww        self.num_heads = num_heads        head_dim = dim // num_heads        self.scale = qk_scale or head_dim ** -0.5        # define a parameter table of relative position bias        self.relative_position_bias_table = nn.Parameter(            torch.zeros((2 * win_size[0] - 1) * (2 * win_size[1] - 1), num_heads))  # 2*Wh-1 * 2*Ww-1, nH        # get pair-wise relative position index for each token inside the window        coords_h = torch.arange(self.win_size[0])  # [0,...,Wh-1]        coords_w = torch.arange(self.win_size[1])  # [0,...,Ww-1]        coords = torch.stack(torch.meshgrid([coords_h, coords_w], indexing='ij'))  # 2, Wh, Ww        coords_flatten = torch.flatten(coords, 1)  # 2, Wh*Ww        relative_coords = coords_flatten[:, :, None] - coords_flatten[:, None, :]  # 2, Wh*Ww, Wh*Ww        relative_coords = relative_coords.permute(1, 2, 0).contiguous()  # Wh*Ww, Wh*Ww, 2        relative_coords[:, :, 0] += self.win_size[0] - 1  # shift to start from 0        relative_coords[:, :, 1] += self.win_size[1] - 1        relative_coords[:, :, 0] *= 2 * self.win_size[1] - 1        relative_position_index = relative_coords.sum(-1)  # Wh*Ww, Wh*Ww        self.register_buffer("relative_position_index", relative_position_index)        trunc_normal_(self.relative_position_bias_table, std=.02)        if token_projection == 'linear':            self.qkv = LinearProjection(dim, num_heads, dim // num_heads, bias=qkv_bias)        else:            raise Exception("Projection error!")        self.token_projection = token_projection        self.attn_drop = nn.Dropout(attn_drop)        self.proj = nn.Linear(dim, dim)        self.proj_drop = nn.Dropout(proj_drop)        self.softmax = nn.Softmax(dim=-1)        self.relu = nn.ReLU()        self.w = nn.Parameter(torch.ones(2))  # 自适应权重参数
    def forward(self, x, attn_kv=None, mask=None):        # 调整输入维度，从 (B, C, H, W) 转为 (B, H, W, C)        x = x.permute(0, 2, 3, 1).reshape(x.shape[0], x.shape[2] * x.shape[3], x.shape[1])        B_, N, C = x.shape        q, k, v = self.qkv(x, attn_kv)        q = q * self.scale        attn = (q @ k.transpose(-2, -1))        relative_position_bias = self.relative_position_bias_table[self.relative_position_index.view(-1)].view(            self.win_size[0] * self.win_size[1], self.win_size[0] * self.win_size[1], -1)  # Wh*Ww,Wh*Ww,nH        relative_position_bias = relative_position_bias.permute(2, 0, 1).contiguous()  # nH, Wh*Ww, Wh*Ww        ratio = attn.size(-1) // relative_position_bias.size(-1)        relative_position_bias = repeat(relative_position_bias, 'nH l c -> nH l (c d)', d=ratio)        attn = attn + relative_position_bias.unsqueeze(0)        if mask is not None:            nW = mask.shape[0]            mask = repeat(mask, 'nW m n -> nW m (n d)', d=ratio)            attn = attn.view(B_ // nW, nW, self.num_heads, N, N * ratio) + mask.unsqueeze(1).unsqueeze(0)            attn = attn.view(-1, self.num_heads, N, N * ratio)        attn0 = self.softmax(attn)        attn1 = self.relu(attn) ** 2  # b,h,w,c        w1 = torch.exp(self.w[0]) / torch.sum(torch.exp(self.w))        w2 = torch.exp(self.w[1]) / torch.sum(torch.exp(self.w))        attn = attn0 * w1 + attn1 * w2        attn = self.attn_drop(attn)        x = (attn @ v).transpose(1, 2).reshape(B_, N, C)        x = self.proj(x)        x = self.proj_drop(x)        x = x.reshape(x.shape[0], int(math.sqrt(x.shape[1])), int(math.sqrt(x.shape[1])), x.shape[2]).permute(0, 3, 1, 2)        return x
    def extra_repr(self) -> str:        return f'dim={self.dim}, win_size={self.win_size}, num_heads={self.num_heads}'
```







## 给一个 14B 的模型和 20B token 的数据，在 32张 A100 上要训练多少时间？



根据之前 OpenAI 的 Scaling Law 的论文，里面对 Transformers 的计算量进行了估算，大概的过程是这样的：

假设

- C 是训练的总 FLOPs (floating point operations)
- N 为模型的参数量
- D 为训练的 token 量。

Transformers 里绝大多数运输都是矩阵相乘，矩阵相乘的运算量是矩阵大小的两倍，因为**对于矩阵中的每个元素来说，需要一次乘法和一次加法**。

先说前向运算，每一个 token 都会在模型里运算一遍，所以对于一个 token 来说，前向运算的 FLOPs 为 2N。

那么对于 D 个 token 来说，前向运算的 FLOPs 为 2ND。

而神经网络的反向传播的 FLOPs 量，大致为前向运算的 2倍，共计 4ND。原理可以看：[学妹问：“反向传播的计算量是前向传播计算量的几倍？”](https://mp.weixin.qq.com/s?__biz=MzUyOTA5OTcwMg==&mid=2247486124&idx=1&sn=c9294e6696047bb616e0f640fca3ff5f&scene=21#wechat_redirect)

所以，最终 C = 6ND。

**当然这只是个大概的估计，实际上运算量会更多一些**，因为还有一些非矩阵的运算。如果为了节省显存，采用了一些比如 Activation recomputation 等，计算量会显著增加。

知道了总的运算量，下一步就是查一下显卡的运算速度，就能得出题目的答案。

对于 A100 来说，FP16 的峰值运算速度为 312 TFLOPS (Tera Floating Point Operations Per Second), 也就是

那么对于前面的任务来说，需要的时间为



上面的单位是秒，换算成天为 1.95 天。

但是注意这里只是最理想的情况下，实际上运算量比这个大，而且对于大模型的训练来说，**根本无法达到 A100 的峰值运算速度**，因为有大量的通信，而且内部运算也并不全是 FP16 的计算。

我们看看 llama 当时的训练数据：

When training a 65B-parameter model, our code processes around 380 tokens/sec/GPU on 2048 A100 GPU with 80GB of RAM. This means that training over our dataset containing 1.4T tokens takes approximately 21 days.

带入上面的公式:



换算成天数为 9.89 天，但是实际上用了 21 天。从这里可以推断出，他们的 GPU 的平均运算速度为 146.94 TFLOPS, MFU（Model FLOPs Utilization， 算力的利用率）为 47.1%

而且模型越大，MFU 越低，比如 Llama 3 405B的训练数据如下图， 最高的 MFU 也就 43%：

![图片](https://mmbiz.qpic.cn/mmbiz_png/GCNbdU0ticibpf2pfr19cdgia2JdnrZZzI3pVs8VueDPq1FMWMiciaQibNtXCEiaNGhjaicqkAPtFNWwweCN1G1pkG7yhQ/640?wx_fmt=png&from=appmsg&tp=wxpic&wxfrom=5&wx_lazy=1&wx_co=1)

这已经是业界几乎最顶尖的水平了。

所以我们按照业界的顶尖水平来估算的话，最开始问题的答案修正为 4.135 天。

在 Transformers 模型中，前向和反向传播的计算量（FLOPs）是理解模型效率的重要方面。让我们详细解释一下前向运算的 FLOPs 是如何计算的，以及为何反向传播的 FLOPs 大致是前向运算的两倍。

前向运算的 FLOPs

1. **前向运算的定义**：前向运算是指将输入数据通过神经网络进行处理以得到输出的过程。在 Transformers 中，每个 token（输入的基本单位，如单词或子词）都需要通过模型的每一层进行前向计算。

2. **单个 token 的计算量**：

   - 假设我们处理的 token 有 NNN 个特征（例如，词嵌入的维度）。

   - 在每一层中，进行矩阵乘法的计算时，假设我们有一个权重矩阵 WWW 大小为 N×NN \times NN×N。

   - 为计算输出，我们需要进行 NNN 次乘法（与每个权重相乘），并且需要 N−1N - 1N−1 次加法（将乘法结果相加）。

   - 所以，对于一个 token 的前向传播，计算量为：

     FLOPs=N (乘法)+(N−1) (加法)≈2N\text{FLOPs} = N \text{ (乘法)} + (N - 1) \text{ (加法)} \approx 2NFLOPs=N (乘法)+(N−1) (加法)≈2N

3. **多个 token 的计算量**：

   - 对于 

     DDD

      个 token，前向运算的 FLOPs 为：

     FLOPsforward=2N×D=2ND\text{FLOPs}_{\text{forward}} = 2N \times D = 2NDFLOPsforward=2N×D=2ND

反向传播的 FLOPs

1. **反向传播的定义**：反向传播是训练神经网络时使用的一种算法，它通过计算损失函数的梯度，来更新网络的权重。反向传播的过程会计算每一层的梯度，通常涉及到与前向传播相似的计算。

2. **反向传播的计算量**：

   - 在反向传播过程中，每一层的权重更新涉及到的计算量与前向传播相似。具体来说，对于每个参数的梯度计算，需要计算损失函数关于该参数的导数。
   - 这种计算通常也需要进行矩阵乘法，类似于前向传播，因此反向传播的 FLOPs 也大致为 2N2N2N（乘法和加法）。

3. **整个网络的反向传播计算量**：

   - 由于反向传播需要计算每层的梯度，且通常涉及多次更新和计算，因此反向传播的计算量大致是前向传播的两倍。

   - 所以，对于 

     DDD

      个 token，反向传播的 FLOPs 为：

     FLOPsbackward≈2×FLOPsforward=2×2ND=4ND\text{FLOPs}_{\text{backward}} \approx 2 \times \text{FLOPs}_{\text{forward}} = 2 \times 2ND = 4NDFLOPsbackward≈2×FLOPsforward=2×2ND=4ND

### 总结

- 前向运算的 FLOPs 是 2ND2ND2ND，因为每个 token 的计算涉及 2N2N2N 的操作。
- 反向传播的 FLOPs 是前向运算的两倍，主要是由于每层的梯度计算和权重更新的复杂性，导致整体计算量增加。因此，反向传播的总体 FLOPs 约为 4ND4ND4ND。



## 交叉熵 (cross entropy) ，KL 散度的值，到底有什么含义？

交叉熵一看就是个信息论的概念，为什么变成了大模型最常用的损失函数了呢？交叉熵的值到底有什么含义呢？与 KL 散度又有什么关系呢？

信息如何度量？

如果某件事情大概率发生，当这件事情发生的时候，携带的信息量是很少的。举个例子：国足输球的概率是95%。当国足又输了的时候，并没有什么信息量。但是如果国足赢球了，那这个信息量大的惊人。

为了度量某个事件的信息，可以定义这么一个信息函数 , 其中 p 为事件的发生概率。这个信息函数有如下的性质

1. 这个函数应该**和概率p成反比,** p 越大则 I(p) 越小。
2. 当 p = 1 时，I(p) 为0. **总是发生的事情没有任何信息量**。
3. , **两个独立的事件同时发生产生的信息，应该等于各自信息的和。**

最后这个信息函数香农给出的答案是 。有没有其他表示呢？可能有，但是当时香农给出的解就是这个，后来大家发现这个似乎就是唯一的解。

 可以用来表示一个概率为 p 的事件发生后的产生信息或者不确定性。那么假设某个随机事件的概率分布为 p, 那么其信息（或者不确定性）的期望值是多少呢？根据求期望的公式，应该为

这就是**信息熵。衡量的是某个随机事件的信息的期望值**。



**信息熵就是某个随机事件的信息的期望值，****同时也是****最优编码的期望长度。**







## 损失函数的作用是什么？以及它基本理论是什么样的？

从字面来理解，损失函数就是用来计算损失的；但它具体的原理是什么呢？ ‍‍‍‍‍‍‍‍‍‍‍‍

在神经网络中，数据的基本格式是向量；而向量是有大小和方向的量，因此就可以用向量来表示数据之间的关系——也就是相似度。‍‍‍‍‍‍

以监督学习图像处理为例，给你一堆猫或狗的照片，然后把猫和狗单独放到不同的目录下，也就是猫一个目录，狗一个目录；这时把猫和狗以及他们的标签——也就是目录名称，转化为向量结构之后；表示猫的向量和表示狗的向量会占据不同的向量空间，而表示不同猫的向量会离的近一点；同样表示狗的向量也会离的近一点，这种表示方式就叫做欧式距离。‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍

以生活中的分类问题举例，比如老师在讲台上写两个标签，一个男同学，一个女同学；然后说男同学站男同学标签下，女同学站女同学标签下；‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍

监督学习也是同样的道理，猫狗的标签(目录)就是告诉神经网络模型，这个是猫，那个是狗；然后让神经网络模型自己去根据特征让表示猫的向量和表示狗的向量，尽量靠近猫标签和狗标签。

无监督学习的基础理论和监督学习基本类似，只不过不会告诉神经网络猫和狗的标签；而是让神经网络自己去根据猫狗的特征去区分，虽然区分的结果可能是错的。

未经过训练的神经网络模型就像幼儿园的小孩子一样，虽然你说了，他也听了，但他做的都是错的；但怎么衡量这个错误的大小呢 ？‍‍‍‍‍‍‍‍‍‍

这就是损失函数的作用，通过计算神经网络给的猫狗向量与真实标签之间的误差，来告诉神经网络你这个搞错了，再想想办法；然后神经网络就会进行新一轮的计算，只不过在从新训练之前会先进行参数调优，也就是优化函数。

优化函数的作用就是告诉神经网络模型，你刚刚算的误差太大了，现在去调整一下你的参数然后从新计算。

但是这里就有一个问题，神经网络怎么知道自己应该怎么调优？总要有一个具体的解决方法或者说算法吧。‍‍‍‍‍‍‍‍‍‍

这时优化函数的经典实现——梯度下降的作用就体现了；实现优化函数的方式有多种，但使用最多影响力最大的就是梯度下降算法。

什么是梯度下降算法？ 

想明白什么是梯度下降，首先你要明白什么是梯度；

但为什么梯度下降就可以优化损失函数计算的误差？或者说为什么导数就可以解决损失函数的误差？

之所以导数能解决损失函数的误差问题，主要原因就在于，数学追求的一种完美曲线(直线)，虽然这个曲线不是一般意义上的水平直线，但它依然是一个连续曲线。‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍‍

![](C:\Users\great\Desktop\资料\梯度下降算法.png)

梯**度计算**：在优化过程中，通常需要计算代价函数的梯度，以指导参数的更新。



## 请说明Momentum、AdaGrad、Adam梯度下降法的特点

Momentum、AdaGrad、Adam是针对SGD梯度下降算法的缺点的改进算法。在SGD算法中，如果函数的形状非均向（参数大小差异较大），SGD的搜索路径会呈“之字形”移动，搜索效率较低







## **什么是线性回归？**

**线性回归实际上就是求线性函数的参数的值的过程**。所谓的线性回归，实际上就类似我们初中开始学习的函数。无论是一元函数还是多元函数，都有其自变量与多变量。而线性回归的目标实际上就是找出自变量与因变量的函数关系，也就是F(x)

我们有足够多的散点时，我们的眼睛会看出来，它好像有点规律，也就是基本在一条线的附近，其实也就是一次函数，y=kx+b。说到这，是不是基本就能理解线性回归干的是什么事了？它就是要找到我们所给的数据，符合一个什么样的函数，或者说表达式。

有些人说，为什么不用数学的方法，我带入两个点进入y=kx+b中，我不就可以求出该直线了吗？事实上真的可以吗？这条线只不过是这些点整体符合的一个趋势函数，但并不是每个点都严格符合该函数。因此，我们并不可以或者说并不容易用数学的方法求出该函数。（数学大佬请避开，我只是说我这种渣渣）
![](C:\Users\great\Desktop\资料\线性回归.png)



## 给一个大模型，如何估算训练和推理需要的显存？

知道了参数的数量，那么根据加载模型采用的精度，很容易就能算出显存是多少。具体来说，1B 的 float32 参数占 4GB, 如果是 bf16/fp16 则占 2GB， int8则为 1GB。





## 激活函数

![](C:\Users\great\Desktop\资料\GeLU激活函数.png)

```python
def gelu(x):
   return x * norm.cdf(x)
GELU论文中，作者使用了标准正态分布的累积分布函数（cdf）的近似计算来提高计算速度。

def relu(x):
   return np.maximum(0, x)

def swish(x, beta=1):
   return x * (1 / (1 + np.exp(-beta * x)))
Swish，这也是对带有非零负值梯度的ReLU平滑版本

GLU（Gated Linear Units）其实不算是一种激活函数，而是一种神经网络层。它是一个线性变换后面接门控机制的结构。其中门控机制是一个sigmoid函数用来控制信息能够通过多少。

其中 
 为sigmoid函数，
 为逐元素乘。通过使用其他的激活函数我们就能够得到GLU的各种变体了。

比如说现在LLM中常用的SwiGLU其实就是采用Swish作为激活函数的GLU变体

```

![](C:\Users\great\Desktop\资料\GLU.png)

## 大模型推理 repetition penalty 是如何实现的？  

repetition penalty是什么意思 有什么作用

Repetition Penalty 的定义

**Repetition Penalty** 是一种在生成文本时使用的技术，旨在减少模型生成重复或冗余内容的倾向。它通过对已经生成的词汇施加惩罚，降低它们在后续生成中的概率，从而鼓励模型生成更加多样化和丰富的文本。

Repetition Penalty 的作用

1. **减少重复**：通过惩罚重复出现的词，避免生成的内容过于单一，增加文本的多样性和可读性。
2. **提高文本质量**：使生成的文本更具连贯性和逻辑性，减少冗余和无意义的重复。
3. **增强用户体验**：在对话系统和文本生成应用中，减少重复内容可以提高用户的满意度。

实现方式

Repetition Penalty 的实现通常涉及以下步骤：

1. **追踪生成的词**：在生成文本的过程中，记录已经生成的每个词。

2. **计算惩罚因子**：对于每个待生成的词，如果该词已经在之前的输出中出现过，则计算一个惩罚因子。这个因子通常是一个小于1的值，以降低该词的生成概率。

3. **调整概率分布**：在生成下一个词时，使用该惩罚因子调整模型输出的概率分布。具体方法如下：

   - 设定一个原始的概率分布 PPP。

   - 对于已生成的词 

     wiw_iwi

     ，调整其概率：

     P′(wi)=P(wi)⋅penaltyP'(w_i) = P(w_i) \cdot \text{penalty}P′(wi)=P(wi)⋅penalty

   - 其中，penalty < 1，且其他词的概率可以相应进行归一化，以确保总概率和为1。

4. **生成下一个词**：根据调整后的概率分布选择下一个词。

示例

假设模型生成的句子为：

复制

```
"The cat sat on the mat. The cat"
```

在生成到第二个 "The cat" 时，模型会检测到 "The" 和 "cat" 已经出现过。通过应用 Repetition Penalty，模型会降低这两个词的生成概率，从而鼓励生成其他词汇。

总结

Repetition Penalty 是一种有效的策略，旨在减少生成文本中的重复内容，提高文本的多样性和质量。通过对已生成词的概率施加惩罚，模型能够生成更加丰富和连贯的文本。



```python
class RepetitionPenaltyLogitsProcessor(LogitsProcessor):
    r"""
    [`LogitsProcessor`] enforcing an exponential penalty on repeated sequences.

    Args:
        repetition_penalty (`float`):
            The parameter for repetition penalty. 1.0 means no penalty. See [this
            paper](https://arxiv.org/pdf/1909.05858.pdf) for more details.
    """

    def __init__(self, penalty: float):
        if not isinstance(penalty, float) or not (penalty > 0):
            raise ValueError(f"`penalty` has to be a strictly positive float, but is {penalty}")

        self.penalty = penalty

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        score = torch.gather(scores, 1, input_ids)

        # if score < 0 then repetition penalty has to be multiplied to reduce the previous token probability
        score = torch.where(score < 0, score * self.penalty, score / self.penalty)

        scores.scatter_(1, input_ids, score)
        return scores
```



## 基于 Llama 的模型都有哪些？有什么细微的差异？

Llama 1 的架构是基于 GPT 来的，做了如下的升级：

- 采用了 Pre-RMSNorm
- 把 Gelu 改成了 SwiGLU
- 位置编码改成了 RoPE

需要注意的是，**这些内容都不是 Meta 首创的，但是 Meta 的 Llama 团队将他们组合到了一起并且取得了开源的 SOTA 效果**。至于闭源的，那肯定早都用了。

Llama2 和 Llama1 结构基本相同，但是在更大的模型上（34B和70B） 采用了 grouped-query attention，主要是为了加速。

Llama3 做了如下改变

- GQA 变成标配。
- 上下文 从 4096 扩展到了 8192
- 词表大小从 32k 变成了 128k。前两代都是基于 SentencePiece 的，Llama 3 直接采用了 Openai 的 tiktoken。因为 tiktoken 用 rust 进行了底层的深度优化，效率比其他家要好很多。

Baichuan 系列

yi 的架构和 llama2 一样。需要注意的是 llama2 只在更大的模型上使用了 GQA, 但是 Yi 在所有系列都用了。

在经历过一些开源协议的质疑之后，**现在 yi 的模型可以用 LlamaForCausalLM 加载了**



## KV Cache 原理是什么？

![](C:\Users\great\Desktop\资料\KV cache.png)

![](C:\Users\great\Desktop\资料\kv cache2.png)

上面图和公式，我们可以得出结论：

1. 默认计算方式存在大量冗余计算。
2.  Attk只与 Qk 有关。
3. 推理第XK个字符的时候只需要输入字符 XK-1 即可.

所以每一步其实只需要根据 Qk 计算 Attk 就可以，但是K 和 V是全程参与计算的。**站在优化后的算法来看，只需要把每一步的K 和 V  缓存起来， 所以叫 KV Cache**。但是实际上不做优化的话，K 和 V 也需要缓存的。

下面4张图展示了使用KV Cache和不使用的对比。

最后需要注意当 sequence 比较长，或者 batch 特别大的时候，KV Cache 其实还是个Memory刺客。

比如batch_size=32, head=32, layer=32, dim_size=4096, seq_length=2048, float32(4个字节)类型，则需要占用的显存为 2 * 32 * 32 * 4096 * 2048  * 4 / 1024/1024/1024 = 64G。一张 A100 也就 80G，所以如何减少 KV 的内存变得尤为重要。

目前各种框架，针对 KV Cache 做了优化，比如 Page Attention, Prefix Caching， Token 的稀疏化， KV 共享或者压缩（MQA、GQA 和 MLA），LayerSkip，Mooncake 等等，可以说 **KV Cache 目前是推理的基建，而各种基于 KV Cache 的优化撑起了推理加速的半边天**。



## Token 的稀疏化

Token 的稀疏化在 KV Cache 的优化中，主要是通过减少需要存储和计算的键值对数量，从而降低内存使用和计算复杂性。以下是具体的实现原理和效果：

Token 的稀疏化

1. **稀疏化定义**：稀疏化是指在生成过程中，只记录和处理关键的或重要的 tokens，而忽略那些在上下文中不重要或不相关的 tokens。这意味着，不是每个输入 token 都会在 KV Cache 中保留其对应的键值。

2. **选择性存储**：
   - 在生成过程中，模型可以根据某些标准（如注意力权重、重要性评分等）选择性地存储键值对。这样，只有那些对当前生成步骤有显著贡献的 tokens 会被缓存。
   - 例如，可以设定一个阈值，只有当某个 token 的注意力权重超过该阈值时，才将其键值对存入 KV Cache。

3. **降低内存使用**：
   - 通过只存储重要的 tokens，可以显著减少 KV Cache 的大小，从而降低内存消耗。这对于大规模模型尤为重要，因为它们在推理时可能会生成大量的 tokens。

4. **提高计算效率**：
   - 当只有一部分 tokens 被存储在 KV Cache 中时，模型在计算注意力时也只需考虑这些 tokens，从而减少计算量。这可以加速推理过程，提高模型的响应速度。

示例

假设在处理一个长文本时，模型可能会生成大量的 tokens，但并不是所有的 tokens 在上下文中都具有相同的重要性。通过稀疏化：

- 只保留与当前生成的内容相关性强的 tokens，比如：
  - 当前生成的上下文中，某些特定的名词或动词可能更为重要，而其他的连接词或冗余信息则可以忽略。
  
- 这样，假设原本需要存储 1000 个 tokens 的 KV Cache，通过稀疏化，仅存储 300 个重要 tokens，显著减少了内存占用和计算负担。

总结

Token 的稀疏化通过选择性地存储和处理重要的 tokens，降低了 KV Cache 的大小和计算复杂性。这种方法在大模型推理中，尤其是在处理长文本时，能够有效提升性能和效率。

## LayerSkip

Meta 推出了*LayerSkip*,一种全新的端到端解决方案,专门用于提高大语言模型(LLM)的推理速度
