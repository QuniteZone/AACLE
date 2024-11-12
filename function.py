import os
import tempfile
from autogen import ConversableAgent

from autogen.coding import LocalCommandLineCodeExecutor, DockerCommandLineCodeExecutor


class AutoGen():
    def __init__(self, model_file, work_dir):
        "指定设定调用的LLM，保存目录"
        self.code_executor_agent = None
        self.code_writer_agent = None
        self.model_file = model_file
        self.work_dir = work_dir  # 保存目录
        self.task_id = None
        os.environ["http_proxy"] = "http://localhost:7890"
        os.environ["https_proxy"] = "http://localhost:7890"
        os.environ["OPENAI_BASE_URL"] = "https://api.chatanywhere.org/v1"

    def run(self, task_id, task_description):
        self.task_id = task_id  # 保存任务id
        self.def_agent()  # 定义代理

        ####构建提示词
        prompt = '''
        你需要通过编写python程序完成指定任务
        你需要利用sklearn-learn库，来按照一般机器学习步骤来完成下面的任务。其中数据集、机器学习模型、最后模型评估指标等如果任务没有指定，那你自己选择合适的来完成任务。如果任务要求有绘图需求，最后需要把绘制的图片给保存下来。如果任务有多个，你可以逐个来解决。
        任务：'''
        prompt += task_description  # 添加任务描述

        ####调用代理完成任务
        chat_result = self.code_executor_agent.initiate_chat(
            self.code_writer_agent,
            message=prompt,
        )

        ####把chat_result.chat_history保存为一个txt文件
        chat_history = chat_result.chat_history
        with open(f"{self.work_dir}/task_{self.task_id}/chat_history.txt", 'w') as f:
            f.write(str(chat_history))

        ####保存token
        prompt_tokens = None
        completion_tokens = None
        for model_key, model_data in chat_result.cost['usage_including_cached_inference'].items():
            if isinstance(model_data, dict) and 'prompt_tokens' in model_data:
                prompt_tokens = model_data['prompt_tokens']
            if isinstance(model_data, dict) and 'completion_tokens' in model_data:
                completion_tokens = model_data['completion_tokens']
        token_filename = f"total_tokens：{prompt_tokens + completion_tokens}.txt"
        # 把token_filename保存为一个txt文件
        with open(f"{self.work_dir}/task_{self.task_id}/{token_filename}", 'w') as f:
            f.write(str(chat_result.cost))

    def def_agent(self):
        # 创建一个Docker命令行代码执行器。
        executor = DockerCommandLineCodeExecutor(
            image="python_self3.9:3.9.20",  # 使用给定的docker镜像名称执行代码。
            timeout=10,  # 每次代码执行的超时时间（秒）。
            # work_dir=temp_dir.name,  # 使用临时目录存储代码文件。
            # work_dir="save_DataFile/_qgz_output_file"
            work_dir=f"{self.work_dir}/task_{self.task_id}"  # 使用指定目录存储代码文件
        )

        # 创建一个带有代码执行器配置的代理.
        code_executor_agent = ConversableAgent(
            "code_executor_agent",
            llm_config=False,  # 为此代理关闭LLM.
            code_execution_config={"executor": executor},  # 使用本地命令行代码执行器.
            # human_input_mode="ALWAYS",   # 为此代理始终接受人类输入以进行安全操作.
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
        )

        # 定义代码编写代理的系统消息.
        code_writer_system_message = """You are a helpful AI assistant.
        Solve tasks using your coding and language skills.
        In the following cases, suggest python code (in a python coding block) or shell script (in a sh coding block) for the user to execute.
        1. When you need to collect info, use the code to output the info you need, for example, browse or search the web, download/read a file, print the content of a webpage or a file, get the current date/time, check the operating system. After sufficient info is printed and the task is ready to be solved based on your language skill, you can solve the task by yourself.
        2. When you need to perform some task with code, use the code to perform the task and output the result. Finish the task smartly.
        Solve the task step by step if you need to. If a plan is not provided, explain your plan first. Be clear which step uses code, and which step uses your language skill.
        When using code, you must indicate the script type in the code block. The user cannot provide any other feedback or perform any other action beyond executing the code you suggest. The user can't modify your code. So do not suggest incomplete code which requires users to modify. Don't use a code block if it's not intended to be executed by the user.
        If you want the user to save the code in a file before executing it, put # filename: <filename> inside the code block as the first line. Don't include multiple code blocks in one response. Do not ask users to copy and paste the result. Instead, use 'print' function for the output when relevant. Check the execution result returned by the user.
        If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
        When you find an answer, verify the answer carefully. Include verifiable evidence in your response if possible.
        Reply 'TERMINATE' in the end when everything is done.
        """
        # 创建一个带有代码编写的代理.
        code_writer_agent = ConversableAgent(
            "code_writer_agent",
            system_message=code_writer_system_message,
            llm_config={"config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}]},
            code_execution_config=False,  # 为此代理关闭代码执行.
        )
        self.code_executor_agent = code_executor_agent
        self.code_writer_agent = code_writer_agent

