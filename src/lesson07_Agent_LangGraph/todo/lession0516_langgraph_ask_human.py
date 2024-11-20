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
    # =============================================
    ask_human: bool
    # ---------------------------------------------

from pydantic import BaseModel

class RequestAssistance(BaseModel):
    """Escalate the conversation to an expert. 
    Use this if you are unable to assist directly or if the user requires support beyond your permissions.
    To use this function, relay the user's 'request' so the expert can provide the right guidance.
    """
    request: str

# Initialize Tavily search tool and bind it to the LLM
tool = TavilySearchResults(max_results=2)
tools = [tool]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)
# =============================================
llm_with_tools = llm.bind_tools(tools + [RequestAssistance])
# ---------------------------------------------

# Define the chatbot function that takes the current state and updates it with a new message
def chatbot(state: State):
    response = llm_with_tools.invoke(state["messages"])
    # =============================================
    ask_human = False
    if (
        response.tool_calls
        and response.tool_calls[0]["name"] == RequestAssistance.__name__
    ):
        ask_human = True
    return {"messages": [response], "ask_human": ask_human}
    # ---------------------------------------------

# Set up the StateGraph with our defined state structure
graph_builder = StateGraph(State)


# =============================================
# Add a node to handle human intervention
from langchain_core.messages import AIMessage, ToolMessage

def create_response(response: str, ai_message: AIMessage):
    return ToolMessage(
        content=response,
        tool_call_id=ai_message.tool_calls[0]["id"],
    )

def human_node(state: State):
    new_messages = []
    if not isinstance(state["messages"][-1], ToolMessage):
        # Typically, the user will have updated the state during the interrupt.
        # If they choose not to, we will include a placeholder ToolMessage to
        # let the LLM continue.
        new_messages.append(
            create_response("No response from human.", state["messages"][-1])
        )
    return {
        # Append the new messages
        "messages": new_messages,
        # Unset the flag
        "ask_human": False,
    }

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=[tool]))
graph_builder.add_node("human", human_node)

def select_next_node(state: State):
    if state["ask_human"]:
        return "human"
    # Otherwise, we can route as before
    return tools_condition(state)

graph_builder.set_entry_point("chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    select_next_node,
    {"human": "human", "tools": "tools", END: END},
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("human", "chatbot")
# --------------------------------------------

# Add memory to the chatbot
memory = MemorySaver()
graph = graph_builder.compile(
    checkpointer=memory,
    # =============================================
    # We interrupt before 'human' here instead.
    interrupt_before=["human"],
    # --------------------------------------------
)

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
    thread_id = input("Enter a thread ID for this session: ")
    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        stream_graph_updates(user_input, thread_id)