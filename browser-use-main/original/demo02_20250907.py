import asyncio
import logging
from browser_use import Agent
from browser_use.llm import ChatOpenAI

# 设置日志级别以便更好地调试
logging.basicConfig(level=logging.INFO)

# region
key = "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"
# endregion

llm = ChatOpenAI(
    model="openai/gpt-5-mini",
    api_key=key,
    base_url="https://openrouter.ai/api/v1"
)


async def main():
    agent = Agent(
        llm=llm,
        task="""
            1.打开网页 https://www.baidu.com/
            2.在输入框中输入手机，然后点击搜索按钮
            3.返回第一页中所有包含广告的信息
            结果：如果广告信息中包含京东返回"通过"，否则返回"失败" 
        """,
    )

    try:
        result = await agent.run()
        response = result.final_result()
        print("结果是:\n", response)
    except Exception as e:
        print(f"执行过程中出现错误: {e}")
        print("请检查以下几点:")
        print("1. 确保已安装Chrome/Chromium浏览器")
        print("2. 检查网络连接是否正常")
        print("3. 确认系统防火墙未阻止浏览器启动")
        print("4. 尝试重启计算机后再次运行")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"程序启动失败: {e}")
