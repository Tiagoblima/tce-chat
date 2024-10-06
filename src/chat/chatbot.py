from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.llms import Cohere
from .prompts import QA_SYSTEM_PROMPT, CONTEXTUALIZED_Q_SYSTEM_PROMPT
from src.llms.llm_factory import LLMFactory, LLM
from src.tools.retriever import Retriever
def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")



import asyncio
class ChatBot:

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.llm = LLMFactory.create(LLM.LLMA_31_70b)
        self.retriever = Retriever()
        self.retriever = self.loop.run_until_complete(self.retriever.get_retriever(QA_SYSTEM_PROMPT, self.llm))
         
       

    async def get_response(self, session_id, message):
        history = get_session_history(session_id)
        messages = history.get_messages()
        prompt = ChatPromptTemplate(
            template=CONTEXTUALIZED_Q_SYSTEM_PROMPT,
            placeholders=[MessagesPlaceholder(messages=messages)]
        )
        prompt = prompt.render()
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        return conversational_rag_chain.invoke(message, config)



