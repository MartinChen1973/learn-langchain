# 1. 演示如何让智能体自动使用工具（如Tavily搜索引擎）来回答问题

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Load environment variables
load_dotenv(find_dotenv())

# << Tavily search tool usage ===========
# search = TavilySearchResults(max_results=10)
# search_results = search.invoke("Who won the 2024 US presidential election?")
# print(search_results)
# exit(0)
# ======================================>>

# Define the structure of the chatbot's state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# =============================================
# Initialize Tavily search tool and bind it to the LLM
from langchain_community.tools import BraveSearch
tavily = TavilySearchResults(max_results=10)
tools = [tavily]
model = ChatOpenAI(model="gpt-4o-mini")
# model = ChatOpenAI(model="gemini-pro")
# model = ChatOpenAI(model="gemma-7b-it") # 默认是gpt-3.5

# model = ChatOpenAI(model="gpt-4o")
# model = ChatOpenAI(model="gpt-4o-2024-08-06")
# model = ChatOpenAI(model="o1-preview-2024-09-12")

model_with_tools = model.bind_tools(tools)
# ---------------------------------------------

# Define the chatbot function that takes the current state and updates it with a new message
def chatbot(state: State):
    # The LLM with tools bound to it can now invoke the search engine if needed
    return {"messages": [model_with_tools.invoke(state["messages"])]}

# Set up the StateGraph with our defined state structure
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)  # Add the chatbot node

# =============================================
# Add a ToolNode for managing tool usage (like Tavily search)
tool_node = ToolNode(tools=[tavily])
graph_builder.add_node("tools", tool_node)
# ---------------------------------------------

# Define conditional edges to invoke tools when needed
graph_builder.add_conditional_edges("chatbot", tools_condition)
# graph_builder.add_edge("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")  # Return to chatbot after using a tool

# Set the entry point for the conversation flow
graph_builder.set_entry_point("chatbot")

# Compile the graph to make it runnable
graph = graph_builder.compile()

# Function to handle conversation updates
def stream_graph_updates(user_input: str):
    final_content = None  # Track the content of the final message

    # Collect the last non-human message content from the last event
    for event in graph.stream({"messages": [("user", user_input)]}, stream_mode="values"):
        for value in event.values():
            # Ensure `value` is a list and has messages
            if isinstance(value, list) and value:
                # Find the last non-HumanMessage instance in the list
                for msg in reversed(value):
                    if not isinstance(msg, HumanMessage) and hasattr(msg, "content"):
                        # Update final_content to the latest assistant message
                        final_content = msg.content
                        break

    # Print only the final message content after processing all events
    if final_content:
        print("Assistant:", final_content)
    else:
        print("Assistant: No assistant response found.")

if __name__ == "__main__":
    # Optional: Visualize the graph structure
    import os
    from utilities.image_saver import save_graph_image    
    save_graph_image(graph, os.path.basename(__file__))

    # Chatbot loop
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
