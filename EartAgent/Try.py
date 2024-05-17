from EartAgent.Agent.text_agents import QwenAgent,AgentConfig
QwenAgent.api_key = "sk-dfee314ae3734edeb7df40b6f64e6c83"
agent_1 = QwenAgent(
    config=AgentConfig(name='Kerry',
                       system_prompt="",
                       ))
agent_1("hi")