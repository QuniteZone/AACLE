import os
import tempfile
import autogen
from autogen import ConversableAgent
from autogen.coding import LocalCommandLineCodeExecutor, DockerCommandLineCodeExecutor
from agent.Problem_Model_Phase import Problem_Model_Phase
from agent.Algorithm_Selection_Phase import Algorithm_Selection_Phase
from agent.Algorithm_Design_Phase import Algorithm_Design_Phase
from agent.Correctness_Verification_Phase import Correctness_Verification_Phase
from agent.Complexity_Analysis_Phase import Complexity_Analysis_Phase
from agent.Program_Execute_Phase import Program_Execute_Phase
import sys
sys.path.append("..")
sys.path.append("../..")
sys.path.append("../../..")
sys.path.append("../../../..")



class AutoLearning():
    def __init__(self, model_file,temperature, work_dir,bind_dir):
        self.bind_dir=bind_dir #绑定所需本地数据的目录，有需要自己拉去
        self.Problem_Model_Phase = Problem_Model_Phase(model_file, temperature,work_dir)  #创建问题建模阶段对象
        self.Algorithm_Selection_Phase = Algorithm_Selection_Phase(model_file, temperature,work_dir) #创建算法选择阶段对象
        self.Algorithm_Design_Phase = Algorithm_Design_Phase(model_file,temperature, work_dir) #创建算法设计阶段对象
        self.Correctness_Verification_Phase = Correctness_Verification_Phase(model_file,temperature,  work_dir) #创建正确性验证阶段对象
        self.Complexity_Analysis_Phase = Complexity_Analysis_Phase(model_file,temperature, work_dir) #创建复杂度分析阶段对象
        self.Program_Execute_Phase = Program_Execute_Phase(model_file,temperature,  work_dir) #创建代码执行阶段对象
        self.task_id = None  # 保存任务id

        pass

    def run(self, task_id, task_message):
        self.task_id = task_id  # 保存任务id
        ######################## 注意注意 前三个环节增加了智能体Agent自问自答环节 #######################
        self.is_satisfactory=False
        ####问题建模阶段
        question_desc, key_question=self.Problem_Model_Phase.phase_run(task_id,task_message) #返回一个列表，第一个元素为最优建模，第二个元素为理解建模的应道问题
        print(f"question_desc:{question_desc}")
        print(f"key_question:{key_question}")



        ####算法选择阶段
        question_desc = '''问题描述：在智能交通系统中，城市的道路网络可以表示为一个无向图，图中的每条边代表一条双向道路，边的权重代表车辆在该路段的行驶时间。系统需要计算两辆车从各自的起点出发前往目的地的最优行驶路径，使行驶时间最短。同时，当某些路段的行驶时间发生变化时，需要重新计算并更新这两辆车的最优路径及行驶时间。
                    符号定义：
                    - N：道路数量
                    - u, v：道路端点
                    - w：从节点u到节点v的行驶时间
                    - S1, T1：车辆1的起点和终点
                    - S2, T2：车辆2的起点和终点
                    - u', v'：行驶时间发生变化的路段端点
                    - w'：路段新的行驶时间
                    - Path1, Path2：车辆1和车辆2的路径
                    - Time1, Time2：车辆1和车辆2的行驶时间
                    数学表达式：
                    $$N: \text{道路数量}$$
                    $$u, v: \text{道路端点}$$
                    $$w: \text{从节点u到节点v的行驶时间}$$
                    $$S1, T1: \text{车辆1的起点和终点}$$
                    $$S2, T2: \text{车辆2的起点和终点}$$
                    $$u', v': \text{行驶时间发生变化的路段端点}$$
                    $$w': \text{路段新的行驶时间}$$
                    $$Path1, Path2: \text{车辆1和车辆2的路径}$$
                    $$Time1, Time2: \text{车辆1和车辆2的行驶时间}$$
                    输入格式要求：
                        第一行 6 表示图中有6条边（即6条道路）。接下来的6行每行描述一条道路，格式为 起点 终点 行驶时间，这表示两点之间的双向道路及其行驶时间：
                        A B 10 表示从A到B的行驶时间为10分钟，双向。
                        A C 15 表示从A到C的行驶时间为15分钟，双向。
                        B D 12 表示从B到D的行驶时间为12分钟，双向。
                        C D 10 表示从C到D的行驶时间为10分钟，双向。
                        C E 5 表示从C到E的行驶时间为5分钟，双向。
                        D E 2 表示从D到E的行驶时间为2分钟，双向。
                        （接下来的两行表示车辆的起点和终点）
                        A E 表示车辆1从A点出发，前往E点。
                        B E 表示车辆2从B点出发，前往E点。
                        （最后一行 ）
                        B D 15 表示更新从B到D的行驶时间为15分钟。
                    输出格式要求：
                        A C E：车辆1的最优路径。
                        20：车辆1的总行驶时间。
                        B D E：车辆2的最优路径。
                        14：车辆2的总行驶时间。
                        B -> D 15：更新后的道路信息。
                        A C E：更新后，车辆1的最优路径保持不变。
                        20：车辆1的更新后总行驶时间不变。
                        B D E：更新后，车辆2的最优路径保持不变。
                    输入示例：['\n6\n\nA B 10\n\nA C 15\n\nB D 12\n\nC D 10\n\nC E 5\n\nD E 2\n\nA E\n\nB E\n\nB D 15']
                    输出示例：['\nA C E\n\n20\n\nB D E\n\n14\n\nB -> D 15\n\nA C E\n\n20\n\nB D E\n\n17']'''
        key_question = '''问题一：在智能交通系统中，将城市道路网络表示为无向图是合理的选择，因为无向图能够很好地描述道路的双向行驶特性，即两个节点之间的道路可以双向通行。这种模型的优势包括简化了道路网络的表示和计算、更符合实际交通规则、考虑了双向行驶的影响。

        问题二：针对车辆行驶时间发生变化时重新计算最优路径的问题，可以设计算法来实现实时交通数据的更新和路径重计算。一种常见的方法是利用实时交通数据更新路段的行驶时间，然后使用最短路径算法（如Dijkstra算法或A*算法）重新计算车辆的最优路径。在设计算法时需要特别关注的考虑因素包括实时数据的准确性、更新频率、计算效率和路径变化对交通流的影响。'''
        self.Algorithm_Selection_Phase.phase_run()




        ####算法设计阶段
        self.Algorithm_Design_Phase.phase_run()
        # 该环节输出，作为下一阶段的输入！

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

