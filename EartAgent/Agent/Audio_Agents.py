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
import re
from http import HTTPStatus
import dashscope
from typing import Optional
from abc import ABC, abstractmethod
from dashscope.audio.tts import SpeechSynthesizer




class AudioAgentConfig:
    """
    Basic configuration information for audio agents
    """

    def __init__(self, system_prompt: str, model_name: str = 'qwen-audio-turbo'):
        self.system_prompt = system_prompt
        self.model_name = model_name


class AudioAgent(ABC):
    """
    Abstract base class for audio recognition agents
    """

    def __init__(self, config: AudioAgentConfig):
        self.config = config

    @abstractmethod
    def chat(self, audio_file: str) -> str:
        """
        Abstract method for processing audio recognition requests
        """
        pass

    def __call__(self, audio_file: str) -> str:
        response = self.chat(audio_file)
        # self.speak(response)
        return response

    def speak(self, response: str):
        """
        Output the agent's response
        """
        print(f"Audio content: {response}")


class QwenAudioAgent(AudioAgent):
    """
    Agent using Dashscope's Qwen model for audio recognition
    """
    api_key = None  # Class attribute to store API key

    def __init__(self, config: AudioAgentConfig):
        super().__init__(config)

    def chat(self, audio_file: str) -> str:
        dashscope.api_key = QwenAudioAgent.api_key  # Use class attribute as API key
        messages = [
            {
                "role": "user",
                "content": [
                    {"audio": f"file://{audio_file}"},
                    {"text": self.config.system_prompt}
                ]
            }
        ]
        response = dashscope.MultiModalConversation.call(model=self.config.model_name, messages=messages)

        if response.status_code == HTTPStatus.OK:
            text = response.output.choices[0].message.content[0]['text']
            match = re.search(r'"(.*?)"', text)

            if match:
                extracted_text = match.group(1)
                return extracted_text
            else:
                print("No content matched")
        else:
            print(response.code)
            print(response.message)

        return ""


class SambertAgent(AudioAgent):
    """
    Agent using Dashscope's Sambert speech synthesis
    """
    api_key = None  # Class attribute to store API key

    def __init__(self, config: AudioAgentConfig):
        super().__init__(config)

    def chat(self, sys_prompt: str):
        sys_prompt=self.config.system_prompt+sys_prompt
        # print(sys_prompt)
        dashscope.api_key = SambertAgent.api_key
        result = SpeechSynthesizer.call(model='sambert-zhichu-v1',
                                        text=sys_prompt,
                                        sample_rate=48000)
        if result.get_audio_data() is not None:
            return result.get_audio_data()