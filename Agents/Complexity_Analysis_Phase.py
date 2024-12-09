import os
from typing import TypedDict
from autogen import ConversableAgent
from AACLE.Agents import Base_Agent
from AACLE.utils import exact_json_from_text


class CorrectnessResult(TypedDict):
    time_complexity: str
    space_complexity: str


class Complexity_Analysis_Phase(Base_Agent):
    """复杂度分析阶段"""
    result_json: CorrectnessResult
    result_text: str

    def __init__(self, model_file,temperature, work_dir):
        super().__init__(model_file, temperature ,work_dir)
        # 创建一个Docker命令行代码执行器。
        self.user_agent = ConversableAgent(
            name="user_agent",
            llm_config={"config_list": [{"model": self.model_file, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",
            is_termination_msg=lambda msg: 'result is' in msg["content"].lower()
        )
        analysis_agent_prompt = """你是一个算法分析专家, 你负责分析给出伪代码算法的时间复杂度和空间复杂度. 
        1.如果你分析完了, 请按照指定的格式进行返回, 如: result is {"time_complexity": "O(nlogn)", "space_complexity": "O(n)"}
        """
        self.analysis_agent = ConversableAgent(
            name="analysis_agent",
            system_message=analysis_agent_prompt,
            llm_config={"config_list": [{"model": self.model_file, "api_key": os.environ["OPENAI_API_KEY"]}]},
        )

    def phase_run(self, input):
        result = self.user_agent.initiate_chat(
            self.analysis_agent, message=input + "我需要评估伪代码算法的时间和空间复杂度，你能帮我吗？"
        )
        self.result_text = result.chat_history[-1]['content']
        self.result_json = exact_json_from_text(self.result_text)
