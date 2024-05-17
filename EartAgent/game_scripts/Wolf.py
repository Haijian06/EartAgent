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
from typing import List, Optional, Type
import random

from EartAgent.Agent.text_agents import *


@dataclass
class GameConfig:
    num_villagers: int = 2
    num_wolves: int = 1
    num_seers: int = 1
    agent_cls: Type[Agent] = ClaudeAgent  # Default to using ClaudeAgent


class WerewolfGame:
    def __init__(self, config: GameConfig):
        self.config = config
        self.players = []
        self.dead_players = []
        self.day = True
        self.discussion_history = []
        self.setup_players()

    def setup_players(self):
        villagers = [self.config.agent_cls(config=AgentConfig(name=f'Villager{i}',
                                                              system_prompt="You are a villager. Your goal is to collaborate with other villagers to identify and expel the werewolves from the village."))
                     for i in range(self.config.num_villagers)]
        wolves = [self.config.agent_cls(
            config=AgentConfig(name=f'Wolf{i}', system_prompt="You are a werewolf. Your goal is to secretly kill all the villagers without being identified."))
                  for i in range(self.config.num_wolves)]
        seers = [self.config.agent_cls(
            config=AgentConfig(name=f'Seer{i}', system_prompt="You are a seer. You can verify the identity of other players to help the villagers identify the werewolves."))
                 for i in range(self.config.num_seers)]
        self.players = villagers + wolves + seers
        random.shuffle(self.players)

    def night_phase(self):
        for player in self.players:
            if 'Wolf' in player.config.name:
                victim = random.choice([p for p in self.players if 'Villager' in p.config.name])
                wolf_action = player.chat(
                    f'Night has fallen. Who should we attack? Available villagers: {[p.config.name for p in self.players if "Villager" in p.config.name]}')
                self.discussion_history.append(f'{player.config.name} says: {wolf_action}')
                print(wolf_action)
            elif 'Seer' in player.config.name:
                checked_player = random.choice(self.players)
                seer_action = player.chat(
                    f'Night has fallen. Whose identity do you want to verify? Available players: {[p.config.name for p in self.players]}')
                self.discussion_history.append(f'{player.config.name} says: {seer_action}')
                print(seer_action)
                if 'Wolf' in checked_player.config.name:
                    role = 'werewolf'
                else:
                    role = 'villager'
                seer_reveal = player.chat(f'You checked {checked_player.config.name}. Their identity is {role}.')
                self.discussion_history.append(f'{player.config.name} says: {seer_reveal}')
                print(seer_reveal)

    def day_phase(self):
        for player in self.players:
            player_action = player.chat(
                f'A new day begins. What happened last night? {" ".join(self.discussion_history)} Based on this information, who do you suspect is a werewolf?')
            self.discussion_history.append(f'{player.config.name} says: {player_action}')
            print(player_action)

        # Simulate voting results
        vote_counts = {}
        for player in [p for p in self.players if 'Villager' in p.config.name]:
            suspect = player.chat(
                f'It is time to vote to expel a suspected werewolf. Based on previous discussions, who do you suspect is a werewolf? Available players: {[p.config.name for p in self.players]}')
            self.discussion_history.append(f'{player.config.name} votes: {suspect}')
            vote_counts[suspect] = vote_counts.get(suspect, 0) + 1

        to_be_expelled = max(vote_counts, key=vote_counts.get)
        expelled_player = next((p for p in self.players if p.config.name == to_be_expelled), None)
        if expelled_player:
            self.players.remove(expelled_player)
            self.dead_players.append(expelled_player)
            print(f'After the vote, {expelled_player.config.name} was expelled from the village.')

    def game_over(self):
        wolves = [p for p in self.players if 'Wolf' in p.config.name]
        villagers = [p for p in self.players if 'Villager' in p.config.name]
        if not wolves:
            print("Villagers win!")
            return True
        elif len(wolves) >= len(villagers):
            print("Werewolves win!")
            return True
        return False

def main(game_config):
    game = WerewolfGame(config=game_config)
    round_counter = 1
    while not game.game_over():
        print(f"\n---------- Round {round_counter} ----------")
        if game.day:
            print("Day Phase - Villagers discuss and vote to expel suspected werewolves")
            game.day_phase()
            game.day = False  # End day, start night
        else:
            print("Night Phase - Werewolves choose their target, seers verify identities")
            game.night_phase()
            game.day = True  # End night, start day

        round_counter += 1  # Increment round counter

    print("\nGame Over")
    # Print final surviving players
    print("Surviving players:")
    for player in game.players:
        print(f"{player.config.name}")
    print("Eliminated players:")
    for dead_player in game.dead_players:
        print(f"{dead_player.config.name}")


if __name__ == '__main__':
    # Run the game
    # Using QwenAgent
    QwenAgent.api_key = "your_api_key"
    qwen_game_config = GameConfig(num_villagers=3, num_wolves=2, num_seers=1, agent_cls=QwenAgent)
    main(qwen_game_config)
