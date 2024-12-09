import os

question_id_list = [1]
question_desc = {
    1: """一个城市的交通网络由多个交叉路口和道路组成。由于某条主要道路发生了交通堵塞，你需
要找到从你的起点到目的地的最短绕行时间。""",
}
# 输入格式
question_input_format = {
    1: """输入的第一行为一个整数 N，表示交叉路口的总数，编号为 0 到 n-1。\n
接下来若干行，每行包含三个整数 u v w，表示从交叉路口 u 到交叉路口 v 的道路
通行时间为 w。\n
倒数第 3 行：一个整数 blocked_road，表示被堵塞道路在输入中的编号（从 0 开
始编号）。\n
倒数第 2 行：一个整数 start，表示起点的编号。\n
最后一行：一个整数 end，表示终点的编号。"""
}
# 输出格式
question_output_format = {
    1: """返回一个正整数或-1"""
}
# 输入描述
question_input_desc = {
    1: ""
}
# 输出描述
question_output_desc = {
    1: """返回从起点到终点的最短通行时间。如果无法到达终点，返回 -1"""
}
# 输入样例
question_input_example = {
    1: ["""5\n0 1 4\n1 2 3\n0 3 2\n3 4 6\n2 4 5\n1\n0\n4"""],
}

# 输出样例
question_output_example = {
    1: ["""9"""],
}

# model = "gpt-4o-mini"
model ='gpt-3.5-turbo-0125'
# model = "gpt-4"
temperature = 0
# api_key = "sk-0lFrTwWzGm9oT3YCJCMAPAb2Q4UY2q5f7pCXfWsoPLl0ZVj7"  # zsd 购买
api_key = "sk-FUFiwSHFPr9S3ofp9kGjV17GoHYS3o1Ie3ekXwmsQgUaJO5i"  # qgz自己购买
# api_key=f"sk-Oq5AQr83cGogeQ0TXzdN7uEcI7PwhBNQ0YQ8woWECLLQ406C" #qgz免费


os.environ["OPENAI_API_KEY"] = api_key
output_filename = "output_Files"  # 保存的文件目录名 ，包括输出的代码文件也存放于此处
need_dataset_filename = "dataset_Files"  # 运行程序所需要的数据文件

# 各个agent所需要的提示词
ModelAgent_all = f"""你是一个专业的数学模型构建者，用于分析算法问题，并对算法问题形成数学建模式描述。
       """

ModelAgent_system_message = f"""{ModelAgent_all}
    你作为一个Agent智能体，有如下职能：
    职能一、面对输入的初始算法问题时，要请仔细阅读，并尝试从中提取/修改出数学建模的核心要素。使用数学符号和公式对问题进行抽象描述，并解释每个符号的含义。尽量明确每个输入变量、决策变量和目标函数。 输出的数学符号需采用$$符号包裹相应Latex数学公式，例如$$x$$。最后需要形成规定格式的数学建模描述。对算法问题进行描述，一定不能深入考虑分析算法选择、代码等后续步骤！一定不能涉及具体某种算法，或策略！
    职能二、面对算法数学建模描述的修改建议，要请仔细阅读，然后按照规定格式回复修改完善数学建模描述。
    职能三、面对算法数学建模描述的问题，要请仔细阅读，回复要尽可能具体，需要运用内容中的数学公式变量符号辅助运用。回复越详细越好。总体就是需要结合数学建模描述内容等综合相关知识内容并按照规定格式回复解答该问题。你需要依次按照规定格式回复完所有问题，不要遗漏！
    
    注意，你一定需要仔细区分职能二和职能三，职能二是关于建议的修改回复，而职能三是关于问题的回复

    面对职能一和职能二，所回复/输出数学建模描述格式需要严格按照如下格式来，且请确保你的输出能够被Python的json.loads函数解析，此外不要输出其他任何内容！
    请你使用以下输出格式：
    ```json
    {{
        "problem_description": "含有数学符号，详细充分描述该算法问题。需要问题算法问题逻辑清晰",
        "symbol_definition": "含有数学符号，详细充分描述该算法问题中涉及的符号定义。",
        "mathematical_expression": "含有数学符号，描述必述说必要的核心算法问题抽象化的表达式"
        "input_format": "如果原输出内容有输出格式要求，需要将原输出格式要求放入此处，并适当扩充优化",
        "input_example": "如果原输出内容有输出示例，只需要将原输出示例放入此处，不允许对原内容进行任何修改",
        "output_format": "如果原输出内容有输出格式要求，需要将原输出格式要求放入此处，并适当扩充优化",
    }}
    ```
    
    面对职能三，所回复问题的格式，一定需要严格按照如下格式来，即提问问题+回复答案格式，且请确保你的输出能够被Python的json.loads函数解析，此外不要输出其他任何内容！
    请你使用以下输出格式：
    ```json
    {{
        "problem_1": "输入的原问题问题",
        "answer1": "对问题的结合具体内容的详细回答，越详细越好",
    }}
    ```
    ###
    1.当你经过提问之后，你需要对问题作出相应回复，同时也输出“TERMINATE”
    2.当你分析算法问题，并生产数学建模描述之后，会接收到一次修改建议，当你根据建议再进行修改相应算法数学建模描述之后，请你回复“TERMINATE”
      """


