###ReAct Agent -> reasoning & acting -> create tools
"""
start -> agent -> end
            ^
            | {loop}
            Tools
"""

from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv  
from langchain_core.messages import BaseMessage # The foundational class for all message types in LangGraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph.message import add_messages #reducer fn - smart ways to update states 
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]

@tool
def add(a:int,b:int):
    """This is an addition function that adds 2 numbers together""" ##if docstring not included graph doesnt work
    return a+b

@tool
def sub(a:int,b:int):
    """This is an subtraction function that subtracts 2 numbers together""" ##if docstring not included graph doesnt work
    return a-b

@tool
def mul(a:int,b:int):
    """This is an multiplication function that multiplies 2 numbers together""" ##if docstring not included graph doesnt work
    return a*b

tools=[add,sub,mul]
model=ChatGroq(model="llama3-70b-8192").bind_tools(tools)

def model_call(state:AgentState)->AgentState:
    system_prompt=SystemMessage(content=
                                "You are my AI Assistant, please answer my query to the best of your ability"
    )
    response=model.invoke([system_prompt]+state["messages"])
    return {"messages":[response]} ##compact way of updating state ->reducer function handles everything


def should_continue(state:AgentState):
    messages=state["messages"]
    last_message=messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"
    

graph=StateGraph(AgentState)
graph.add_node("our_agent",model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools",tool_node)

graph.add_edge(START,"our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue":"tools",
        "end":END
    }
)

graph.add_edge("tools","our_agent")
app=graph.compile()

#function for beaut op in term
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [HumanMessage(content="Add 40 and 12 then multiply the result by 2. then tell me a joke")]}
print_stream(app.stream(inputs, stream_mode="values"))