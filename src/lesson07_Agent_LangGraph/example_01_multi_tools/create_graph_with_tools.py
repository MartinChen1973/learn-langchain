from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition


def create_graph_with_tools(tools, chatbot, state_class, memory):
    """
    Creates a StateGraph with tools and memory enabled.

    Args:
        tools: List of tools to integrate with the graph.
        chatbot: Chatbot function to handle state updates.

    Returns:
        A compiled StateGraph with memory enabled.
    """
    # Set up the StateGraph with our defined state structure
    graph_builder = StateGraph(state_class)
    graph_builder.add_node("chatbot", chatbot)

    # Add a ToolNode for managing tool usage
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    # Define conditional edges to invoke tools when needed
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")  # Return to chatbot after using a tool

    # Set the entry point for the conversation flow
    graph_builder.set_entry_point("chatbot")

    # Add memory to the chatbot
    graph = graph_builder.compile(checkpointer=memory)

    return graph