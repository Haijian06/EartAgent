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

class AgentCommunication:
    def __init__(self, agent_list=None):
        """Initialize the communication system with an optional list of agents."""
        self.agents = agent_list if agent_list else []

    def add_agent(self, agent):
        """Add a new agent to the communication system."""
        if agent not in self.agents:
            self.agents.append(agent)
            print(f"Agent {agent.config.name} added to the system.")
        else:
            print(f"Agent {agent.config.name} is already in the system.")

    def remove_agent(self, agent_name):
        """Remove an agent from the communication system by name."""
        self.agents = [agent for agent in self.agents if agent.config.name != agent_name]
        print(f"Agent {agent_name} removed from the system.")

    def broadcast_message(self, message):
        """Broadcast a message to all agents in the system."""
        print(f"Broadcasting message: {message}")
        for agent in self.agents:
            try:
                agent(message)
            except Exception as e:
                print(f"Error broadcasting message to {agent.config.name}: {e}")

    def execute_pipeline(self):
        """Execute the response pipeline of agents."""
        raise NotImplementedError("This method should be implemented by subclasses.")

class MsgHub(AgentCommunication):
    def __init__(self, agent_list=None):
        """Initialize the message hub with an optional list of agents."""
        super().__init__(agent_list)

    def execute_pipeline(self):
        """Execute each agent's response generation in sequence."""
        for agent in self.agents:
            try:
                message = f"Message to {agent.config.name}"
                agent(message)
                self.broadcast_message(message)
            except Exception as e:
                print(f"Error in agent {agent.config.name} pipeline: {e}")

class Pipeline(AgentCommunication):
    def __init__(self, agent_list=None):
        """Initialize the pipeline with an optional list of agents."""
        super().__init__(agent_list)

    def execute_pipeline(self, initial_message, condition=None):
        """Execute each agent's response generation based on a condition, passing the message sequentially."""
        message = initial_message
        user_input = ''
        while True:
            for agent in self.agents:
                try:
                    if condition is None or condition(agent):
                        message = agent(user_input + message)
                except Exception as e:
                    print(f"Error in agent {agent.config.name} conditional pipeline: {e}")
            user_input = input()
            if user_input == 'exit':
                print("Discussion ended")
                break
        return message