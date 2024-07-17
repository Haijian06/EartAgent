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

## 💡 What is EartAgent？

EartAgent (Efficient and real-time Agent) is a multimodal multi-intelligent body framework, through the compatibility of the large model ecology, for the current large model exists such as outdated information, the lack of external validation, error prediction frequently, etc., EartAgent framework aims to improve the efficiency and accuracy of the large language model. The framework is lightweight and easy to use, with a range of tools such as real-time search capabilities, and improves answer accuracy through multi-intelligence collaboration and reflection mechanisms. The framework is highly compatible and provides packaging examples to realize out-of-the-box use.
At high fault tolerance, we also provide wrapper examples for developers to use out of the box:
- 😃 Example
  - Real-time voice dialog
  - Website cloning
  - Thesis writing
- 😁 Games.
  - Werewolf
  - Italian Town Life
  - moot court
## 📌 Recent Updates
- 2024-05-31 We try our best to build the best function call.
- 2024~~~~~~ One click to build a simpler RAG, we're working on it, stay tuned!☺️
- 2024-05-22 Integrate model zhipuAI, add moot court games
- 2024-05-18  Integration of the Great Model Yi!
- 2024-05-17 EartAgent has been released on github on May 17th!
- 2024-05-15 Integration of large models OpenAI GPT-4o, Gemini1.5pro.

## 🎬 Give it a Try

### 📝 Prerequisites

- python >= 3.9 
   > If you do not have pytorch installed locally (Windows, Mac, or Linux), you can install it yourself by referring to the documentation [Install pytorch](https://pytorch.org/).
   > Recommended to use conda as an administrative tool, you can create a new Python 3.9 virtual environment with the following command:
   > Creating a conda environment
   > ```bash
   > conda create -n EartAgent python=3.9
   > ```
   > ```bash
   > conda activate EartAgent
   > ```
   > Pulling items
   > ```bash
   > git clone https://github.com/haijian-wang/EartAgent.git
   > ```
   > ```bash
   > cd EartAgent
   > ```
   > Installation of dependencies
   > ```bash
   >pip install -r requirements.txt
   > ```

### 🚀 Getting Started Quickly

1. In the following examples we use the China Tongyi Big Model as an example:

   > You need to apply api_key in advance, [apply](https://dashscope.console.aliyun.com/apiKey) according to your needs:
   >```python
   > import EartAgent
   >
   > form EartAgent.Agent.text_Agent import *
   > 
   > QwenAgent.api_key = “your_api_key”
   > agent = QwenAgent(
   > config=AgentConfig(name='kerry', system_prompt=“”))
   > x = 'Hi kerry'
   > agent(x)
   > ```
   > Memory is not turned on by default because it will cost you more tokens, but of course it is convenient to turn it on
   > ```python
   > agent = QwenAgent(
   >   config=AgentConfig(name='kerry', system_prompt=“”,remember=True)
   > )
   > ```
   > We also support uploading all files and URLs to make Agent replies more what you want them to be.
   > ```python
   > agent(x,url='')
   > ```
2. Multi-intelligentsia coordinated work and communication:
   >Multi-intelligence collaboration can greatly prompt the accuracy of responses, and MsgHub and Pipeline are the main means of communication between intelligences in EartAgent
   >If we want agent_1 and agent_2 to communicate then it would be
   >```python
   >while True:
   >  x = agent_1t(x)
   >  x = agent_2(x)
   >
   ># If the user types “exit”, terminate the dialog.
   >if x.content == “exit”:
   >   print(“Exiting the conversation.”)
   >   break
   >```
   >Simpler you just need, EartAgent provides the option of Pipeline to maintain the flow of messages between intelligences
   >```python
   >pipeline = Pipeline(agent_list=[agent_1, agent_2])
   >final_response = pipeline.execute_pipeline(initial_message=“Initial message to pipeline”)
   >```
   > Actually agent can also communicate in group chats
   >```python
   >hub = MsgHub(agent_list)
   >hub.broadcast_message(“Hello, everyone.”)
   >hub.execute_pipeline()
   >```
   >You can also add and remove members to the group chat as you wish.
   >```python
   >hub.add_agent(agent_3)
   >hub.remove_agent(agent_3)
   >```
3. We have prepared a rich set of tools for Agents to use, such as Smart Body Networking.
   > But here we need to request [search_api_key](https://serpapi.com/).
   >```python
   >agent_1 = QwenAgent(
   > config=AgentConfig(name='Kerry',
   > system_prompt=“You're a good helper.", system_prompt="You're a good helper."
   > tool_use=[
   > {'name': 'serpapi_search', 'api_key': 'your_search_api_key'}
   > ]))
   > ```
5. There are many more tools available to us, as follows, and UtilityTools is full of them for you to explore.
   >UtilityTools has many tools for you to explore.
   >```python
   >from EartAgent.utils.UT import UtilityTools
   >tools = UtilityTools()
   >```
   >
### 🚀 Encapsulation Examples

1. In EartAgent we provide a lot of out-of-the-box wrapper examples for developers to use, such as (website cloning, essay writing, real-time voice dialog, etc.).
How to use it? Let's take real-time voice dialog as an example
   > Still need to apply for api_key in advance, according to your needs to [apply](https://dashscope.console.aliyun.com/apiKey):
   > ```python
   >from EartAgent.app_packaging.voice_dialog_assistant import VoiceAssistant
   >assistant = VoiceAssistant(api_key=“your_api_key”)
   >assistant.run()        
   > ```
### 🤗 Reflection mechanism

1. In EartAgent we can have the Agent reflect on itself to output better answers
   > ```python
   >from EartAgent.thinking.reflector import AgentReflector
   >qwen_reflector = AgentReflector(qwen_agent)
   ># Here you can define the number of reflections   
   >reflected_content = qwen_reflector.Mreflect(reflection_count=3)        
   > ```
### 🤪 There's more to the framework
### 🙂 Feel free to contact me for a discussion
- 😃 email:wanghaijian05@gmail.com
- 🫡 Wechat:AI_nlp_john
- 🤓 Thank you to everyone who helped me.
## ⭐ Star History

[[![Star History Chart](https://api.star-history.com/svg?repos=haijian-wang/EartAgent&type=Date)](https://star-history.com/#haijian-wang/EartAgent&Date)](https://star-history.com/#Haijian06/EartAgent&Date)
