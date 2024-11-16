import os
import tempfile
import autogen
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor, DockerCommandLineCodeExecutor

class Base_Agent():
    def __init__(self, model_file, work_dir):
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
        self.work_dir = work_dir  # 保存目录
        self.task_id = None
        # os.environ["http_proxy"] = "http://localhost:7890"
        # os.environ["https_proxy"] = "http://localhost:7890"
        os.environ["OPENAI_BASE_URL"] = "https://api.chatanywhere.org/v1"
    def def_agent(self):
        """
        定义每个环节自己的代理代理
        """

        ##### 定义第一个agent智能体 ModelAgent，用于分析算法问题，并生产数学建模描述 ####
        ModelAgent_system_message = "你是一个专门进行算法问题分析，并生成数学建模描述的代理"
        ModelAgent = ConversableAgent(
            name="ModelAgent",
            system_message=ModelAgent_system_message,
            llm_config={"config_list": [{"model": self.model_file, "api_key": os.environ["OPENAI_API_KEY"]}]},
        )


        ##### 定义第二个agent智能体 AlgorithmSelectorAgent，根据问题建议出适用的算法和数据结构 ####
        AlgorithmSelectorAgent_system_message = "你是一个根据算法问题描述，来建议出解决该算法问题应该采取的合适算法和合适数据结构的代理"
        AlgorithmSelectorAgent = ConversableAgent(
            name="AlgorithmSelectorAgent",
            system_message=AlgorithmSelectorAgent_system_message,
            llm_config={"config_list": [{"model": self.model_file, "api_key": os.environ["OPENAI_API_KEY"]}]},
        )
        user_proxy = autogen.UserProxyAgent(
            name="User_proxy",
            system_message="你是用户代理，用于发起对话。",
            human_input_mode="TERMINATE",
            #关闭人类输入
        )
        ##### 定义第三个agent智能体 PseudocodeDesignerAgent，根据算法选择，编写对应的伪代码 ####

        ##### 定义第四个agent智能体 VerificationAgent，验证伪代码的正确性，通过数学推导或逻辑推理确保算法逻辑无误 ####

        ##### 定义第五个agent智能体 ComplexityAnalyzerAgent，分析算法的时间复杂度和空间复杂度，并提供优化建议 ####

        ##### 定义第六个agent智能体 CodeExecutorAgent，根据伪代码编写Python程序 ####

        ##### 定义第七个agent智能体 CodeWriteAgent，执行Python程序，并验证输出结果 ####

        ##### 定义第八个agent智能体 AssistantAgent，在前三个环节结束后，向环节主Agent提出针对性问题，同时问题需与具体环节内容紧密相关，并避免空泛提问 ####


        #### 将各个代理用变量存储 ####
        self.ModelAgent = ModelAgent
        self.AlgorithmSelectorAgent = AlgorithmSelectorAgent


class Problem_Model_Phase(Base_Agent):
    """问题建模阶段"""

    def __init__(self, llm_config, max_round=12):
        """初始化群聊代理和管理器"""
        self.llm_config = llm_config
        self.max_round = max_round

        # 初始化代理
        self.user_proxy = autogen.UserProxyAgent(
            name="User_proxy",
            system_message="你是用户，负责描述问题。",
            human_input_mode="TERMINATE",
        )
        self.model_agent = autogen.AssistantAgent(
            name="ModelAgent",
            system_message="你负责根据用户描述建立数学模型，用数学符号清晰表达模型。",
            llm_config=llm_config,
            is_termination_msg=lambda msg: "满意" in msg["content"],#如果检测到关键词“满意”，则终止对话
        )
        self.algorithm_selector_agent = autogen.AssistantAgent(
            name="AlgorithmSelectorAgent",
            system_message="你负责评估ModelAgent提出的数学模型是否合理，并给出改进建议，如果你感觉模型合理，请回答“满意”。",
            llm_config=llm_config,
        )

        # 初始化群聊
        self.groupchat = autogen.GroupChat(
            agents=[self.user_proxy, self.model_agent, self.algorithm_selector_agent],
            messages=[],
            max_round=max_round,
        )
    #定义函数，选择发言顺序
    def turn_select(self,last_speaker,groupchat):


        if last_speaker is self.model_agent:
            return self.algorithm_selector_agent

        else:
            return self.model_agent

        #三种情况：如果上一个发言者是model_agent，则下一个让algorithm_selector_agent发言
        #如果上一个发言者是user_proxy，则下一个让model_agent发言
        #如果上一个发言者是user_proxy，则下一个让model_agent发言
        #后两个情况合并在一起



    def phase_run(self,task_description):
        groupchat = autogen.GroupChat(agents=[self.user_proxy, self.model_agent, self.algorithm_selector_agent], messages=[], max_round=12,speaker_selection_method=self.turn_select,)
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)

        self.user_proxy.initiate_chat(
            manager, message=f"根据以下描述使用数学符号建立数学模型：{task_description}"
        )

        #倒叙遍历对话记录，返回ModelAgent的最后一次输出，则为最佳建模
        for msg in reversed(groupchat.messages):
            if msg["sender"] == "ModelAgent":
                return msg["content"]




class Algorithm_Selection_Phase(Base_Agent):
    """算法选择阶段"""



class Algorithm_Design_Phase(Base_Agent):
    """算法设计阶段"""
    def phase_run(self):
        pass


class Correctness_Verification_Phase(Base_Agent):
    """正确性验证阶段"""
    def phase_run(self):
        pass


class Complexity_Analysis_Phase(Base_Agent):
    """复杂度分析阶段"""
    def phase_run(self):
        pass


class Program_Execute_Phase(Base_Agent):
    """代码执行阶段"""
    def phase_run(self):
        pass




class AutoGen():
    def __init__(self, model_file, work_dir):
        self.Problem_Model_Phase = Problem_Model_Phase(model_file, work_dir)  #创建问题建模阶段对象
        self.Algorithm_Selection_Phase = Algorithm_Selection_Phase(model_file, work_dir) #创建算法选择阶段对象
        self.Algorithm_Design_Phase = Algorithm_Design_Phase(model_file, work_dir) #创建算法设计阶段对象
        self.Correctness_Verification_Phase = Correctness_Verification_Phase(model_file, work_dir) #创建正确性验证阶段对象
        self.Complexity_Analysis_Phase = Complexity_Analysis_Phase(model_file, work_dir) #创建复杂度分析阶段对象
        self.Program_Execute_Phase = Program_Execute_Phase(model_file, work_dir) #创建代码执行阶段对象
        self.task_id = None  # 保存任务id

        pass

    def run(self, task_id, task_description):
        self.task_id = task_id  # 保存任务id
        ######################## 注意注意 前三个环节增加了智能体Agent自问自答环节 #######################
        self.is_satisfactory=False
        ####问题建模阶段
        self.Problem_Model_Phase.phase_run()
        # 该环节输出，作为下一阶段的输入！

        ####算法选择阶段
        self.Algorithm_Selection_Phase.phase_run()

        ####算法设计阶段
        self.Algorithm_Design_Phase.phase_run()
        # 该环节输出，作为下一阶段的输入！

        ####正确性验证阶段
        self.Correctness_Verification_Phase.phase_run()
        # 该环节输出，作为下一阶段的输入！

        ####复杂度分析阶段
        self.Complexity_Analysis_Phase.phase_run()
        # 该环节输出，作为下一阶段的输入！

        ####代码执行阶段
        self.Program_Execute_Phase.phase_run()



        final_result="最终输出结果"
        return final_result

