from langchain_community.llms import Ollama

ollama_llm = Ollama(model="openhermes")

print(ollama_llm.invoke("Tell me a joke"))