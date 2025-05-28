from langchain_openai import ChatOpenAI
from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    def create_llm(self):
        pass


class OpenAILLMFactory(LLM):
    def __init__(self, model_name="gpt-4o-mini", temperature=0.7, api_key=None):
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = api_key

    def create_llm(self):
        return ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature
        )

class LLMFactory:
    def create_llm(self, llm_type, **kwargs):
        if llm_type == "openai":
            return OpenAILLMFactory(**kwargs).create_llm()
        else:
            raise ValueError(f"Unsupported LLM type: {llm_type}")