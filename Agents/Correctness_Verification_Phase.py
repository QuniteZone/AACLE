import os

from autogen import ConversableAgent, GroupChat, GroupChatManager
from AACLE.Agents.Base_Agent import Base_Agent




class Correctness_Verification_Phase(Base_Agent):
    """正确性验证阶段"""
    def phase_run(self,QueMath_desc,Algorithm_Select_list):
        prompt = f"""下面是我输入的算法内容描述和解题算法及结构，请你依据这些内容选择VerificationAgent来完成编写伪代码的任务！
                    算法内容描述：
                        problem_description: {QueMath_desc['problem_description']}
                        symbol_definition: {QueMath_desc['symbol_definition']}
                        mathematical_expression: {QueMath_desc['mathematical_expression']}
                        input_format:{QueMath_desc['input_format']}
                        input_example: {QueMath_desc['input_example']}
                        output_example: {QueMath_desc['output_example']}
                        output_format:{QueMath_desc['output_format']}

                    算法选择：
                        BaseInfo: {Algorithm_Select_list[0]}
                        Pseudocode: {Algorithm_Select_list[1]}
                        """
        allowed_transitions = {
            self.VerificationAgent: [self.ComplexityAnalyzerAgent_discussion,],
            self.ComplexityAnalyzerAgent_discussion: [self.VerificationAgent],
        }

        group_chat = GroupChat(
            agents=[self.VerificationAgent, self.ComplexityAnalyzerAgent_discussion],
            allowed_or_disallowed_speaker_transitions=allowed_transitions,
            speaker_transitions_type="allowed",
            messages=[],
            max_round=4,
        )

        group_chat_manager = GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": [{"model": self.model, "api_key": os.environ["OPENAI_API_KEY"]}]},
        )

        chat_result = self.ComplexityAnalyzerAgent_discussion.initiate_chat(
            group_chat_manager,
            message=prompt,
            summary_method="reflection_with_llm",
        )

        VerificationAgent_ResultData=[] #用于存储chat_result
        for result in chat_result.chat_history:
            if result['name']=='VerificationAgent':
                VerificationAgent_ResultData.append(result['content'])
        if len(VerificationAgent_ResultData)<2:
            assert False,"环节四未成功完成，请检查相关对话排错！"

        VerificationAgent_list=self.paras_str(VerificationAgent_ResultData[-1])
        print(f"########################################## 环节四已成功结束 ##########################################")
        # print(f"VerificationAgent_list: {VerificationAgent_list}")
        # VerificationAgent_list=[
        #     '（算法正确性验证部分）\n证明如下：（循环不变式法证明）\n1、初始化：首先证明在第一次循环迭代之前（当pq为空时），循环不变式成立。此时，起点到起点的距离为0，其他节点的距离为无穷大，优先队列中只有起点； // 初始化距离数组和优先队列\n2、保持：其次处理第二条性质：证明每次迭代保持循环不变式。在循环的每次迭代过程中，优先队列中始终存储当前最短路径的候选节点，并且更新节点的最短距离； // 更新节点的最短距离\n3、终止：最后研究在循环终止时发生了什么。当优先队列为空时，表示所有节点都已被访问，如果终点被访问过，则返回起点到终点的最短距离，否则返回-1表示无法到达终点。 // 处理终止条件',
        #     '成功']

        return VerificationAgent_list
