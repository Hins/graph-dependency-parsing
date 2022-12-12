# 基于Flair的组块分析模型评测工具

## 目录

+ <a href="#1">功能介绍</a>
+ <a href="#2">上手指南</a>
  + <a href="#3">开发前的配置要求</a>
  + <a href="#4">安装步骤</a>
+ <a href="#5">文件目录说明</a>

## <span name="1">功能介绍</span>

​		基于Flair的组块分析模型评测工具，针对中文句法分析输出结果。输入的格式为 .json 输出格式为 .json。

##<span name="2">上手指南 </span>

### <span name="3">开发前的配置要求</span>

arm服务器
argparse
psutil

### <span name="4">安装步骤</span>

pip install -r requirements.txt

## <span name="5">文件目录说明</span>

code
├── Dockerfile ---> docker镜像工具
├── eval.py ---> 评测工具