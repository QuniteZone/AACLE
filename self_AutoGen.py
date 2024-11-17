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
    def __init__(self, model_file, work_dir,bind_dir):
        self.bind_dir=bind_dir #绑定所需本地数据的目录，有需要自己拉去
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
        self.Problem_Model_Phase.phase_run(task_description)
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

