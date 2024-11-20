import sys
import os

from src.utilities.create_retriever_from_md_files import create_retriever_from_md_files, find_md_files
from src.utilities.create_retriever_from_urls import create_retriever_from_urls, load_urls

from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults


def create_tools():
    # Create url_retriever_tool
    urls_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_data", "Langgraph_official_website.urls")
    name, description, urls = load_urls(urls_file)

    url_retriever_tool_for_langgraph = create_retriever_tool(
        retriever=create_retriever_from_urls(urls),
        name=name,
        description=description,
    )

    # Create markdown_files_tool
    md_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_data", "org_information")
    md_files = find_md_files(md_folder_path)

    url_retriever_tool_for_md = create_retriever_tool(
        retriever=create_retriever_from_md_files(md_files),
        name="org_information",
        description="Retriever for information stored in markdown files.",
    )

    # Add additional tools like Tavily search
    tavily_tool = TavilySearchResults(max_results=10)

    tools = [url_retriever_tool_for_langgraph, url_retriever_tool_for_md, tavily_tool]
    return tools
