import json
import os

from autogen import ConversableAgent, GroupChat, GroupChatManager
from AACLE.Agents.Base_Agent import Base_Agent





class Algorithm_Design_Phase(Base_Agent):
    """算法设计阶段"""
    def phase_run(self,QueMath_desc,Algorithm_Select):

        prompt = f"""下面是我输入的算法内容描述和解题算法及结构，请你依据这些内容选择x来完成编写伪代码的任务！
            算法内容描述：
                problem_description: {QueMath_desc['problem_description']}
                symbol_definition: {QueMath_desc['symbol_definition']}
                mathematical_expression: {QueMath_desc['mathematical_expression']}
                input_format:{QueMath_desc['input_format']}
                input_example: {QueMath_desc['input_example']}
                output_example: {QueMath_desc['output_example']}
                output_format:{QueMath_desc['output_format']}
                
            算法选择：
                data_structure: {Algorithm_Select['data_structure']}
                data_structure_example: {Algorithm_Select['data_structure_example']}
                data_structure_reason: {Algorithm_Select['data_structure_reason']}
                algorithm_type:{Algorithm_Select['algorithm_type']}
                algorithm_name: {Algorithm_Select['algorithm_name']}
                algorithm_idea: {Algorithm_Select['algorithm_idea']}
                algorithm_reason: {Algorithm_Select['algorithm_reason']}
                """

        allowed_transitions = {
            self.PseudocodeDesignerAgent: [self.VerificationAgent_discussion, self.AssistantAgent],
            self.VerificationAgent_discussion: [self.PseudocodeDesignerAgent, ],
            self.AssistantAgent: [self.PseudocodeDesignerAgent],
        }

        group_chat = GroupChat(
            agents=[self.PseudocodeDesignerAgent, self.VerificationAgent_discussion, self.AssistantAgent],
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
        AlgorithmDesignAgent_ResultData=[] #用于存储chat_result
        for result in chat_result.chat_history:
            if result['name']=='PseudocodeDesignerAgent':
                AlgorithmDesignAgent_ResultData.append(result['content'])
                # print(f"AlgorithmDesignAgent_ResultData: {result['content']}")
        if len(AlgorithmDesignAgent_ResultData)<3:
            assert False,"环节三未成功完成，请检查相关对话排错！"

        Algorithm_Select_list=self.paras_str(AlgorithmDesignAgent_ResultData[-2])
        key_question=self.load_json(AlgorithmDesignAgent_ResultData[-1])



        print(f"########################################## 环节三已成功结束 ##########################################")
        # print(f"Algorithm_Select: {Algorithm_Select_list}")
        # print(f"key_question: {key_question}")

        # Algorithm_Select=[
        #     '1） 子问题定义：使用Dijkstra算法找到从起点到终点的最短通行时间。\n2） 根据Dijkstra算法的思想，每次选择当前距离最短的节点进行松弛操作，更新其他节点的距离，直到所有节点都被访问。\n    \\left. dist[v] = \\min\\left\\{dist[v], dist[u] + w(u, v)\\right\\}\\right.\n其中dist[v]表示起点到节点v的最短距离，w(u, v)表示节点u到节点v的边权重。\n3） 设交叉路口总数为N，起点编号为start，终点编号为end，被堵塞道路编号为blocked_road。\n4） 使用优先队列（Priority Queue）来维护当前最短路径的候选节点，以提高算法效率。',
        #     '// 初始化距离数组，起点到各节点的距离初始为无穷大\nfor i ← 0 to N-1\n    do\n        dist[i] ← INF  // 表示无穷大\ndist[start] ← 0  // 起点到自身的距离为0\n\n// 使用优先队列实现Dijkstra算法\npriority_queue<Node> pq\npq.push(Node(start, 0))\n\nwhile pq is not empty\n    do\n        Node cur ← pq.top()\n        pq.pop()\n        \n        if cur.vertex == end\n            then return dist[end]  // 已找到终点的最短距离\n        \n        if cur.vertex == blocked_road\n            then continue  // 被堵塞道路不考虑\n        \n        for each neighbor of cur.vertex\n            do\n                if dist[cur.vertex] + w(cur.vertex, neighbor) < dist[neighbor]\n                    then\n                        dist[neighbor] ← dist[cur.vertex] + w(cur.vertex, neighbor)\n                        pq.push(Node(neighbor, dist[neighbor]))\n                        \nreturn -1  // 无法到达终点']
        # key_question={'problem_1': '如何在算法中实现对输入数据的合法性检查？',
        #                'answer1': '在算法中实现对输入数据的合法性检查可以通过以下步骤：\n1. 在读取起点、终点和被堵塞道路编号后，检查它们是否在合法范围内（0到N-1）。\n2. 检查被堵塞道路编号是否在道路信息中存在，以确保输入的道路信息和被堵塞道路信息一致。\n3. 确保起点和终点不相同，避免出现起点和终点相同的情况。\n4. 如果输入数据不符合合法性要求，可以返回错误信息或采取其他处理方式。',
        #                'problem_2': '如何使用邻接表来表示图的结构以提高算法效率？',
        #                'answer2': '使用邻接表来表示图的结构可以提高算法效率，具体步骤如下：\n1. 创建一个数组，数组的每个元素是一个链表，链表中存储与该节点相邻的节点及对应的边权重。\n2. 遍历道路信息，将每条道路的起点、终点和权重信息存储到对应节点的链表中。\n3. 使用邻接表表示图的结构可以快速查找节点的邻居和对应的边权重，提高算法效率。',
        #                'problem_3': '如何利用STL中的priority_queue来优化算法，减少重复工作并提高效率？',
        #                'answer3': '利用STL中的priority_queue来优化算法可以通过以下方式：\n1. 定义一个自定义结构体Node，包含节点编号和距离信息，作为优先队列的元素。\n2. 将起点信息加入优先队列，并初始化起点到各节点的距禒为无穷大。\n3. 在每次取出距离最短的节点时，检查该节点是否已被访问，避免重复工作。\n4. 将更新后的节点信息加入优先队列，并更新距离数组。\n5. 使用STL中的priority_queue可以方便地实现优先队列的功能，减少手动维护队列的工作，提高算法效率。'}

        return Algorithm_Select_list,key_question