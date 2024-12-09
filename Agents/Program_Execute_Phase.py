import os

from autogen import ConversableAgent
from autogen.coding import DockerCommandLineCodeExecutor

from AACLE.Agents import Base_Agent


class Program_Execute_Phase(Base_Agent):
    """代码执行阶段"""

    def __init__(self, model_file,temperature ,work_dir):
        super().__init__(model_file,temperature, work_dir)

        # 创建一个Docker命令行代码执行器。
        executor = DockerCommandLineCodeExecutor(
            image="python_self3.9:3.9.20",  # 使用给定的docker镜像名称执行代码。
            timeout=10,  # 每次代码执行的超时时间（秒）。
            work_dir=f"../{self.work_dir}/code_result"  # 使用指定目录存储代码文件
        )
        code_executor_system_message = """你以一名代码运行者, 主要负责运行python代码并给出运行结果.
        1.如果运行成功了, 请在会话的最后输出运行结果, 并且运行结果请以"code run result:\n"开头.
        2.如果运行失败了，请给出运行失败的原因.
        """
        # 创建一个带有代码执行器配置的代理.
        self.code_executor_agent = ConversableAgent(
            "code_executor_agent",
            llm_config=False,  # 为此代理关闭LLM.
            code_execution_config={"executor": executor},  # 使用本地命令行代码执行器.
            human_input_mode="NEVER",  # 为此代理从不接受人类输入以进行安全操作.
        )
        # 定义代码编写代理的系统消息.
        code_writer_system_message = """你是一名代码编写者, 请根据给出的要求去编写python代码.
        1.如果需要将伪代码转化为可运行代码, 请转化为python代码
        2.如果您希望用户在执行代码之前将其保存在文件中，请将 # filename: <filename> 作为第一行放在代码块内。
        3.如果code_executor_agent执行成功了代码, 请结束会话, 并恢复"TERMINATE".
        4.如果code_executor_agent执行失败了代码, 请根据它给的原因来修改为正确的代码."""
        self.code_writer_agent = ConversableAgent(
            "code_writer_agent",
            system_message=code_writer_system_message,
            llm_config={"config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}]},
            code_execution_config=False,  # 为此代理关闭代码执行.
            human_input_mode="NEVER",
            is_termination_msg=lambda msg: 'execution succeeded' in msg["content"].lower()
        )

    def phase_run(self, input):
        prompt = '''你需要根据提供的伪代码编写python程序, 伪代码：\n'''
        # 调用代理完成任务
        result = self.code_executor_agent.initiate_chat(
            self.code_writer_agent,
            message=prompt + input,
        )
        self.result_text = result.chat_history[-1]['content']


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

program_execute_phase = ProgramExecutePhase("gpt-3.5-turbo", "output_Files")
program_execute_phase.phase_run(input)
