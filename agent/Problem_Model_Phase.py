from run import tasks_list
import autogen
import os
from autogen import ConversableAgent
from agent.Base_Agent import Base_Agent


class Problem_Model_Phase(Base_Agent):
    """问题建模阶段"""

    def __init__(self, model_file, work_dir, task_list):
        """初始化群聊代理和管理器"""
        super().__init__(model_file, work_dir)
        self.max_round = 20
        self.task_list = task_list
        # 初始化代理
        self.assistant = ConversableAgent(
            name="Assistant",
            system_message="""你是助手，负责对数学模型的关键点进行提问，帮助新手理解模型。请按照一下格式提问：
            1. 模型的核心目的是什么
            2. 模型中的假设条件是什么？这些假设如何影响结果？如果假设不成立，结果会如何变化？
            3. 每个变量代表什么？它们是如何影响计算的？
            4. 计算步骤是如何进行的？每个步骤的目的是什么？
            5. 输出结果具体意味着什么？
            """
                           ,
            llm_config={"config_list": [{"model": self.model_file, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="TERMINATE",
        )
        self.model_agent = ConversableAgent(
            name="ModelAgent",
            system_message=f"""你负责根据问题建立数学模型，用数学符号清晰表达模型。
            请按照指定的格式返回模型：
            1. 请用数学符号表达问题的核心模型，例如公式、方程等。
            2. 列出用于模型构建的前提条件或假设。
            3. 定义模型中的所有变量，说明每个变量代表的意义。
            4. 给出问题的数学表达式
            5. 解释如何根据输入数据通过模型进行计算。
            6. 说明模型的输出结果是什么，以及如何解读这些输出。""",
            llm_config={"config_list": [{"model": self.model_file, "api_key": os.environ["OPENAI_API_KEY"]}]},
            is_termination_msg=lambda msg: "满意" in msg["content"],  # 如果检测到关键词“满意”，则终止对话
        )
        self.algorithm_selector_agent = ConversableAgent(
            name="AlgorithmSelectorAgent",
            system_message=f"""你负责评估ModelAgent提出的数学模型是否合理，并给出改进建议。如果你觉得模型合理，请回答“满意”。

                你的任务包括但不限于：
                1. 评估模型合理性：
                    确认模型是否符合问题的描述和目标。
                    检查模型中的假设是否合理，是否存在不必要或错误的假设。
                    确认模型公式的逻辑是否正确，是否符合数学推导。
                2. 提出改进建议：
                    如果发现模型有问题，提供具体的修改意见。例如，公式中的错误或不明确的变量定义。
                    如果模型过于复杂或冗余，建议简化模型。
                    如果缺少假设或考虑的因素不全面，建议补充。
                3. “满意”回复：
                    如果模型合理且没有问题，直接回复“满意”表示模型符合要求，不需要改进。

                请确保你的评估和建议清晰、具体，帮助优化数学模型。""",
            llm_config={"config_list": [{"model": self.model_file, "api_key": os.environ["OPENAI_API_KEY"]}]},
        )

        # 初始化群聊

    def phase_run(self, task_id):
        task_info=tasks_list[task_id]
        result1 = self.algorithm_selector_agent.initiate_chat(self.model_agent, message=f"""
    根据问题使用数学符号建立数学模型：
    1. 问题描述：{task_info['question_desc']}
    2. 输入格式：{task_info['question_input_format']}
    3. 输出格式：{task_info['question_output_format']}
    4. 输入描述：{task_info['question_input_desc']}
    5. 输出描述：{task_info['question_output_desc']}
    6. 输入样例：{task_info['question_input_example']}
    7. 输出样例：{task_info['question_output_example']}""", max_turns=20)

        msg1 = None
        msg2 = None
        # 倒叙遍历对话记录，返回ModelAgent的最后一次输出，则为最佳建模
        for msg in reversed(result1):
            if msg["sender"] == "ModelAgent":
                msg1=msg["content"]

        result2=self.assistant.initiate_chat(self.algorithm_selector_agent,message=f"""请根据下面的数学模型给出理解模型的关键点： msg1""",max_turns=2)

        for msg in reversed(result2):
            if msg["sender"] == "AlgorithmSelectorAgent":
                msg2=msg["content"]
            #返回一个列表，第一个元素为最优建模，第二个元素为理解建模的关键点
            return [msg1,msg2]
