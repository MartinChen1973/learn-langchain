import sys
import os

from src.utilities.create_retriever_from_md_files import create_retriever_from_md_files, find_md_files
from src.utilities.create_retriever_from_urls import create_retriever_from_urls, load_urls

from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools.tavily_search import TavilySearchResults

import os

def create_url_retriever_tool():
    """Creates a retriever tool for Langgraph official website."""
    urls_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_data", "Langgraph_official_website.urls")
    name, description, urls = load_urls(urls_file)

    url_retriever_tool = create_retriever_tool(
        retriever=create_retriever_from_urls(urls),
        name=name,
        description=description,
    )
    return url_retriever_tool
