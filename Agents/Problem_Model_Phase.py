import json
import os
import re

from autogen import ConversableAgent, GroupChat
from AACLE.Agents.Base_Agent import Base_Agent


class Problem_Model_Phase(Base_Agent):
    """问题建模阶段"""

    def phase_run(self, task_id, task_message):
        """问题建模阶段运行"""
        # self.def_agent() #定义各类agent

        prompt = f"""这是我输入的算法问题，请你解决这个问题：
1. 问题描述：{task_message['question_desc']}
2. 输入格式：{task_message['question_input_format']}
3. 输出格式：{task_message['question_output_format']}
4. 输入描述：{task_message['question_input_desc']}
5. 输出描述：{task_message['question_output_desc']}
6. 输入样例：{task_message['question_input_example']}
7. 输出样例：{task_message['question_output_example']}"""

        group_chat = GroupChat(
            agents=[self.ModelAgent, self.AlgorithmSelectorAgent_discussion, self.ModelAgent_discussion],
            messages=[],
            max_round=6,
        )

        from autogen import GroupChatManager

        group_chat_manager = GroupChatManager(
            groupchat=group_chat,
            llm_config={"config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}]},
        )

        chat_result = self.ModelAgent.initiate_chat(
            group_chat_manager,
            message=prompt,
            summary_method="reflection_with_llm",
        )

        # TODO: 解析chat_result，筛选出构建的模型，和所用的算法
        math_model_json = {
            "problem_description": "在一个城市的交通网络中，给定 N 个交叉路口和若干条道路，求从起点到终点的最短绕行时间。因一条主要道路堵塞，该条道路在计算最短路径时被忽略。",
            "symbol_definition": "N: 交叉路口的总数; u: 起点交叉路口; v: 终点交叉路口; w: 道路通行时间; blocked_road: 被堵塞的道路编号; start: 起点编号; end: 终点编号; G: 图的邻接表表示; T: 最短通行时间; P: 优先队列（最小堆）用于Dijkstra算法的实现。",
            "mathematical_expressions": "G(u, v) = w: 表示从交叉路口 u 到 v 的通行时间为 w; T = min(T_i): 表示从起点到终点的最短通行时间; T = -1: 表示无法到达终点; P.push((T, v)): 将当前节点和通行时间加入优先队列。",
            "input_format": "N\nu1 v1 w1\nu2 v2 w2\n...\nblocked_road\nstart\nend\n注: 输入的道路信息需要包含所有交叉路口之间的连接关系。",
            "output_format": "正整数或 -1; 注: 当起点和终点之间没有可达路径时，返回 -1。",
            "input_example": "5\n0 1 4\n1 2 3\n0 3 2\n3 4 6\n2 4 5\n1\n0\n4",
            "output_example": "9",
            "algorithm": "Dijkstra算法",
            "data_structure": "优先队列（最小堆）",
        }

        return math_model_json
