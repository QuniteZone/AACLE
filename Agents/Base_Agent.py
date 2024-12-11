import json
import os
import re

import autogen
from autogen import ConversableAgent, ModelClient
from AACLE.conf import ModelAgent_system_message, AlgorithmSelectorAgent_system_message, AssistantAgent_system_message, \
    ModelAgent_system_message_discussion, AlgorithmSelectorAgent_system_message_discussion, \
    PseudocodeDesignerAgent_system_message, PseudocodeDesignerAgent_system_message_discussion, \
    VerificationAgent_system_message, VerificationAgent_system_message_discussion, \
    ComplexityAnalyzerAgent_system_message, ComplexityAnalyzerAgent_system_message_discussion, \
    CodeWriteAgent_system_message, CodeWriteAgent_system_message_discussion, CodeExecutorAgent_system_message, \
    CodeExecutorAgent_system_message_discussion


class Base_Agent():
    def __init__(self, model, temperature, work_dir):
        "指定设定调用的LLM，保存目录"
        self.ModelAgent = None  # 1.ModelAgent：分析问题并生成数学建模描述。
        self.AlgorithmSelectorAgent = None  # 2.AlgorithmSelectorAgent：根据问题类型建议适用的算法和数据结构。
        self.PseudocodeDesignerAgent = None  # 3.PseudocodeDesignerAgent：根据算法选择，编写对应的伪代码。
        self.VerificationAgent = None  # 4.VerificationAgent：验证伪代码的正确性，通过数学推导或逻辑推理确保算法逻辑无误。
        self.ComplexityAnalyzerAgent = None  # 5.ComplexityAnalyzerAgent：分析算法的时间复杂度和空间复杂度，并提供优化建议。
        self.CodeExecutorAgent = None  # 6.CodeExecutorAgent：根据伪代码编写Python程序
        self.CodeWriteAgent = None  # 7.CodeWriteAgent：执行Python程序，并验证输出结果。
        self.AssistantAgent = None  # 8.AssistantAgent：在前三个环节结束后，向环节主Agent提出针对性问题，同时问题需与具体环节内容紧密相关，并避免空泛提问。

        self.ModelAgent_discussion = None  # ModelAgent_discussion：作为一个用于参与讨论的ModelAgent
        self.AlgorithmSelectorAgent_discussion = None  # AlgorithmSelectorAgent_discussion：作为一个用于参与讨论的AlgorithmSelectorAgent
        self.PseudocodeDesignerAgent_discussion = None  # PseudocodeDesignerAgent_discussion：作为一个用于参与讨论的PseudocodeDesignerAgent

        self.code_executor_agent = None
        self.code_writer_agent = None
        self.model = model
        self.temperature= temperature # 指定设定调用LLM的温度参数
        self.work_dir = work_dir  # 保存目录
        self.task_id = None
        os.environ["http_proxy"] = "http://localhost:7890"
        os.environ["https_proxy"] = "http://localhost:7890"
        os.environ["OPENAI_BASE_URL"] = "https://api.chatanywhere.org/v1"

        self.def_agent() # 定义每个环节自己的代理



    def paras_str(self, paras):
        """解析###之间内容"""
        # Extract text between ### sections
        try:
            pattern = r"###\s*(.*?)\s*###"  # Regular expression to capture text between ###
            matches = re.findall(pattern, paras, re.DOTALL)  # DOTALL ensures multi-line matching
            return matches
        except:
            assert False, "解析错误"


    def load_json(self,text):
        """
        加载json，如果text中包含json代码块，则提取json代码块并加载
        :param text:
        :return:
        """
        try:
            return json.loads(text)
        except:

            json_pattern = re.compile(r"```(\s*json)?$(.*?)^```", re.MULTILINE | re.DOTALL)
            matches = re.findall(json_pattern, text)
            if len(matches) > 0:
                text_json = matches[0][1].strip()
            else:
                assert False,"没有找到JSON代码块"
            try:
                return json.loads(text_json)
            except:
                assert False,"JSON解析错误"

    def def_agent(self):
        """
        定义每个环节自己的代理
        """

        ############################### 定义第一个agent智能体 ModelAgent，用于分析算法问题，并生产数学建模描述 ####
        self.ModelAgent = ConversableAgent(
            name="ModelAgent",
            system_message=ModelAgent_system_message,
            llm_config={"config_list": [{"model": self.model,"temperature":self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
            # is_termination_msg=lambda msg: "terminate" in msg["content"],  # 如果检测到关键词“满意”，则终止对话
            # max_consecutive_auto_reply=2,#  # 代理连续两次自动回复后，将停止自动回复
        )

        ##### 定义第二个agent智能体 ModelAgent_discussion，作为一个用于参与讨论的ModelAgent####
        self.ModelAgent_discussion = ConversableAgent(
            name="ModelAgent_discussion",
            system_message=ModelAgent_system_message_discussion,
            llm_config={"config_list": [{"model": self.model,"temperature":self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
            # is_termination_msg=lambda msg: "terminate" in msg["content"],  # 如果检测到关键词“满意”，则终止对话
            # max_consecutive_auto_reply=2,#  # 代理连续两次自动回复后，将停止自动回复
        )



        ############################### 定义第二个agent智能体 AlgorithmSelectorAgent，根据问题建议出适用的算法和数据结构 ####
        self.AlgorithmSelectorAgent = ConversableAgent(
            name="AlgorithmSelectorAgent",
            system_message=AlgorithmSelectorAgent_system_message,
            llm_config={"config_list": [{"model": self.model,"temperature":self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
            is_termination_msg=lambda msg: "TERMINATE" in msg["content"],  # 如果检测到关键词“满意”，则终止对话
            # max_consecutive_auto_reply=1,  # # 代理连续两次自动回复后，将停止自动回复
        )

        ##### 定义第二个agent智能体 AlgorithmSelectorAgent_discussion，作为一个用于参与讨论的AlgorithmSelectorAgent ####
        self.AlgorithmSelectorAgent_discussion = ConversableAgent(
            name="AlgorithmSelectorAgent_discussion",
            system_message=AlgorithmSelectorAgent_system_message_discussion,
            llm_config={"config_list": [
                {"model": self.model, "temperature": self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
            # is_termination_msg=lambda msg: "TERMINATE" in msg["content"],  # 如果检测到关键词“满意”，则终止对话
            # max_consecutive_auto_reply=1,  # # 代理连续两次自动回复后，将停止自动回复
        )



        ############################### 定义第三个agent智能体 PseudocodeDesignerAgent，根据算法选择，编写对应的伪代码。####
        self.PseudocodeDesignerAgent = ConversableAgent(
            name="PseudocodeDesignerAgent",
            system_message=PseudocodeDesignerAgent_system_message,
            llm_config={"config_list": [
                {"model": self.model, "temperature": self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
            # is_termination_msg=lambda msg: "TERMINATE" in msg["content"],  # 如果检测到关键词“满意”，则终止对话
            # max_consecutive_auto_reply=1,  # # 代理连续两次自动回复后，将停止自动回复
        )

        ##### 定义第三个agent智能体 PseudocodeDesignerAgent_discussion，作为一个用于参与讨论的PseudocodeDesignerAgent ####
        self.PseudocodeDesignerAgent_discussion = ConversableAgent(
            name="PseudocodeDesignerAgent_discussion",
            system_message=PseudocodeDesignerAgent_system_message_discussion,
            llm_config={"config_list": [
                {"model": self.model, "temperature": self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
        )



        ############################### 定义第四个agent智能体 VerificationAgent，验证伪代码的正确性，通过数学推导或逻辑推理确保算法逻辑无误####
        self.VerificationAgent = ConversableAgent(
            name="VerificationAgent",
            system_message=VerificationAgent_system_message,
            llm_config={"config_list": [
                {"model": self.model, "temperature": self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",
        )

        ##### 定义第四个agent智能体 VerificationAgent_discussion，作为一个用于参与讨论的 VerificationAgent ####
        self.VerificationAgent_discussion = ConversableAgent(
            name="VerificationAgent_discussion",
            system_message=VerificationAgent_system_message_discussion,
            llm_config={"config_list": [
                {"model": self.model, "temperature": self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",
        )




        ############################### 定义第五个agent智能体 ComplexityAnalyzerAgent，分析算法的时间复杂度和空间复杂度，并提供优化建议 ####
        self.ComplexityAnalyzerAgent = ConversableAgent(
            name="ComplexityAnalyzerAgent",
            system_message=ComplexityAnalyzerAgent_system_message,
            llm_config={"config_list": [
                {"model": self.model, "temperature": self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",
        )

        ##### 定义第五个agent智能体 ComplexityAnalyzerAgent_discussion，作为一个用于参与讨论的 ComplexityAnalyzerAgent ####
        self.ComplexityAnalyzerAgent_discussion = ConversableAgent(
            name="ComplexityAnalyzerAgent_discussion",
            system_message=ComplexityAnalyzerAgent_system_message_discussion,
            llm_config={"config_list": [
                {"model": self.model, "temperature": self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",
        )




        ############################### 定义第六个agent智能体 CodeWriteAgent，根据伪代码编写Python程序 ####
        self.CodeWriteAgent = ConversableAgent(
            name="CodeWriteAgent",
            system_message=CodeWriteAgent_system_message,
            llm_config={"config_list": [
                {"model": self.model, "temperature": self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",
        )

        ##### 定义第六个agent智能体 CodeWriteAgent_discussion，作为一个用于参与讨论的 CodeWriteAgent ####
        self.CodeWriteAgent_discussion = ConversableAgent(
            name="CodeWriteAgent_discussion",
            system_message=CodeWriteAgent_system_message_discussion,
            llm_config={"config_list": [
                {"model": self.model, "temperature": self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",
        )


        ############################### 定义第七个agent智能体 CodeExecutorAgent，执行Python程序，并验证输出结果 ####
        self.CodeExecutorAgent = ConversableAgent(
            name="CodeExecutorAgent",
            system_message=CodeExecutorAgent_system_message,
            llm_config={"config_list": [
                {"model": self.model, "temperature": self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",
        )

        ##### 定义第七个agent智能体 CodeExecutorAgent_discussion，作为一个用于参与讨论的 CodeExecutorAgent ####
        self.CodeExecutorAgent_discussion = ConversableAgent(
            name="CodeExecutorAgent_discussion",
            system_message=CodeExecutorAgent_system_message_discussion,
            llm_config={"config_list": [
                {"model": self.model, "temperature": self.temperature, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",
        )

        ############################### 定义第八个agent智能体 AssistantAgent，在前三个环节结束后，向环节主Agent提出针对性问题，同时问题需与具体环节内容紧密相关，并避免空泛提问 ####
        self.AssistantAgent = ConversableAgent(
            name="Assistant",
            system_message=AssistantAgent_system_message,
            llm_config={"config_list": [{"model": self.model, "api_key": os.environ["OPENAI_API_KEY"]}]},
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
            # max_consecutive_auto_reply=1,  # # 代理连续两次自动回复后，将停止自动回复
            is_termination_msg=lambda msg: "TERMINATE" in msg["content"],  # 如果检测到关键词“满意”，则终止对话
        )
