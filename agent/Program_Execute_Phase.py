import os

from autogen import ConversableAgent
from autogen.coding import DockerCommandLineCodeExecutor
from agent.Base_Agent import Base_Agent


class Program_Execute_Phase(Base_Agent):
    """代码执行阶段"""

    def __init__(self, model_file, work_dir):
        super().__init__(model_file, work_dir)

        # 创建一个Docker命令行代码执行器。
        executor = DockerCommandLineCodeExecutor(
            image="python_self3.9:3.9.20",  # 使用给定的docker镜像名称执行代码。
            timeout=10,  # 每次代码执行的超时时间（秒）。
            work_dir=f"{self.work_dir}/code_result",  # 使用指定目录存储代码文件
            # bind_dir=
        )

        # 创建一个带有代码执行器配置的代理.
        self.code_executor_agent = ConversableAgent(
            "code_executor_agent",
            llm_config=False,  # 为此代理关闭LLM.
            code_execution_config={"executor": executor},  # 使用本地命令行代码执行器.
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
        self.code_writer_agent = ConversableAgent(
            "code_writer_agent",
            system_message=code_writer_system_message,
            llm_config={"config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}]},
            code_execution_config=False,  # 为此代理关闭代码执行.
        )

    def phase_run(self, input):
        prompt = '''你需要根据提供的伪代码编写python程序, 伪代码：\n'''
        # 调用代理完成任务
        chat_result = self.code_executor_agent.initiate_chat(
            self.code_writer_agent,
            message=prompt + input,
        )


# ====================测试================================

api_key = "sk-Oq5AQr83cGogeQ0TXzdN7uEcI7PwhBNQ0YQ8woWECLLQ406C"
os.environ["OPENAI_API_KEY"] = api_key

input = """
function quicksort(array, low, high)
    if low < high then
        // Partition the array and get the pivot index
        pivot_index = partition(array, low, high)

        // Recursively sort elements before and after partition
        quicksort(array, low, pivot_index - 1)
        quicksort(array, pivot_index + 1, high)
    end if
end function

function partition(array, low, high)
    // Choose the rightmost element as pivot
    pivot = array[high]
    i = low - 1

    for j = low to high - 1 do
        if array[j] <= pivot then
            i = i + 1
            swap array[i] and array[j]
        end if
    end for

    // Swap the pivot element with the element at i+1
    swap array[i + 1] and array[high]

    return i + 1
end function

function swap(a, b)
    temp = a
    a = b
    b = temp
end function
"""

# program_execute_phase = Program_Execute_Phase("gpt-3.5-turbo", "output_Files")
# program_execute_phase.phase_run(input)
