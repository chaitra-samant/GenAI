from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_groq import ChatGroq
from langserve import add_routes
from dotenv import load_dotenv
import os
import uvicorn

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="Simple API Server"
)

# Base LLM model
llm = ChatGroq(model="llama3-70b-8192")

# Routes
add_routes(
    app,
    llm,
    path="/groq"
)

# Prompt templates
prompt = ChatPromptTemplate.from_template("Write me an essay of 100 words about {topic}")
prompt2 = ChatPromptTemplate.from_template("Give me a 4 line poem with rhyme scheme about {topic} in marathi language")

# Runnable chains
essay_chain = prompt | llm
poem_chain = prompt2 | llm

add_routes(
    app,
    essay_chain,
    path="/essay"
)
add_routes(
    app,
    poem_chain,
    path="/poem"
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8000
    )
