import re
import json
import os


def exact_json_from_text(text: str):
    """
    从文本中提取出json格式数据
    """
    match = re.search(r'\{.*\}', text)
    if match:
        # 提取匹配的部分
        json_str = match.group(0)
        print("json_str: ", json_str)
        # 将提取的字符串转换为 JSON 对象
        try:
            result_dict = json.loads(json_str)
            return result_dict
        except json.JSONDecodeError as e:
            print(f"JSON 解码错误: {e}")


def get_project_root():
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    # 向上一级
    current_directory = os.path.dirname(current_file_path)
    # 再次向上一级
    project_root = os.path.dirname(current_directory)

    return project_root


def Check_file_exists(filename):
    folder_path = os.path.join(get_project_root(), r'AACLE',filename)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"文件夹'{folder_path}'已创建。")
    else:
        print(f"文件夹'{folder_path}'已存在。")
