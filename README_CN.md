<div align="center">
<img src="assets/130898843/f145bbb8-ed97-4025-a40b-4260a8a75f6bno_alpha-4.png"  alt="EartAgent logo">
</a>
</div>

<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README_CN.md">简体中文</a> 
</p>

<p align="center">
      <a href="./LICENSE">
    <img height="21" src="https://img.shields.io/badge/License-Apache--2.0-ffffff?style=flat-square&labelColor=d4eaf7&color=1570EF" alt="license">
  </a>
</p>

## 💡 EartAgent 是什么？

EartAgent(Efficient and real-time Agent) EartAgent是一款多模态多智能体框架，通过兼容大模型生态，针对当前大模型存在的诸如信息过时、缺乏外部验证、错误预测频繁等问题，EartAgent框架旨在提升大语言模型的效率和准确性。框架轻量易用，具备实时搜索能力等一系工具，通过多智能体协作和反思机制提高回答精度。该框架兼容性强，提供封装实例，实现开箱即用。
在高容错下，我们还提供封装实例给开发者开箱即用：
- 😃实例
  - 实时语音对话
  - 网站克隆
  - 论文书写
- 😁游戏:
  - 狼人杀
  - 意大利小镇生活

## 📌 近期更新
- 2024-05-17 EartAgent5月17号正式上线github
- 2024-05-15 集成大模型 OpenAI GPT-4o、Gemini1.5pro。

## 🎬 试一试

### 📝 前提条件

- python >= 3.9 
   > 如果你并没有在本机安装 pytorch（Windows、Mac，或者 Linux）, 可以参考文档 [Install pytorch](https://pytorch.org/) 自行安装。
   > 推荐使用conda作为管理工具，您可以使用以下命令创建一个新的Python 3.9虚拟环境：
   >
   > ```bash
   > conda create -n EartAgent python=3.9
   > conda activate EartAgent
   > ```
   > ```bash
   > git clone https://github.com/haijian-wang/EartAgent.git
   > ```
   > 安装依赖包
   > ```bash
   > pip install -r requirements.txt
   > ```

### 🚀 快速开始

1. 以下实例我们使用中国通义大模型为示例：

   > 需要提前申请api_key,根据你的需求进行[申请](https://dashscope.console.aliyun.com/apiKey)：
   > ```python
   > import EartAgent
   >
   > form EartAgent.Agent.text_Agent import *
   > 
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
   >while True:
   >x = agent_1t(x)
   >x = agent_2(x)
   >
   ># 如果用户输入"exit"，则终止对话
   >if x.content == "exit":
   >    print("Exiting the conversation.")
   >    break
   >```
   >更简单的你只需要，EartAgent提供了Pipeline来维护智能体之间消息流的选项
   >```python
   >pipeline = Pipeline(agent_list=[agent_1, agent_2])
   >final_response = pipeline.execute_pipeline(initial_message="Initial message to pipeline")
   >```
   >其实agent还可以进行群聊沟通
   >```python
   >hub = MsgHub(agent_list)
   >hub.broadcast_message("Hello, everyone.")
   >hub.execute_pipeline()
   >```
   >你还可以随意的在群聊里面增删成员
   >```python
   >hub.add_agent(agent_3)
   >hub.remove_agent(agent_3)
   >```
3. 我们准备了丰富的工具提供给Agent进行使用比如智能体联网
   >但是在这里需要申请[search_api_key](https://serpapi.com/)
   >```python
   >agent_1 = QwenAgent(
   >     config=AgentConfig(name='Kerry',
   >                        system_prompt="You're a good helper.",
   >                        tool_use=[
   >                            {'name': 'serpapi_search', 'api_key': 'your_search_api_key'}
   >                        ]))
   > ```
5. 我们还有更多的工具可以使用,具体的如下,UtilityTools里面有很多工具等待你去探索
   >```python
   >from EartAgent.utils.UT import UtilityTools
   >tools = UtilityTools()
   >```
   >
### 🚀 封装实例

1. 在EartAgent中我们提供了很多让开发者开箱即用的封装实例,例如(网站克隆、论文写作、实时语音对话等等)
如何使用？我们以实时语音对话为例
   > 仍然需要提前申请api_key,根据你的需求进行[申请](https://dashscope.console.aliyun.com/apiKey)：
   > ```python
   >from EartAgent.app_packaging.voice_dialog_assistant import VoiceAssistant
   >assistant = VoiceAssistant(api_key="your_api_key")
   >assistant.run()        
   > ```
### 🤗 反思机制

1. 在EartAgent中我们可以让Agent进行自我反思，以输出更好的回答
   > ```python
   >from EartAgent.thinking.reflector import AgentReflector
   >qwen_reflector = AgentReflector(qwen_agent)
   ># 这里可以定义反思次数   
   >reflected_content = qwen_reflector.Mreflect(reflection_count=3)        
   > ```
### 🤪 对于框架的我们做的内容还有很多，大家可以跟着使用
### 🙂 欢迎和我一起交流和探讨
- 😃 email:wanghaijian05@gmail.com
- 🫡 Wechat:AI_nlp_john
- 感谢所有帮助过我的人！
   

   
   
