# 1. 演示如何让智能体记住对话历史
# 2. 演示如何利用thread_id来区分不同的会话

from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv(find_dotenv())

# Define the structure of the chatbot's state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize Tavily search tool and bind it to the LLM
tavily = TavilySearchResults(max_results=10)
tools = [tavily]
llm = ChatOpenAI(model="gpt-4o-mini")
# llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

# Define the chatbot function that takes the current state and updates it with a new message
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Set up the StateGraph with our defined state structure
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

# Add a ToolNode for managing tool usage (like Tavily search)
tool_node = ToolNode(tools=[tavily])
graph_builder.add_node("tools", tool_node)

# Define conditional edges to invoke tools when needed
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")  # Return to chatbot after using a tool

# Set the entry point for the conversation flow
graph_builder.set_entry_point("chatbot")

# =============================================
# Add memory to the chatbot
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
# --------------------------------------------

# Function to handle conversation updates with thread_id for memory
def stream_graph_updates(user_input: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}

    # The config is the **second positional argument** to stream() or invoke()!
    events = graph.stream(
        {"messages": [("user", user_input)]}, config, stream_mode="values"
    )
    for event in events:
        message = event["messages"][-1] # Get the last message in the event
        # 1. print the last message in the event no matter what, or...
        message.pretty_print()

        # 2. only print the last message if it's AIMessage and has content
        # if isinstance(message, AIMessage) and message.content:
        #     print("Assistant:", message.content + f" (totally {len(event['messages'])} messages)")

        # For more information, try these RAW contents:
        # print(f"Message type: {type(message).__name__}")
        # print(message) 
        # print("-------------")

if __name__ == "__main__":
    # Optional: Visualize the graph structure
    import os
    from utilities.image_saver import save_graph_image    
    save_graph_image(graph, os.path.basename(__file__))

    # Chatbot loop with memory enabled using thread_id
    while True:
        print("==================================== Users can input 'quit' to quit.")
        thread_id = input("Enter a thread ID for this session: ")
        user_input = input("User: ")
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        stream_graph_updates(user_input, thread_id)
