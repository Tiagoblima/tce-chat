# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import getpass
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from src.chat.chatbot import ChatBot
load_dotenv()

app = FastAPI()

# Modelo de dados para a requisição
class RequestModel(BaseModel):
    text: str


@app.post("/ainvoke")
async def ainvoke(request: RequestModel):
    # Processar o texto usando LangChain
    processed_text = await ChatBot().get_response("2", HumanMessage(request.text))
    return {"processed_text": processed_text}

# Rota de exemplo
@app.get("/")
async def read_root():
    return {"message": "API FastAPI com LangChain"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)