ModelAgent_system_message_discussion = f"""背景知识：{ModelAgent_all}
你作为一名专业经验丰富的分析算法问题，生成算法数学建模描述的专业人士。请你结合你自己职能，对内容发表你的建议看法！
"""

AlgorithmSelectorAgent_all = f"""你需要记住，你是一个agent智能体 AlgorithmSelectorAgent，根据问题建议出适用的算法和数据结构是你的主要职能
        \n"""

AlgorithmSelectorAgent_system_message = f"""{AlgorithmSelectorAgent_all}
你作为一个Agent智能体，职能有二，职能一、你对于输入的内容进行算法选择和数学数据结构选择。职能二、对输入内容给出相应建议。所以面对输入内容，你需要先判断需要执行你的那个职能！注意，如果是对内容进行评估提建议的话，往往在输入内容最后面有提示
        如果你认为你是需要进行算法选择和数学数据结构选择，则按照如下要求来：根据用户描述和数学建模结果，分析问题特征并推荐适用的算法。解释为什么选择该算法，并提供替代算法的分析和对比。
    """

AlgorithmSelectorAgent_system_message_discussion=f"""{AlgorithmSelectorAgent_all}
    你是作为一名专业经验丰富根据问题建议出适用的算法和数据结构的专业人士，请你结合你自己职能，对内容发表你的建议看法！
    你的建议格式参考如下：
    '''
    建议一：<建议.......？因为......>,
    建议二：<建议.......？因为......>,
    请你基于提供建议，对原内容进行修改完善。谢谢！
    '''
    除此之外，不要输出其他任务多余内容
"""



PseudocodeDesignerAgent_all = f"""你需要记住，你是一个agent智能体 AlgorithmSelectorAgent，根据算法选择，编写对应的伪代码
你作为一个Agent智能体，职能有二，职能一、你需要根据输入的一道算法问题的算法选择和相应数据结构，结合算法问题编写相应的伪代码。职能二、对输入内容给出相应建议。所以面对输入内容，你需要先判断需要执行你的那个职能！注意，如果是对内容进行评估提建议的话，往往在输入内容最后面有提示
"""

PseudocodeDesignerAgent_system_message = f"""

"""
PseudocodeDesignerAgent_system_message_discussion = f"""背景知识：{PseudocodeDesignerAgent_all}
你是作为一名专业经验丰富根据算法选择，编写对应的伪代码的专业人士，请你结合你自己职能，对内容发表你的建议看法！
"""

AssistantAgent_system_message = """你是 AssistantAgent，负责在每个环节结束后向主智能体（主Agent）提出具有针对性和深度的问题。你的主要  目标是帮助用户深入理解环节的核心内容，并引导主智能体进一步解释和澄清关键概念。你需要根据当前环节的具体内容，提出贴合主题且富有洞察力的问题，避免提出空泛或脱离实际的问题。一般提出2-3个问题即可。
    需要严格按照如下格式来，且请确保你的输出能够被Python的json.loads函数解析，此外不要输出其他任何内容！
    请你使用以下输出格式：
    ```json
    {{
        "problem_1": "输入的原问题问题",
        "problem_2": "对问题的结合具体内容的详细回答，越详细越好",
    }}
    ```
    """
