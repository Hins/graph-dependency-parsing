# 基于图模型的句法分析模型推理工具

## 目录

+ <a href="#1">功能介绍</a>
+ <a href="#2">上手指南</a>
  + <a href="#3">开发前的配置要求</a>
  + <a href="#4">安装步骤</a>
+ <a href="#5">文件目录说明</a>

## <span name="1">功能介绍</span>

​		基于图模型的句法分析模型推理工具，针对中文句法分析输出结果。输入的格式为 .txt 输出格式为 .json。

##<span name="2">上手指南 </span>

### <span name="3">开发前的配置要求</span>

arm服务器
numpy
jieba
torch
pathlib
pickle
matplotlib
argparse
psutil

### <span name="4">安装步骤</span>

pip install -r requirements.txt

## <span name="5">文件目录说明</span>

code
├── README.md ---> 工具说明
├── Dockerfile ---> docker镜像工具
├── /lang_zh/ ---> 模型和词向量文件夹
│ ├── embeddings ---> 中文预训练词向量文件
│ ├── models ---> 模型文件
├── NLP_training.py ---> 推理工具
├── emb.py ---> 预训练词向量生成工具
├── embedding.py ---> 预训练向量在线读取工具
├── inference.py ---> 推理工具
│── monitoring.py ---> 监控工具
│── mst.py ---> 树工具