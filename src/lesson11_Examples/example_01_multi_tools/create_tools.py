import sys
import os

from .tools.create_md_files_retriever_tool import create_md_files_retriever_tool
from .tools.create_search_engine_tool import create_search_engine_tool
from .tools.create_url_retriever_tool import create_url_retriever_tool

import os

def create_tools():
    """Creates and returns all tools by combining specific tool creation methods."""
    url_retriever_tool = create_url_retriever_tool()
    md_files_tool = create_md_files_retriever_tool()
    search_engine_tool = create_search_engine_tool()

    tools = [url_retriever_tool, md_files_tool, search_engine_tool]
    return tools
