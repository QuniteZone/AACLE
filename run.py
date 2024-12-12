##这是“利用LLM实现算法自动构建与学习增强”项目主程序
import os
from utils import get_project_root, Check_file_exists
from conf import model, output_filename, need_dataset_filename,temperature
from conf import question_id_list,question_desc,question_input_format,question_output_format,question_input_desc,question_output_desc,question_output_example,question_input_example
import sys
sys.path.append("..")
sys.path.append("../..")

####################### 以下为配置信息，请根据需要修改 ##############
tasks_list={}
for question_id in question_id_list: #遍历所有问题，构造问题列表基本配置
    question_message={}
    question_message['question_desc']=question_desc[question_id]
    question_message['question_input_format']=question_input_format[question_id]
    question_message['question_output_format']=question_output_format[question_id]
    question_message['question_input_desc']=question_input_desc[question_id]
    question_message['question_output_desc']=question_output_desc[question_id]
    question_message['question_output_example']=question_output_example[question_id]
    question_message['question_input_example']=question_input_example[question_id]
    tasks_list[question_id]=question_message

Check_file_exists(output_filename) #检查文件是否存在
Check_file_exists(need_dataset_filename)  #检查文件是否存在





####################### 以下为AutoLearning主程序调用 ##############
from self_AutoGen import AACLE
error_list = []  # 记录错误的task_id
autogen = AACLE(model=model,temperature=temperature,work_dir=output_filename,bind_dir=need_dataset_filename) #初始化AutoLearning

for task_id in tasks_list.keys():
    print(f"########################Task {task_id}: 开始解决！########################")
    all_result,all_KeyQuestion = autogen.run(task_id, tasks_list[task_id])
    print(f"########################Task {task_id}: 结束解决！########################")
    print(f"all_result:{all_result}")
    print(f"all_KeyQuestion:{all_KeyQuestion}")



