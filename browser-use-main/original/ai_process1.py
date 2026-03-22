from browser_use import Agent
from browser_use.agent.views import AgentHistoryList
from browser_use.llm import ChatOpenAI

# region
key = "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"
# endregion

llm = ChatOpenAI(
    model="openai/gpt-5-mini",
    # model="google/gemini-2.0-flash-exp:free",
    api_key=key,
    base_url="https://openrouter.ai/api/v1"
)


async def process_prompt(task):
    agent = Agent(
        task=task,
        llm=llm,
    )
    result = await agent.run() # type:AgentHistoryList  # 黑死特瑞
    response = result.final_result()
    print("结果是:\n", type(result))
    return response
