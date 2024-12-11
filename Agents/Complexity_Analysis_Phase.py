from AACLE.Agents.Base_Agent import Base_Agent


class Complexity_Analysis_Phase(Base_Agent):
    """正确性验证阶段"""
    def phase_run(self, Algorithm_Design_list):
        """复杂度分析阶段"""
        prompt = f"""下面是我输入的算法内容描述和解题算法及结构，请你依据这些内容完成伪代码的时间、空间复杂度分析任务！
            算法选择：
                BaseInfo: {Algorithm_Design_list[0]}
                Pseudocode: {Algorithm_Design_list[1]}
            """

        chat_result = self.ComplexityAnalyzerAgent.initiate_chat(
            self.ComplexityAnalyzerAgent,
            message=prompt,
            summary_method="reflection_with_llm",
            max_turns=1,
        )

        ComplexityAnalyzerAgent_ResultData = []  # 用于存储chat_result
        for result in chat_result.chat_history:
            if result['name'] == 'ComplexityAnalyzerAgent':
                ComplexityAnalyzerAgent_ResultData.append(result['content'])
        if len(ComplexityAnalyzerAgent_ResultData) < 3:
            assert False, "环节五未成功完成，请检查相关对话排错！"

        ComplexityAnalyzerResult = self.load_json(ComplexityAnalyzerAgent_ResultData[-1])

        print(f"########################################## 环节五已成功结束 ##########################################")
        print(f"ComplexityAnalyzerResult: {ComplexityAnalyzerResult}")

        assert False,"暂时终止！！！"
