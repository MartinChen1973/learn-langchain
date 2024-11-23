# 1. 演示一个最简单的无记忆、无工具的智能体。

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

load_dotenv(find_dotenv())
model = ChatOpenAI(model="gpt-4o-mini")

# Define the structure of the chatbot's state
# State是当前聊天状态的数据结构，用于存储聊天过程中的信息、状态。
# 下面的State只有唯一的一个字段messages，用于存储聊天过程中的历史消息。
# add_messages是一个内建的方法，用于追加消息历史。
class State(TypedDict):
    messages: Annotated[list, add_messages] 

# Define the chatbot function that takes the current state and updates it with a new message
# 这是一个简单的机器人，他直接调用了llm.invoke()方法处理以往的历史，然后返回model最后一次的回复。
def chatbot(state: State):
    return {"messages": [model.invoke(state["messages"])]}

# Set up the StateGraph with our defined state structure
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)  # Add the chatbot node

# Define start and end points for the conversation flow
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile the graph to make it runnable
graph = graph_builder.compile()

# Function to handle conversation updates
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            if value["messages"][-1].content:
                print("Assistant:", value["messages"][-1].content + f" (totally {len(value['messages'])} messages)")

# Run the chatbot in a loop
if __name__ == "__main__":
    # Optional: Visualize the graph structure
    import os
    from utilities.image_saver import save_graph_image    
    save_graph_image(graph, os.path.basename(__file__))

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input)
