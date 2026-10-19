import asyncio

from jobastra_ai.llm.models import get_chat_model


async def main():
    model = get_chat_model()
    response = await model.ainvoke("Say hello in one sentence.")
    print(response.content)


asyncio.run(main())