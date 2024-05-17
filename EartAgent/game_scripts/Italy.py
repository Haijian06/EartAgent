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

from dataclasses import dataclass
from typing import Dict, List, Type
import random
from EartAgent.Agent.text_agents import *

@dataclass
class Resident:
    name: str
    occupation: str
    agent_cls: Type[Agent]
    agent_config: AgentConfig

@dataclass
class TownConfig:
    num_residents: int = 8
    main_character_agent_cls: Type[Agent] = QwenAgent
    main_character_model_name: str = "qwen-turbo"
    resident_agent_cls: Type[Agent] = QwenAgent
    resident_model_name: str = "qwen-turbo"
    temperature: float = 0.7
    max_tokens: int = 256

class ItalianTown:
    def __init__(self, config: TownConfig):
        self.config = config
        self.residents: Dict[str, Resident] = {}
        self.setup_residents()

    def setup_residents(self):
        occupations = ["farmer", "fisherman", "merchant", "artisan", "chef"]
        self.residents = {
            "Main Character": Resident(
                name="Main Character",
                occupation="artist",
                agent_cls=self.config.main_character_agent_cls,
                agent_config=AgentConfig(
                    name="Main Character",
                    system_prompt="You are an adventurous artist who loves to travel and experience different cultures. You are vacationing in a small town in Italy, hoping to gain inspiration for your work.",
                    model_name=self.config.main_character_model_name,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens,
                ),
            ),
            **{
                f"Resident{i}": Resident(
                    name=f"Resident{i}",
                    occupation=random.choice(occupations),
                    agent_cls=self.config.resident_agent_cls,
                    agent_config=AgentConfig(
                        name=f"Resident{i}",
                        system_prompt=f"You are a {resident.occupation} living in this small town. You love the lifestyle here and are happy to share your experiences and insights with visiting travelers.",
                        model_name=self.config.resident_model_name,
                        temperature=self.config.temperature,
                        max_tokens=self.config.max_tokens,
                    ),
                )
                for i, resident in enumerate(
                    [
                        Resident(name=f"Resident{i + 1}", occupation=random.choice(occupations),
                                 agent_cls=self.config.resident_agent_cls, agent_config=None)
                        for i in range(self.config.num_residents)
                    ],
                    start=1,
                )
            },
        }

    def run_day(self):
        for resident in self.residents.values():
            agent = resident.agent_cls(resident.agent_config)
            print(f"\n{resident.name} ({resident.occupation}):")
            agent.remember_flag = True

            # Interaction between main character and residents
            if resident.name == "Main Character":
                print("You are wandering around the town, admiring the surroundings...")
                for other_resident in [r for r in self.residents.values() if r.name != "Main Character"]:
                    encounter = agent.chat(
                        f"You encounter a {other_resident.occupation}, {other_resident.name}. Do you want to talk to them and learn about life here?"
                    )
                    print(f"\nMain Character: {encounter}")
                    if "yes" in encounter.lower():
                        other_agent = other_resident.agent_cls(other_resident.agent_config)
                        other_agent.remember_flag = True
                        chat = agent.chat(
                            f"Nice to meet you! As a visitor, I am very interested in the lifestyle here. Can you tell me something about your daily life as a {other_resident.occupation}?"
                        )
                        print(f"\nMain Character: {chat}")
                        response = other_agent.chat(chat)
                        print(f"\n{other_resident.name}: {response}")

            # Interaction between residents
            else:
                daily_routine = agent.chat(f"As a {resident.occupation}, how do you spend your day?")
                print(f"\n{resident.name}: {daily_routine}")
                for other_resident in [
                    r for r in self.residents.values() if r.name != resident.name
                ]:
                    interact = agent.chat(
                        f"You encounter {other_resident.name}, a {other_resident.occupation}. Do you want to greet them and have a conversation?"
                    )
                    if "yes" in interact.lower():
                        other_agent = other_resident.agent_cls(other_resident.agent_config)
                        other_agent.remember_flag = True
                        chat = agent.chat(f"What do you plan to say to {other_resident.name}?")
                        print(f"\n{resident.name}: {chat}")
                        response = other_agent.chat(f"{resident.name} says to you: '{chat}'. What is your response?")
                        print(f"\n{other_resident.name}: {response}")

            agent.remember_flag = False

if __name__ == "__main__":
    QwenAgent.api_key = "your_api_key"
    town_config = TownConfig()
    italian_town = ItalianTown(town_config)

    for day in range(1, 4):
        print(f"\n=========== Day {day} ===========")
        italian_town.run_day()
