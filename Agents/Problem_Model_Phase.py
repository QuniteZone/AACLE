import json
import os
import re
from autogen import ConversableAgent, GroupChat
from AACLE.Agents.Base_Agent import Base_Agent
from autogen import GroupChatManager

class Problem_Model_Phase(Base_Agent):
    """问题建模阶段"""

    def phase_run(self, task_id, task_message):
        """问题建模阶段运行"""
        # self.def_agent() #定义各类agent

        prompt = f"""这是我输入的算法问题，请你解决这个问题，我需要你先选择ModelAgent来完成任务。：
                1. 问题描述：{task_message['question_desc']}
                2. 输入格式：{task_message['question_input_format']}
                3. 输出格式：{task_message['question_output_format']}
                4. 输入描述：{task_message['question_input_desc']}
                5. 输出描述：{task_message['question_output_desc']}
                6. 输入样例：{task_message['question_input_example']}
                7. 输出样例：{task_message['question_output_example']}"""

        allowed_transitions = {
            self.ModelAgent: [self.AlgorithmSelectorAgent_discussion,self.AssistantAgent],
            self.AlgorithmSelectorAgent_discussion: [self.ModelAgent,],
            self.AssistantAgent: [self.ModelAgent],
        }

        group_chat = GroupChat(
            agents=[self.ModelAgent, self.AlgorithmSelectorAgent_discussion, self.AssistantAgent],
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

        ModelAgent_ResultData=[] #用于存储chat_result
        for result in chat_result.chat_history:
            if result['name']=='ModelAgent':
                ModelAgent_ResultData.append(result['content'])
        if len(ModelAgent_ResultData)<3:
            assert False,"环节一未成功完成，请检查相关对话排错！"


        print(f"ModelAgent_ResultData:{ModelAgent_ResultData[1]}")
        QueMath_desc= self.load_json(ModelAgent_ResultData[1])
        key_question = self.load_json(ModelAgent_ResultData[2])

        print(f"########################################## 环节一已成功结束 ##########################################")
        # print(f"QueMath_desc:{QueMath_desc}")
        # print(f"key_question:{key_question}")
        """
        QueMath_desc:{'problem_description': '一个城市的交通网络由多个交叉路口和道路组成。由于某条主要道路发生了交通堵塞，你需要找到从你的起点到目的地的最短绕行时间。', 'symbol_definition': 'N表示交叉路口的总数，编号为0到n-1。每行包含三个整数u v w，表示从交叉路口u到交叉路口v的道路通行时间为w。blocked_road表示被堵塞道路在输入中的编号，start表示起点的编号，end表示终点的编号。', 'mathematical_expression': '找到从起点到终点的最短通行时间，如果无法到达终点，返回-1。可以使用Dijkstra算法来解决，该算法适用于解决单源最短路径问题。在实现Dijkstra算法时，使用优先队列（Priority Queue）来维护当前最短路径的候选节点，以提高算法效率。', 'input_format': '输入的第一行为一个整数N，表示交叉路口的总数，编号为0到n-1。接下来若干行，每行包含三个整数u v w，表示从交叉路口u到交叉路口v的道路通行时间为w。倒数第3行：一个整数blocked_road，表示被堵塞道路在输入中的编号（从0开始编号）。倒数第2行：一个整数start，表示起点的编号。最后一行：一个整数end，表示终点的编号。', 'input_example': "['5\\n0 1 4\\n1 2 3\\n0 3 2\\n3 4 6\\n2 4 5\\n1\\n0\\n4']", 'output_format': '返回一个正整数或-1'}
        key_question:{'problem_1': '在使用Dijkstra算法解决最短路径问题时，为什么选择使用优先队列（Priority Queue）来维护当前最短路径的候选节点？优先队列相对于普通队列的优势是什么？', 'answer1': '在Dijkstra算法中，使用优先队列可以快速找到当前最短路径的节点，减少不必要的遍历。优先队列能够根据节点的权值（距离）进行排序，每次取出权值最小的节点，确保每次处理的节点是当前最短路径的候选节点。相比普通队列，优先队列的插入和删除操作的时间复杂度更低，能够提高算法的效率。', 'problem_2': '在Dijkstra算法中，如何处理被堵塞的道路？被堵塞的道路会对最终的最短通行时间产生什么影响？', 'answer2': '在Dijkstra算法中，处理被堵塞的道路可以通过将被堵塞道路的权值设置为一个较大的值，例如无穷大，使得算法不会选择该道路作为最短路径的一部分。被堵塞的道路会导致算法无法通过该道路到达目的地，可能会影响最终的最短通行时间。如果被堵塞的道路是唯一的通往目的地的道路，那么最终的最短通行时间可能会变为无穷大，表示无法到达目的地。'}
        """

        return QueMath_desc, key_question
