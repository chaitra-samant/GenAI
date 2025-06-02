#make a more intelligent bot -> with memory (volatile)
import os
from typing import TypedDict,List,Union
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,AIMessage
from langgraph.graph import StateGraph,START,END
from dotenv import load_dotenv
load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage,AIMessage]]

llm=ChatGroq(model="llama3-70b-8192")

def process(state:AgentState)->AgentState:
    """This node will solve the request you input"""
    response=llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    print("CURRENT STATE:",state["messages"])
    return state

graph=StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)
agent=graph.compile()

conversation_history=[]
user_input=input("Enter:")
while user_input!="exit":
    conversation_history.append(HumanMessage(content=user_input))

    res=agent.invoke({"messages":conversation_history})
    conversation_history=res["messages"]
    user_input=input("Enter:")

###memory is wiped out after exiting the prog
## how to make it non volatile use a db
# simple txt file for prototyping


with open("agent2_db.txt", "w") as file:
    file.write("Your Conversation Log:\n")
    
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of Conversation")

print("Conversation saved to logging.txt")

#####this solves the volatility prob but the state size keeps increasing
###soln -> if size(state) > 5 then remove the oldest msg