import autogen
from autogen import ConversableAgent
from agent.Base_Agent import Base_Agent


class Problem_Model_Phase(Base_Agent):
    """问题建模阶段"""

    def __init__(self, llm_config, model_file, work_dir, max_round=12):
        """初始化群聊代理和管理器"""
        super().__init__(model_file, work_dir)
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
