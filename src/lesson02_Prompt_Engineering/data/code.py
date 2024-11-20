from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

# Load environment variables
load_dotenv(find_dotenv())

# Define the structure of the chatbot's state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize Tavily search tool and bind it to the LLM
tool = TavilySearchResults(max_results=2)
tools = [tool]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

# Define the chatbot function that takes the current state and updates it with a new message
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Set up the StateGraph with our defined state structure
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

# Add a ToolNode for managing tool usage (like Tavily search)
tool_node = ToolNode(tools=[tool])
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
    final_content = None  # Track the content of the final message

    # Collect the last non-human message content from the last event
    for event in graph.stream({"messages": [("user", user_input)]}, config, stream_mode="values"):
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
    from tools.image_saver import save_graph_image    
    save_graph_image(graph, os.path.basename(__file__))

    # Chatbot loop with memory enabled using thread_id
    while True:
        thread_id = input("Enter a thread ID for this session: ")
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        if user_input.lower() in ["memory"]:
            print(memory.storage)
            continue

        stream_graph_updates(user_input, thread_id)
