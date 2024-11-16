import re
import json


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
