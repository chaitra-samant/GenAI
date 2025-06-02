##integrating llms in langgraph -> simple bot w/llm wrapper
from typing import TypedDict,List
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import START,END,StateGraph
from dotenv import load_dotenv
load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm=ChatGroq(model="llama3-70b-8192")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state

graph=StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)
agent=graph.compile()

user_input=input("Enter:")
while user_input!="exit":
    agent.invoke({"messages":[HumanMessage(content=user_input)]})
    user_input=input("Enter:")