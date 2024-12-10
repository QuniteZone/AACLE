import os
import tempfile
import autogen
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor, DockerCommandLineCodeExecutor
from AACLE.Agents.Problem_Model_Phase import Problem_Model_Phase
from AACLE.Agents.Algorithm_Selection_Phase import Algorithm_Selection_Phase
from AACLE.Agents.Algorithm_Design_Phase import Algorithm_Design_Phase
from AACLE.Agents.Correctness_Verification_Phase import Correctness_Verification_Phase
# from AACLE.Agents.Complexity_Analysis_Phase import Complexity_Analysis_Phase
# from AACLE.Agents.Program_Execute_Phase import Program_Execute_Phase
import sys
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")
sys.path.append("../../../..")



class AACLE():
    def __init__(self, model,temperature, work_dir,bind_dir):
        self.bind_dir=bind_dir #绑定所需本地数据的目录，有需要自己拉去
        self.Problem_Model_Phase = Problem_Model_Phase(model, temperature,work_dir)  #创建问题建模阶段对象
        self.Algorithm_Selection_Phase = Algorithm_Selection_Phase(model, temperature,work_dir) #创建算法选择阶段对象
        self.Algorithm_Design_Phase = Algorithm_Design_Phase(model,temperature, work_dir) #创建算法设计阶段对象
        self.Correctness_Verification_Phase = Correctness_Verification_Phase(model,temperature,  work_dir) #创建正确性验证阶段对象
        # self.Complexity_Analysis_Phase = Complexity_Analysis_Phase(model,temperature, work_dir) #创建复杂度分析阶段对象
        # self.Program_Execute_Phase = Program_Execute_Phase(model,temperature,  work_dir) #创建代码执行阶段对象
        self.task_id = None  # 保存任务id

        pass

    def run(self, task_id, task_message):
        self.task_id = task_id  # 保存任务id
        ######################## 注意注意 前三个环节增加了智能体Agent自问自答环节 #######################
        self.is_satisfactory=False
        ####问题建模阶段
        # QueMath_desc, key_question1=self.Problem_Model_Phase.phase_run(task_id,task_message) #第一个算法问题数学建模，第二个为辅助理解建模的问题
        # print(f"QueMath_desc:{QueMath_desc}")
        # print(f"key_question1:{key_question1}")

        ####算法选择阶段
        QueMath_desc={
            'problem_description': '一个城市的交通网络由多个交叉路口和道路组成。由于某条主要道路发生了交通堵塞，你需要找到从你的起点到目的地的最短绕行时间。',
            'symbol_definition': 'N表示交叉路口的总数，编号为0到n-1。每行包含三个整数u v w，表示从交叉路口u到交叉路口v的道路通行时间为w。blocked_road表示被堵塞道路在输入中的编号，start表示起点的编号，end表示终点的编号。',
            'mathematical_expression': '找到从起点到终点的最短通行时间，如果无法到达终点，返回-1。可以使用Dijkstra算法来解决，该算法适用于解决单源最短路径问题。在实现Dijkstra算法时，使用优先队列（Priority Queue）来维护当前最短路径的候选节点，以提高算法效率。',
            'input_format': '输入的第一行为一个整数N，表示交叉路口的总数，编号为0到n-1。接下来若干行，每行包含三个整数u v w，表示从交叉路口u到交叉路口v的道路通行时间为w。倒数第3行：一个整数blocked_road，表示被堵塞道路在输入中的编号（从0开始编号）。倒数第2行：一个整数start，表示起点的编号。最后一行：一个整数end，表示终点的编号。',
            'input_example': "['5\\n0 1 4\\n1 2 3\\n0 3 2\\n3 4 6\\n2 4 5\\n1\\n0\\n4']",
            'output_format': '返回一个正整数或-1'}
        key_question1={
            'problem_1': '在使用Dijkstra算法解决最短路径问题时，为什么选择使用优先队列（Priority Queue）来维护当前最短路径的候选节点？优先队列相对于普通队列的优势是什么？',
            'answer1': '在Dijkstra算法中，使用优先队列可以快速找到当前最短路径的节点，减少不必要的遍历。优先队列能够根据节点的权值（距离）进行排序，每次取出权值最小的节点，确保每次处理的节点是当前最短路径的候选节点。相比普通队列，优先队列的插入和删除操作的时间复杂度更低，能够提高算法的效率。',
            'problem_2': '在Dijkstra算法中，如何处理被堵塞的道路？被堵塞的道路会对最终的最短通行时间产生什么影响？',
            'answer2': '在Dijkstra算法中，处理被堵塞的道路可以通过将被堵塞道路的权值设置为一个较大的值，例如无穷大，使得算法不会选择该道路作为最短路径的一部分。被堵塞的道路会导致算法无法通过该道路到达目的地，可能会影响最终的最短通行时间。如果被堵塞的道路是唯一的通往目的地的道路，那么最终的最短通行时间可能会变为无穷大，表示无法到达目的地。'}
        # Algorithm_Select, key_question2=self.Algorithm_Selection_Phase.phase_run(QueMath_desc)
        # print(f"Algorithm_Select:{Algorithm_Select}")
        # print(f"key_question2:{key_question2}")



        ####算法设计阶段
        Algorithm_Select={'data_structure': '优先队列（Priority Queue）',
                           'data_structure_example': 'struct Node { int vertex; int distance; };',
                           'data_structure_reason': '选择优先队列来维护当前最短路径的候选节点，因为Dijkstra算法需要不断更新最短路径，优先队列可以高效地找到当前最短路径的候选节点。',
                           'algorithm_type': '贪心算法', 'algorithm_name': 'Dijkstra算法',
                           'algorithm_idea': 'Dijkstra算法通过不断更新起点到各个节点的最短路径来找到最终的最短路径。具体来说，从起点开始，每次选择当前距离最短的节点进行松弛操作，更新其他节点的距离。重复这个过程直到所有节点都被访问。',
                           'algorithm_reason': '选择Dijkstra算法是因为它适用于解决单源最短路径问题，而且在实现Dijkstra算法时，使用优先队列可以提高算法效率。在实现Dijkstra算法时，可以添加对输入数据的合法性检查，考虑使用邻接表来表示图的结构，并可以使用已有的优先队列实现，如STL中的priority_queue，以提高算法的效率和减少重复工作。'}
        key_question2= {'problem_1': '对于Dijkstra算法中的松弛操作，你能详细解释一下具体是如何更新节点的距离吗？',
                       'answer1': '在Dijkstra算法中的松弛操作是通过比较当前节点经过某条边到达相邻节点的距离和已知最短路径的距离之间的大小关系来更新节点的距离。具体来说，如果经过当前节点到达相邻节点的距离小于已知最短路径的距离，则更新相邻节点的距离为经过当前节点到达的距离。这样可以不断更新节点的最短路径，直到所有节点都被访问。',
                       'problem_2': '在实现Dijkstra算法时，为什么建议使用邻接表来表示图的结构？这种数据结构有哪些优点？',
                       'answer2': '建议使用邻接表来表示图的结构是因为邻接表可以更高效地存储稀疏图的连接关系。邻接表由一个数组和链表组成，数组的每个元素对应一个节点，链表存储与该节点相邻的节点及边的信息。使用邻接表可以节省空间，因为只存储实际存在的边，而且可以更快地访问节点的邻居节点，提高算法效率。',
                       'problem_3': '你能进一步说明如何在Dijkstra算法的实现中添加对输入数据的合法性检查吗？这样的检查可以带来哪些好处？',
                       'answer3': '在Dijkstra算法的实现中，可以添加对输入数据的合法性检查，例如检查起点和终点是否在有效范围内，检查道路通行时间是否为非负数等。这样的检查可以避免程序在处理不合法输入时出现意外错误，提高程序的健壮性和可靠性，同时可以提前发现输入数据的问题，减少调试时间。'}
        self.Algorithm_Design_Phase.phase_run(QueMath_desc,Algorithm_Select)
        # 该环节输出，作为下一阶段的输入！



        assert False, '测试之中'




        ####正确性验证阶段
        self.Correctness_Verification_Phase.phase_run()
        # 该环节输出，作为下一阶段的输入！

        ####复杂度分析阶段
        # self.Complexity_Analysis_Phase.phase_run()
        # # 该环节输出，作为下一阶段的输入！
        #
        # ####代码执行阶段
        # self.Program_Execute_Phase.phase_run()



        final_result="最终输出结果"
        return final_result

