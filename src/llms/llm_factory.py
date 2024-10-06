from langchain_groq import ChatGroq
from enum import Enum
from typing import Dict, Any
class LLM(Enum):

    LLMA_31_70b = "llama-3.1-70b-versatile" 



class LLMFactory:


    def __init__(self) -> None:
        pass

    @staticmethod
    def create(self, llm: LLM = LLM.LLMA_31_70b, config: Dict[str, Any] = {}) -> LLM:
        return  ChatGroq(model=llm, config=config)



