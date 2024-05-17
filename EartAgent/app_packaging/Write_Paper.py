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
from typing import List
import logging


def write_paper(question: str, search: str, serpapi_api_key: str, agent_list: List):
    """
    Function to write a paper using AI agents.

    :param question: The user's question to guide the paper writing.
    :param search: Search keywords to retrieve relevant web information.
    :param serpapi_api_key: SerpAPI API key for web scraping.
    :param agent_list: List of AI agents used for paper writing.
    :return: None
    """
    try:
        # Create agent instances
        agents = agent_list
        primary_agent = agents[3]
        del agents[3]

        # Search for related information
        tool = UtilityTools()
        web_search_results = tool.search_crawler(
            api_key=serpapi_api_key,
            query=search,
            max_results=1,
            agent=primary_agent
        )

        # Initialize system prompt
        system_prompt = f'The user\'s question is: {question}\n'
        system_prompt += f'The relevant search results are: {web_search_results}\n'
        system_prompt += 'Based on this information, please help me complete a 5000-word paper.'

        # Agent interaction loop
        while True:
            agent_responses = []
            for agent in agents:
                response = agent.generate_response(system_prompt)
                agent_responses.append(response)
                system_prompt = response

            # User input
            user_input = input("Type 'exit' to end the discussion, or press Enter to continue: ").strip()
            if user_input.lower() == 'exit':
                logging.info("Discussion ended.")
                break

            # Add user input to system prompt
            system_prompt = f"User input: {user_input}\n" + system_prompt

        # Generate paper using primary agent
        paper_content = primary_agent.generate_paper(system_prompt)

        # Save the text as a Word document
        tool.write_docx(content=paper_content, file_path='From_the_paper_generated_by_Eartagent.docx')

        logging.info('The paper has been saved, file name: From_the_paper_generated_by_Eartagent.docx')

    except Exception as e:
        logging.error(f"An error occurred: {e}")




