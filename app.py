import chainlit as cl
from langchain_community.llms import Ollama
from agent_crew import generate_spring_plan

llm = Ollama(model="openhermes")

@cl.on_message
async def main(message: cl.Message):
    response = await cl.make_async(generate_spring_plan)(message,llm)
    await cl.Message(
        content=response,
    ).send()
