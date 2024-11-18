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
from self_AutoGen import AutoLearning
error_list = []  # 记录错误的task_id
autogen = AutoLearning(model_file=model,temperature=temperature,work_dir=output_filename,bind_dir=need_dataset_filename) #初始化AutoLearning

for task_id in tasks_list.keys():
    print(f"########################Task {task_id}: 开始解决！########################")
    result = autogen.run(task_id, tasks_list[task_id])
    print(f'result:{result}')
    # try:
    #     print(f"tasks_list[task_id]:{tasks_list[task_id]}")
    #     result=autogen.run(task_id, tasks_list[task_id])
    #     print(f'result:{result}')
    # except Exception as e:
    #     print(f'    Task {task_id} 执行失败，错误信息：{e}')
    #     error_list.append(task_id)
print(f"######################## 所有任务执行完毕！ ########################\n")
print(f"执行失败的task_id有：{error_list}")

