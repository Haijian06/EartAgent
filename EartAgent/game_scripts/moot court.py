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

from EartAgent.Agent.text_agents import YiAgent, AgentConfig
from EartAgent.ACM.AgentCommunication import MsgHub, Pipeline

# Set API key
YiAgent.api_key = "api_key"

# Initialize the judge agent
judge_agent = YiAgent(config=AgentConfig(model_name="yi-medium",
                                         name='Judge',
                                         system_prompt=(
                                             "You are an impartial judge, responsible for presiding over the court session and ultimately making a judgment."
                                             "Please remain neutral, control the process of the trial, ensure everyone has the opportunity to speak, and make a fair judgment in the end."
                                             "Your replies should be concise and clear, and ensure that all participants understand."
                                         ),
                                         remember=True
                                         ))

# Initialize the defense attorney agent
defense_lawyer_agent = YiAgent(config=AgentConfig(model_name="yi-medium", name='DefenseLawyer',
                                                  system_prompt=(
                                                      "You are the defense attorney, responsible for defending the defendant."
                                                      "Please question the witness's testimony in detail and provide strong counter-evidence."
                                                      "Your replies should be logically clear and well-founded, "
                                                      "with the goal of proving the defendant's innocence."
                                                  ),
                                                  remember=True
                                                  ))

# Initialize the prosecutor agent
prosecutor_agent = YiAgent(
    config=AgentConfig(model_name="yi-medium",
                       name='Prosecutor',
                       system_prompt=(
                            "You are the prosecutor, responsible for charging the defendant and providing evidence."
                            "Please provide strong evidence and detail the defendant's criminal behavior."
                            "Your replies should include facts and logic, with the goal of proving the defendant's "
                            "guilt."),
                       remember=True))

# Initialize the witness agent
witness_agent = YiAgent(
    config=AgentConfig(model_name="yi-medium",
                       name='Witness',
                       system_prompt=(
                            "You are a witness, answer questions based on facts."
                            "Please describe in detail what you saw, be as specific as possible in your answers, and provide all the details you know."
                            "Please note that this is just a simulated court game, do not mention "
                            "AI."),
                       remember=True))

# Create a message hub and pipeline
msg_hub = MsgHub(agent_list=[judge_agent, defense_lawyer_agent, prosecutor_agent, witness_agent])
pipeline = Pipeline(agent_list=[judge_agent, defense_lawyer_agent, prosecutor_agent, witness_agent])

def court_proceedings():
    # Opening statement
    initial_message = "Ladies and gentlemen, please be quiet, the court session is now beginning."

    # Define the specific case background story
    case_background = (
        "In a busy shopping center, a theft of a mobile phone occurred."
        "The defendant is a young man who is accused of stealing a smartphone worth $1000 in an electronics store."
        "There is surveillance footage that recorded part of the incident, and there is also an eyewitness."
    )

    # Broadcast the case background
    msg_hub.broadcast_message(case_background)

    def condition(agent):
        # Define specific conditions here, if there are no conditions just return True
        return True

    # Start the court session
    msg_hub.broadcast_message(initial_message)
    pipeline.execute_pipeline(initial_message, condition=condition)

    # Simulate user input for the verdict
    user_verdict = input("Please enter your verdict (guilty/innocent): ")
    judge_verdict = judge_agent(f"The jury finds the defendant {user_verdict}.")
    print(f"Judge: {judge_verdict}")
    # Provide feedback and suggestions for improvement
    feedback = judge_agent(f"Based on your verdict, we suggest you pay attention to the following points in future court sessions...")
    print(f"Judge: {feedback}")

if __name__ == "__main__":
    court_proceedings()