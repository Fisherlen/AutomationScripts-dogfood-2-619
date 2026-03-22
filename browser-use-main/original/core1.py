"""
    当前文件名称必须以test_开头，才会被测试框架执行
"""
import pandas
import allure
import pytest
from ai_process1 import process_prompt

# 1. 使用pandas读取测试用例的excel文件
all_case = pandas.read_excel('测试用例.xlsx').to_dict('records')

# 2.
@pytest.mark.parametrize('case_dict', all_case)
@pytest.mark.asyncio
async def test_case(case_dict):
    allure.dynamic.title(case_dict["用例标题"]) # 厄 陆尔
    test_result = await process_prompt(case_dict["用例描述"])
    allure.attach(f'{case_dict["用例描述"]}\n执行结果:\n{test_result}', name="AI处理结果")
    assert case_dict["期望结果"] in test_result
