<div align="center">
<img src="![f145bbb8-ed97-4025-a40b-4260a8a75f6bno_alpha-4](https://github.com/haijian-wang/EartAgent/assets/130898843/229751e5-7ce5-4f75-8180-b54b44c57b90)
" width="350" alt="EartAgent logo">
</a>
</div>

<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_zh.md">简体中文</a> 
</p>

<p align="center">
      <a href="https://github.com/infiniflow/ragflow/blob/main/LICENSE">
    <img height="21" src="https://img.shields.io/badge/License-Apache--2.0-ffffff?style=flat-square&labelColor=d4eaf7&color=1570EF" alt="license">
  </a>
</p>

## 💡 EartAgent 是什么？

EartAgent(Efficient and real-time Agent) EartAgent是一款多模态多智能体框架，通过兼容大模型生态，针对当前大模型存在的诸如信息过时、缺乏外部验证、错误预测频繁等问题，EartAgent框架旨在提升大语言模型的效率和准确性。框架轻量易用，具备实时搜索能力等一系工具，通过多智能体协作和反思机制提高回答精度。该框架兼容性强，提供封装实例，实现开箱即用。

## 📌 近期更新
- 2024-05-17 预计5月17号上线github
- 2024-05-15 集成大模型 OpenAI GPT-4o。

## 🎬 快速开始

### 📝 前提条件

- CPU >= 4 核
- python >= 3.9 
  > 如果你并没有在本机安装 pytorch（Windows、Mac，或者 Linux）, 可以参考文档 [Install pytorch](https://pytorch.org/) 自行安装。

### 🚀 快速开始

1. 以下实例我们使用中国通义大模型为示例：
   > 推荐使用conda作为管理工具，您可以使用以下命令创建一个新的Python 3.9虚拟环境：
   >
   > ```bash
   > conda create -n EartAgent python=3.9
   > conda activate EartAgent
   > ```
   > ```bash
   > pip install -r
   > ```
   > 需要提前申请api_key,根据你的需求进行申请：
   > ```python
   > import EartAgent
   > form EartAgent.Agent.text_Agent import QwenAgent
   > QwenAgent.api_key = "your_api_key"
   > agent = QwenAgent(
   >     config=AgentConfig(name='kerry', system_prompt=""))
   > x = '你好kerry'
   > agent(x)
   >
   > ```
   > 默认不开启记忆因为这会耗费你更多的token，当然开启也很方便
   > ```python
   > agent = QwenAgent(
   >     config=AgentConfig(name='kerry', system_prompt="",remember=True))
   > ```
   > 我们还支持上传所有文件,具体的
   > ```python
   > agent = QwenAgent(
   >     config=AgentConfig(name='kerry', system_prompt=""))
   > agent(x,url='')
   > ```
   > 一键构建rag
   
