import os

import autogen
from autogen import ConversableAgent
from conf import ModelAgent_system_message, AlgorithmSelectorAgent_system_message, AssistantAgent_system_message


class Base_Agent():
    def __init__(self, model_file, temperature, work_dir):
        "指定设定调用的LLM，保存目录"
        self.ModelAgent = None  # 1.ModelAgent：分析问题并生成数学建模描述。
        self.AlgorithmSelectorAgent = None  # 2.AlgorithmSelectorAgent：根据问题类型建议适用的算法和数据结构。
        self.PseudocodeDesignerAgent = None  # 3.PseudocodeDesignerAgent：根据算法选择，编写对应的伪代码。
        self.VerificationAgent = None  # 4.VerificationAgent：验证伪代码的正确性，通过数学推导或逻辑推理确保算法逻辑无误。
        self.ComplexityAnalyzerAgent = None  # 5.ComplexityAnalyzerAgent：分析算法的时间复杂度和空间复杂度，并提供优化建议。
        self.CodeExecutorAgent = None  # 6.CodeExecutorAgent：根据伪代码编写Python程序
        self.CodeWriteAgent = None  # 7.CodeWriteAgent：执行Python程序，并验证输出结果。
        self.AssistantAgent = None  # 8.AssistantAgent：在前三个环节结束后，向环节主Agent提出针对性问题，同时问题需与具体环节内容紧密相关，并避免空泛提问。

        self.code_executor_agent = None
        self.code_writer_agent = None
        self.model_file = model_file
        self.temperature= temperature # 指定设定调用LLM的温度参数
        self.work_dir = work_dir  # 保存目录
        self.task_id = None
        os.environ["http_proxy"] = "http://localhost:7890"
        os.environ["https_proxy"] = "http://localhost:7890"
        os.environ["OPENAI_BASE_URL"] = "https://api.chatanywhere.org/v1"

        self.def_agent() # 定义每个环节自己的代理

    def def_agent(self):
        """
        定义每个环节自己的代理
        """

        ##### 定义第一个agent智能体 ModelAgent，用于分析算法问题，并生产数学建模描述 ####
        self.ModelAgent = ConversableAgent(
            name="ModelAgent",
            system_message=ModelAgent_system_message,
            llm_config={"config_list": [{"model": self.model_file,"temperature":self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
            # is_termination_msg=lambda msg: "terminate" in msg["content"],  # 如果检测到关键词“满意”，则终止对话
            # max_consecutive_auto_reply=2,#  # 代理连续两次自动回复后，将停止自动回复
        )


        ##### 定义第二个agent智能体 AlgorithmSelectorAgent，根据问题建议出适用的算法和数据结构 ####
        self.AlgorithmSelectorAgent = ConversableAgent(
            name="AlgorithmSelectorAgent",
            system_message=AlgorithmSelectorAgent_system_message,
            llm_config={"config_list": [{"model": self.model_file,"temperature":self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
            # is_termination_msg=lambda msg: "terminate" in msg["content"],  # 如果检测到关键词“满意”，则终止对话
            max_consecutive_auto_reply=1,  # # 代理连续两次自动回复后，将停止自动回复
        )




        ##### 定义第三个agent智能体 PseudocodeDesignerAgent，根据算法选择，编写对应的伪代码 ####

        ##### 定义第四个agent智能体 VerificationAgent，验证伪代码的正确性，通过数学推导或逻辑推理确保算法逻辑无误 ####

        ##### 定义第五个agent智能体 ComplexityAnalyzerAgent，分析算法的时间复杂度和空间复杂度，并提供优化建议 ####

        ##### 定义第六个agent智能体 CodeExecutorAgent，根据伪代码编写Python程序 ####

        ##### 定义第七个agent智能体 CodeWriteAgent，执行Python程序，并验证输出结果 ####


        ##### 定义第八个agent智能体 AssistantAgent，在前三个环节结束后，向环节主Agent提出针对性问题，同时问题需与具体环节内容紧密相关，并避免空泛提问 ####
        self.AssistantAgent = ConversableAgent(
            name="Assistant",
            system_message=AssistantAgent_system_message,
            llm_config={"config_list": [{"model": self.model_file, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
            max_consecutive_auto_reply=1,  # # 代理连续两次自动回复后，将停止自动回复
        )
