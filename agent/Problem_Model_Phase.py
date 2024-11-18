import os
from autogen import ConversableAgent
from agent.Base_Agent import Base_Agent


class Problem_Model_Phase(Base_Agent):
    """问题建模阶段"""

    def phase_run(self, task_id,task_message):
        """问题建模阶段运行"""
        # self.def_agent() #定义各类agent

        prompt=f"""这是我输入的算法问题，请你解决这个问题：
                1. 问题描述：{task_message['question_desc']}
                2. 输入格式：{task_message['question_input_format']}
                3. 输出格式：{task_message['question_output_format']}
                4. 输入描述：{task_message['question_input_desc']}
                5. 输出描述：{task_message['question_output_desc']}
                6. 输入样例：{task_message['question_input_example']}
                7. 输出样例：{task_message['question_output_example']}"""

        result1 = self.AlgorithmSelectorAgent.initiate_chat(self.ModelAgent, message=prompt, max_turns=2)
        msg1=result1.chat_history[-1]["content"]
        msg1 = msg1.split("其他：")[0]

        result2=self.ModelAgent.initiate_chat(self.AssistantAgent,message=f"""输入算法的分析和数学描述： {msg1}""",max_turns=2)
        msg2 = result2.chat_history[-1]["content"]

        return msg1,msg2
