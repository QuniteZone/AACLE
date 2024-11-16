##这是“利用LLM实现算法自动构建与学习增强”项目主程序
import os
from function import AutoGen

task_list = {
    "1": "加载鸢尾花数据集（Iris dataset），并基于这个数据完成对应任务。最后绘制出在数据集上模型达到的预测效果图，建议构建混淆矩阵图。",
    "2": "加载葡萄酒识别数据集（Wine recognition dataset），并基于这个数据完成对应任务。最后绘制出在数据集上模型达到的预测效果图，建议利用混淆矩阵实现。这个任务要求对数据划分80%作为测试集，20%作为测试集，另外最后评估指标选择用accuracy。"
}

output_filename = "output_Files"  # 保存的文件目录名
model = "gpt-3.5-turbo"
api_key = "sk-Oq5AQr83cGogeQ0TXzdN7uEcI7PwhBNQ0YQ8woWECLLQ406C"
os.environ["OPENAI_API_KEY"] = api_key

error_list = []  # 记录错误的task_id
autogen = AutoGen(model_file=model, work_dir=output_filename)

for task_id in task_list.keys():
    print(f"########################Task {task_id}: 开始解决！########################")
    try:
        autogen.run(task_id, task_list[task_id])
    except Exception as e:
        print(f'    Task {task_id} 执行失败，错误信息：{e}')
        error_list.append(task_id)
print(f"######################## 所有任务执行完毕！ ########################\n")
print(f"执行失败的task_id有：{error_list}")

