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

from EartAgent.Agent.text_agents import *
from EartAgent.Agent.images2text_agents import *
from EartAgent.utils.UT import UtilityTools

class WebsiteClone:
    def __init__(self, qwen_api_key: str, claude_api_key: str):
        self.qwen_api_key = qwen_api_key
        self.claude_api_key = claude_api_key
        self.utility_tools = UtilityTools()

    def clone_website(self, image_path: str, qwen_iterations: int, claude_iterations: int) -> str:
        dashscope.api_key = self.qwen_api_key
        qwen_agent = QwenVLMaxAgent(
            IAgentConfig(name="QwenVLMax", system_prompt="Analyze this image and generate HTML css js code.",
                        model_name="qwen-vl-max"))
        initial_code = qwen_agent.analyze(image_path, "Please look carefully at the layout and typography of the site without errors,Generate HTML css js code based on this image,")
        print("The first analyze-->", initial_code)
        refined_code = self.reflect_and_optimize1(initial_code, "Improve and optimize HTML css js code", qwen_agent, qwen_iterations)
        ClaudeAgent.api_key = self.claude_api_key
        claude_agent = ClaudeAgent(
            config=AgentConfig(name="Claude",
                               system_prompt="Refine this HTML code.",
                               model_name='claude-3-sonnet-20240229'))
        final_code = self.reflect_and_optimize2(refined_code, "Improve and optimize HTML css js code", claude_agent, claude_iterations)
        return final_code

    def reflect_and_optimize1(self, code: str, scenario: str, agent, iterations: int) -> str:
        current_code = code
        for i in range(iterations):
            prompt = f"Improve the following code for the scenario '{scenario}': '{current_code}'. Consider the functionality, aesthetics, and correctness.You look at the code based on the image to see if the code restores the image, if not it must be modified and you must write out all the code, writing the html, css, js code together"
            reflection = agent.analyze(image_path, prompt)
            current_code = reflection
            print(f"The {i+1} reflect by qwen-->", current_code)
        return current_code

    def reflect_and_optimize2(self, code: str, scenario: str, agent, iterations: int) -> str:
        current_code = code
        for i in range(iterations):
            prompt = f"Improve the following code for the scenario '{scenario}': '{current_code}'. Consider the functionality, aesthetics, and correctness.You continue to modify and optimize according to the code I give you and must write the entire code, putting together html, css, js code"
            reflection = agent.chat(prompt)
            current_code = reflection
            print(f"The {i + 1} reflect by claude-->", current_code)
        return current_code

