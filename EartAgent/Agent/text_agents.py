# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import abc
from dataclasses import dataclass, field
from http import HTTPStatus
from typing import List, Dict, Optional
import dashscope
import anthropic
from openai import OpenAI
from EartAgent.utils.UT import UtilityTools

"""
@EartAgentV1.0
    Includes ali qwen series, kimi series, baichuan series, zero-one-everything (loading), Deepseek, llama3, chatgpt series, claude series, phi-3
"""


@dataclass
class AgentConfig:
    name: str
    system_prompt: str
    model_name: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    remember: bool = False
    tool_use: List[Dict[str, str]] = field(default_factory=list)


class Agent(abc.ABC):
    remember_flag = False

    def __init__(self, config: AgentConfig):
        self.config = config
        self.memory: List[str] = []
        self.remember_flag = config.remember
        self.utility_tools = UtilityTools()
        self.utility_tools.log_agent(self)

    def integrate_tools(self, sys_prompt: str) -> list:
        context = []
        for tool_config in self.config.tool_use:
            tool_name = tool_config['name']
            api_key = tool_config['api_key']
            tool_method = getattr(self.utility_tools, tool_name, None)
            if callable(tool_method):
                params = self.extract_params_for_tool(sys_prompt, tool_name)
                params['api_key'] = api_key
                result = tool_method(params['query'], params['api_key'])
                context.append(result)
        return context

    def extract_params_for_tool(self, prompt: str, tool_name: str) -> dict:
        if tool_name == 'serpapi_search':
            return {'query': prompt}
        return {}

    def retrieve_context_from_url(self, url: str) -> str:
        if url.startswith("http"):
            return self.utility_tools.web_crawler_all(url)
        elif url.endswith(".pdf"):
            return " ".join(self.utility_tools.read_pdf(url))
        elif url.endswith(".docx"):
            return " ".join(self.utility_tools.read_docx(url))
        elif url.endswith(".pptx"):
            return " ".join(self.utility_tools.read_ppt(url))
        elif url.endswith(".txt"):
            return " ".join(self.utility_tools.read_txt(url))
        else:
            raise ValueError("Unsupported URL or file type")

    def build_rag_prompt(self, user_input: str, context: str) -> str:
        return f"{user_input}\n\nAdditional Context:\n{context}"

    @abc.abstractmethod
    def chat(self, sys_prompt: str) -> str:
        raise NotImplementedError

    def __call__(self, sys_prompt: str, url: Optional[str] = None) -> str:
        context = ""
        if url:
            context = self.retrieve_context_from_url(url)
        response = self.chat(self.build_rag_prompt(sys_prompt, context))
        self.speak(response)
        return response

    def speak(self, response: str):
        print(f"{self.config.name}：{response}")

    def remember(self, message: str):
        if self.remember_flag:
            self.memory.append(message)
            if len(self.memory) > 5:
                self.memory.pop(0)
        self.utility_tools.log_agent(self)

    def recall(self) -> List[str]:
        return self.memory

    def build_messages(self, sys_prompt: str) -> List[dict]:
        messages = [
            {"role": "system",
             "content": f"You are a helpful assistant.{self.config.system_prompt} and this is your recall {self.recall()} if you need you can find something ,You are {self.config.name}"},
            {"role": "user", "content": sys_prompt}
        ]
        return messages


class QwenAgent(Agent):
    """
    Agents for the Qwen model using Dashscope
    """
    api_key: str = None
    default_model_name = 'qwen_turbo'

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.model_name = config.model_name or self.default_model_name

    def chat(self, sys_prompt: str) -> str:
        dashscope.api_key = self.api_key
        # Output of the integration tool
        tool_context = self.integrate_tools(sys_prompt)
        context = []
        # Passing the output of system tips and tools to the model
        if tool_context != context:
            full_prompt = f"{sys_prompt}+'The results of the web search are as follows:'+{tool_context}"
        else:
            full_prompt = sys_prompt
        self.remember(f"users say that：{sys_prompt}")
        messages = self.build_messages(full_prompt)
        response = dashscope.Generation.call(
            dashscope.Generation.Models.qwen_turbo,
            messages=messages,
            result_format='message',
        )
        self.remember(f"You said.：{response.output.choices[0].message.content}")
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content
        else:
            raise Exception(
                f"Request failed: {response.request_id}, {response.status_code}, {response.code}, {response.message}")


class KimiAgent(Agent):
    api_key: str = None
    default_model_name = 'moonshot-v1-8k'

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.model_name = config.model_name or self.default_model_name

    def chat(self, sys_prompt: str) -> str:

        tool_context = self.integrate_tools(sys_prompt)
        context = []

        if tool_context != context:
            full_prompt = f"{sys_prompt}+'The results of the web search are as follows:'+{tool_context}"
        else:
            full_prompt = sys_prompt
        self.remember(f"users say that：{sys_prompt}")
        messages = self.build_messages(full_prompt)
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.moonshot.cn/v1",
        )
        completion = client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            temperature=self.config.temperature or 0.3,
        )
        return completion.choices[0].message.content

class YiAgent(Agent):
    api_key: str = None
    default_model_name = "yi-large"

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.model_name = config.model_name or self.default_model_name

    def chat(self, sys_prompt: str) -> str:

        tool_context = self.integrate_tools(sys_prompt)
        context = []

        if tool_context != context:
            full_prompt = f"{sys_prompt}+'The results of the web search are as follows:'+{tool_context}"
        else:
            full_prompt = sys_prompt
        self.remember(f"users say that：{sys_prompt}")
        messages = self.build_messages(full_prompt)
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.lingyiwanwu.com/v1"
        )
        completion = client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            # temperature=self.config.temperature or 0.3,
        )
        return completion.choices[0].message.content


