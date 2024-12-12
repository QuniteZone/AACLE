import os
from AACLE.Agents.Base_Agent import Base_Agent


class Program_Execute_Phase(Base_Agent):
    """代码执行阶段"""

    def phase_run(self,QueMath_desc, Algorithm_Design_list):
        prompt = f'''你需要根据提供的算法数学基本描述和构建伪代码编写python程序解决该算法问题。你需要测试是否通过题目的输入示例。若没通过，不断修改代码直至完成！
                算法内容描述：
                        problem_description: {QueMath_desc['problem_description']}
                        symbol_definition: {QueMath_desc['symbol_definition']}
                        mathematical_expression: {QueMath_desc['mathematical_expression']}
                        input_format:{QueMath_desc['input_format']}
                        input_example: {QueMath_desc['input_example']}
                        output_example: {QueMath_desc['output_example']}
                        output_format:{QueMath_desc['output_format']}
                算法选择：
                        BaseInfo: {Algorithm_Design_list[0]}
                        Pseudocode: {Algorithm_Design_list[1]}'''
        ####调用代理完成任务
        chat_result = self.code_executor_agent.initiate_chat(
            self.code_writer_agent,
            message=prompt,
        )