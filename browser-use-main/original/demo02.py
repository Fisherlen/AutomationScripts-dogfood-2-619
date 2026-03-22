import asyncio
from browser_use import Agent
from browser_use.llm import ChatOpenAI

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
    result = await agent.run()
    response = result.final_result()
    print("结果是:\n", response)


if __name__ == "__main__":
    asyncio.run(main())
