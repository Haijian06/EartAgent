from EartAgent.Agent.text_agents import QwenAgent,AgentConfig
QwenAgent.api_key = "your_api_key"
agent_1 = QwenAgent(
    config=AgentConfig(name='Kerry',
                       system_prompt="",
                       ))
agent_1("hi")