class BaiChuanAgent(Agent):

    api_key: str = None
    default_model_name = 'baichuan2-7b-chat-v1'

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.model_name = config.model_name or self.default_model_name

    def chat(self, sys_prompt: str) -> str:

        tool_context = self.integrate_tools(sys_prompt)

        context = []
        if tool_context != context:
            full_prompt = f"{sys_prompt}+'The results of the web search are as follows:'+{tool_context}"
        else:
            full_prompt = sys_prompt
        dashscope.api_key = self.api_key
        self.remember(f"users say that：{sys_prompt}")
        messages = self.build_messages(full_prompt)
        response = dashscope.Generation.call(
            dashscope.Generation.Models.qwen_turbo,
            messages=messages,
            result_format='message',
        )
        self.remember(f"你说的：{response}")
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content
        else:
            raise Exception(
                f"Request failed: {response.request_id}, {response.status_code}, {response.code}, {response.message}")


class DeepSeekAgent(Agent):

    api_key: str = None
    default_model_name = "deepseek-chat"

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.model_name = config.model_name or self.default_model_name

    def chat(self, sys_prompt: str) -> str:

        tool_context = self.integrate_tools(sys_prompt)
        context = []

        if tool_context != context:
            full_prompt = f"{sys_prompt}+'The results of the web search are as follows:'+{tool_context}"
        else:
            full_prompt = sys_prompt
        self.remember(f"users say that：{sys_prompt}")
        messages = self.build_messages(full_prompt)
        client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com",
        )
        completion = client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            temperature=self.config.temperature or 0.3,
        )
        return completion.choices[0].message.content


class LlamaAgent(Agent):
    """
    Agents using Nvidia's Llama model
    """
    api_key: str = None
    default_model_name = 'meta/llama3-70b-instruct'

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.model_name = config.model_name or self.default_model_name

    def chat(self, sys_prompt: str) -> str:
        tool_context = self.integrate_tools(sys_prompt)
        context = []
        if tool_context != context:
            full_prompt = f"{sys_prompt}+'The results of the web search are as follows:'+{tool_context}"
        else:
            full_prompt = sys_prompt
        self.remember(f"user say that {sys_prompt}")
        messages = self.build_messages(full_prompt)
        print(messages)
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )
        completion = client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            temperature=self.config.temperature or 0.7,
            top_p=1,
            max_tokens=self.config.max_tokens or 1024,
            stream=True
        )
        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        return response


class MixtralAgent(Agent):
    """
    Agents using Nvidia's Mixtral model
    """
    api_key: str = None
    default_model_name = "mistralai/mixtral-8x22b-instruct-v0.1"

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.model_name = config.model_name or self.default_model_name

    def chat(self, sys_prompt: str) -> str:

        tool_context = self.integrate_tools(sys_prompt)
        context = []

        if tool_context != context:
            full_prompt = f"{sys_prompt}+'The results of the web search are as follows:'+{tool_context}"
        else:
            full_prompt = sys_prompt
        self.remember(f"user say that {sys_prompt}")
        messages = self.build_messages(full_prompt)
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )
        completion = client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            temperature=self.config.temperature or 0.7,
            top_p=1,
            max_tokens=self.config.max_tokens or 1024,
            stream=True
        )
        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        return response


class PhiAgent(Agent):
    """
    Agents using Nvidia's microsoft model
    """
    api_key: str = None
    default_model_name = "microsoft/phi-3-mini-128k-instruct"

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.model_name = config.model_name or self.default_model_name

    def chat(self, sys_prompt: str) -> str:

        tool_context = self.integrate_tools(sys_prompt)
        context = []

        if tool_context != context:
            full_prompt = f"{sys_prompt}+'The results of the web search are as follows:'+{tool_context}"
        else:
            full_prompt = sys_prompt
        self.remember(f"user say that {sys_prompt}")
        messages = self.build_messages(full_prompt)
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=self.api_key
        )
        completion = client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            temperature=self.config.temperature or 0.7,
            top_p=1,
            max_tokens=self.config.max_tokens or 1024,
            stream=True
        )
        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        return response


class ChatGPTAgent(Agent):
    """
    Agents using OpenAI's ChatGPT model
    """
    api_key: str = None
    default_model_name = 'gpt-3.5-turbo'

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.model_name = config.model_name or self.default_model_name

    def chat(self, sys_prompt: str) -> str:
        self.remember(f"users say that：{sys_prompt}")
        messages = self.build_messages(sys_prompt)

        try:
            client = OpenAI()
            completion = client.chat.completions.create(
                model=self.config.model_name,
                messages=messages,
                temperature=self.config.temperature or 0.7
            )
            response_content = completion.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API request failed: {e}")

        self.remember(response_content)
        return response_content


class ClaudeAgent(Agent):
    """
    Agents using Anthropic's Claude model
    """
    api_key: str = None
    default_model_name = 'claude-3-sonnet-20240229'

    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.config.model_name = config.model_name or self.default_model_name

    def chat(self, sys_prompt: str) -> str:
        self.remember(f"users say that：{sys_prompt}")
        messages = self.build_messages(sys_prompt)

        client = anthropic.Anthropic(api_key=self.api_key)

        message = client.messages.create(
            model=self.config.model_name,
            messages=messages,
            temperature=self.config.temperature or 0.7,
            max_tokens=self.config.max_tokens or 1000,
            system=sys_prompt
        )

        response_content = message.content
        self.remember(response_content)
        return response_content

