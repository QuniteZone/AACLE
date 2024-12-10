import os

from autogen import ConversableAgent, GroupChat, GroupChatManager
from AACLE.Agents.Base_Agent import Base_Agent


class Algorithm_Selection_Phase(Base_Agent):
    """算法选择阶段"""
    def phase_run(self, task_message, ModelAgent_ResultData=None):

        prompt = f"""这是我输入的算法问题，请你解决这个问题，我需要你先选择AlgorithmSelectorAgent来完成任务。：
                        1. problem_description：{task_message['problem_description']}
                        2. symbol_definition：{task_message['symbol_definition']}
                        3. mathematical_expression：{task_message['mathematical_expression']}
                        4. input_format：{task_message['input_format']}
                        5. input_example：{task_message['input_example']}
                        6. output_format：{task_message['output_format']}"""

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


        AlgorithmAgent_ResultData=[] #用于存储chat_result
        for result in chat_result.chat_history:
            if result['name']=='AlgorithmSelectorAgent':
                AlgorithmAgent_ResultData.append(result['content'])
        if len(AlgorithmAgent_ResultData)<3:
            assert False,"环节一未成功完成，请检查相关对话排错！"
        Algorithm_Select, key_question = self.load_json(AlgorithmAgent_ResultData[1]), self.load_json(AlgorithmAgent_ResultData[2])


        print(f"########################################## 环节二已成功结束 ##########################################")
        # print(f"chat_result: {chat_result}")

        # print(f"Algorithm_Select: {Algorithm_Select}")
        # print(f"key_question: {key_question}")

        # Algorithm_Select={'data_structure': '优先队列（Priority Queue）',
        #                    'data_structure_example': 'struct Node { int vertex; int distance; };',
        #                    'data_structure_reason': '选择优先队列来维护当前最短路径的候选节点，因为Dijkstra算法需要不断更新最短路径，优先队列可以高效地找到当前最短路径的候选节点。',
        #                    'algorithm_type': '贪心算法', 'algorithm_name': 'Dijkstra算法',
        #                    'algorithm_idea': 'Dijkstra算法通过不断更新起点到各个节点的最短路径来找到最终的最短路径。具体来说，从起点开始，每次选择当前距离最短的节点进行松弛操作，更新其他节点的距离。重复这个过程直到所有节点都被访问。',
        #                    'algorithm_reason': '选择Dijkstra算法是因为它适用于解决单源最短路径问题，而且在实现Dijkstra算法时，使用优先队列可以提高算法效率。在实现Dijkstra算法时，可以添加对输入数据的合法性检查，考虑使用邻接表来表示图的结构，并可以使用已有的优先队列实现，如STL中的priority_queue，以提高算法的效率和减少重复工作。'}
        # key_question= {'problem_1': '对于Dijkstra算法中的松弛操作，你能详细解释一下具体是如何更新节点的距离吗？',
        #                'answer1': '在Dijkstra算法中的松弛操作是通过比较当前节点经过某条边到达相邻节点的距离和已知最短路径的距离之间的大小关系来更新节点的距离。具体来说，如果经过当前节点到达相邻节点的距离小于已知最短路径的距离，则更新相邻节点的距离为经过当前节点到达的距离。这样可以不断更新节点的最短路径，直到所有节点都被访问。',
        #                'problem_2': '在实现Dijkstra算法时，为什么建议使用邻接表来表示图的结构？这种数据结构有哪些优点？',
        #                'answer2': '建议使用邻接表来表示图的结构是因为邻接表可以更高效地存储稀疏图的连接关系。邻接表由一个数组和链表组成，数组的每个元素对应一个节点，链表存储与该节点相邻的节点及边的信息。使用邻接表可以节省空间，因为只存储实际存在的边，而且可以更快地访问节点的邻居节点，提高算法效率。',
        #                'problem_3': '你能进一步说明如何在Dijkstra算法的实现中添加对输入数据的合法性检查吗？这样的检查可以带来哪些好处？',
        #                'answer3': '在Dijkstra算法的实现中，可以添加对输入数据的合法性检查，例如检查起点和终点是否在有效范围内，检查道路通行时间是否为非负数等。这样的检查可以避免程序在处理不合法输入时出现意外错误，提高程序的健壮性和可靠性，同时可以提前发现输入数据的问题，减少调试时间。'}

        return Algorithm_Select, key_question