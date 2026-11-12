from llm_cw.llm.ollama_client import OllamaClient

client = OllamaClient()

response = client.generate("What is a three-letter word for feline pet?")

print(response)