import sys
import os

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI

# 从当前文件夹或父文件夹中加载.env文件的配置（成为全局可访问的静态变量）。
load_dotenv(find_dotenv())

# Add the project root dynamically to sys.path
current_file = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file, "../../../.."))  # Adjust to project root
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from langchain_core.messages import HumanMessage, AIMessage
from src.utilities.create_retriever_from_md_files import create_retriever_from_md_files, find_md_files
from src.utilities.create_retriever_from_urls import create_retriever_from_urls, load_urls
from src.utilities.image_saver import save_graph_image
from create_tools import create_tools
from create_graph_with_tools import create_graph_with_tools
from langgraph.checkpoint.memory import MemorySaver


def main():

    # Create tools for the chatbot
    tools = create_tools()
    print("\nCount of tools created: ", len(tools))

    # Create the chatbot model
    llm = ChatOpenAI(model="gpt-4o-mini")
    llm_with_tools = llm.bind_tools(tools)

    # Define the structure of the chatbot's state
    class State(TypedDict):
        messages: Annotated[list, add_messages]

    # Define the chatbot function
    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    # Create the graph with memory
    memory = MemorySaver()
    graph = create_graph_with_tools(tools, chatbot, State, memory)

    # Optional: Visualize the graph structure
    save_graph_image(graph, os.path.basename(__file__))

    # Function to handle conversation updates with thread_id for memory
    def stream_graph_updates(user_input: str, thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}

        # Stream events and print responses
        events = graph.stream(
            {"messages": [("user", user_input)]}, config, stream_mode="values"
        )
        for event in events:
            message = event["messages"][-1]
            if (isinstance(message, AIMessage) and message.content):
                message.pretty_print()

    # Chatbot loop with memory enabled using thread_id
    while True:
        print("==================================== Users can input 'quit' to quit.")
        thread_id = input("Enter a thread ID for this session: ")
        user_input = input("User: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        stream_graph_updates(user_input, thread_id)


if __name__ == "__main__":
    main()
