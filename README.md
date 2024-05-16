<div align="center">
<img src="assets/130898843/f145bbb8-ed97-4025-a40b-4260a8a75f6bno_alpha-4.png"  alt="EartAgent logo">
</a>
</div>

<p align="center">
  <a href="./README_EN.md">English</a> |
  <a href="./README.md">简体中文</a> 
</p>

<p align="center">
      <a href="">
    <img height="21" src="https://img.shields.io/badge/License-Apache--2.0-ffffff?style=flat-square&labelColor=d4eaf7&color=1570EF" alt="license">
  </a>
</p>

## 💡 EartAgent 是什么？

EartAgent(Efficient and real-time Agent) EartAgent是一款多模态多智能体框架，通过兼容大模型生态，针对当前大模型存在的诸如信息过时、缺乏外部验证、错误预测频繁等问题，EartAgent框架旨在提升大语言模型的效率和准确性。框架轻量易用，具备实时搜索能力等一系工具，通过多智能体协作和反思机制提高回答精度。该框架兼容性强，提供封装实例，实现开箱即用。

## 📌 近期更新
- 2024-05-17 预计5月17号上线github
- 2024-05-15 集成大模型 OpenAI GPT-4o、Gemini1.5pro。

## 🎬 试一试

### 📝 前提条件

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
   > x = 'Hi kerry'
   > agent(x)
   >
   > ```
   > 默认不开启记忆因为这会耗费你更多的token，当然开启也很方便
   > ```python
   > agent = QwenAgent(
   >     config=AgentConfig(name='kerry', system_prompt="",remember=True))
   > ```
   > 我们还支持上传所有文件和网址,让Agent回复更加是你希望的
   > ```python
   > agent(x,url='')
   > ```
2. 多智能体协调工作与交流：
   >多智能体协作能够大大的提示回复的准确性，MsgHub和Pipeline是EartAgent中智能体之间的主要通信手段
   >如果我们希望agent_1和agent_2进行交流那么会是
   >```python
    while True:
    x = dialogAgent(x)
    x = userAgent(x)

    # 如果用户输入"exit"，则终止对话
    if x.content == "exit":
        print("Exiting the conversation.")
        break
   >```
   > 我们准备了丰富的工具提供给Agent进行使用比如智能体联网
   >```python
   >agent_1 = QwenAgent(
   >     config=AgentConfig(name='Kerry',
   >                        system_prompt="You're a good helper.",
   >                        tool_use=[
   >                            {'name': 'serpapi_search', 'api_key': 'your_search_api_key'}]
   >                        ))
   > ```
   > 
   
