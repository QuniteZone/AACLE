from autogen import ConversableAgent
from AACLE.Agents.Base_Agent import Base_Agent





class Algorithm_Design_Phase(Base_Agent):
    """算法设计阶段"""
    def phase_run(self,QueMath_desc,Algorithm_Select):

        prompt = f"""下面是我输入的算法内容描述和解题算法及结构，请你依据这些内容选择x来完成编写伪代码的任务！
            算法内容描述：
                {QueMath_desc}
            算法选择：
                {Algorithm_Select}"""

        allowed_transitions = {
            self.AlgorithmSelectorAgent: [self.PseudocodeDesignerAgent_discussion, self.AssistantAgent],
            self.PseudocodeDesignerAgent_discussion: [self.AlgorithmSelectorAgent, ],
            self.AssistantAgent: [self.AlgorithmSelectorAgent],
        }

        group_chat = GroupChat(
            agents=[self.AlgorithmSelectorAgent, self.PseudocodeDesignerAgent_discussion, self.AssistantAgent],
            allowed_or_disallowed_speaker_transitions=allowed_transitions,
            speaker_transitions_type="allowed",
            messages=[],
            max_round=6,
        )

        group_chat_manager = GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": [{"model": self.model, "api_key": os.environ["OPENAI_API_KEY"]}]},
        )

        chat_result = self.AssistantAgent.initiate_chat(
            group_chat_manager,
            message=prompt,
            summary_method="reflection_with_llm",
        )









        print(f"Algorithm_Design_Phase: {Algorithm_Select}")
        print(f"Algorithm_Design_Phase: {QueMath_desc}")




        assert False ,'暂停中——qgz'
