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
from dataclasses import dataclass
from http import HTTPStatus
import dashscope
from dashscope import MultiModalConversation

@dataclass
class IAgentConfig:
    """
    Agent configuration information
    """
    name: str
    system_prompt: str
    model_name: str

class Agent(abc.ABC):
    """
    Base agent class, defining the basic interface and behavior of an agent
    """

    def __init__(self, config: IAgentConfig):
        self.config = config

    @abc.abstractmethod
    def analyze(self, image_path_or_url: str, sys_prompt: str) -> str:
        """
        Analyze an image and return a description result
        """
        raise NotImplementedError

class QwenVLPlusAgent(Agent):
    """
    Use Dashscope's QwenVLPlus model for image analysis
    """

    def analyze(self, image_path_or_url: str, sys_prompt: str) -> str:
        messages = [
            {
                "role": "user",
                "content": [
                    {"image": image_path_or_url},
                    {"text": sys_prompt}
                ]
            }
        ]
        response = MultiModalConversation.call(model='qwen-vl-plus', messages=messages)
        if response.status_code == HTTPStatus.OK:
            return response["output"]["choices"][0]["message"]["content"][0]["text"]
        else:
            raise Exception(f"Request failed: {response.request_id}, {response.status_code}, {response.code}, {response.message}")

class QwenVLMaxAgent(Agent):
    """
    Use Dashscope's QwenVLMax model for image analysis
    """

    def analyze(self, image_path_or_url: str, sys_prompt: str) -> str:
        messages = [
            {
                'role': 'system',
                'content': [{'text': self.config.system_prompt}]
            },
            {
                'role': 'user',
                'content': [
                    {'image': image_path_or_url},
                    {'text': sys_prompt}
                ]
            }
        ]
        response = MultiModalConversation.call(model='qwen-vl-max', messages=messages)
        if response.status_code == HTTPStatus.OK:
            return response["output"]["choices"][0]["message"]["content"][0]["text"]
        else:
            raise Exception(f"Request failed: {response.request_id}, {response.status_code}, {response.code}, {response.message}")

class ImageAnalyzer:
    """
    Example usage:
    api_key = "your_api_key_here"  # Replace with your API key
    image_analyzer = ImageAnalyzer(api_key)
    # Analyze a web image
    description = image_analyzer.analyze_web_image("https://example.com/image.jpg", "Please describe this image")
    print(description)
    # Analyze a local image
    description = image_analyzer.analyze_local_image('file://D:/python_project_yeah/NLP/EartAgentV0.1/Agent/images/b99849f6d4244dac5d20c426445b8ec.png', "Please help me describe this image")
    print(description)
    """

    def __init__(self, api_key):
        dashscope.api_key = api_key

    def analyze_web_image(self, image_url, sys_prompt):
        """
        Analyze a web image and return a description result.
        """
        agent = QwenVLPlusAgent(IAgentConfig(name="QwenVLPlus", system_prompt="You are a helpful image analyzer.", model_name="qwen-vl-plus"))
        return agent.analyze(image_url, sys_prompt)

    def analyze_local_image(self, image_path, sys_prompt):
        """
        Analyze a local image and return a description result.
        """
        agent = QwenVLMaxAgent(IAgentConfig(name="QwenVLMax", system_prompt="You are a helpful image analyzer.", model_name="qwen-vl-plus"))
        return agent.analyze(image_path, sys_prompt)