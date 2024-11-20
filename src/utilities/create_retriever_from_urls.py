from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def create_retriever_from_urls(urls, chunk_size=1000, chunk_overlap=200):
    """
    Creates a retriever using documents fetched from the given URLs with FAISS.

    Parameters:
        urls (list): A list of URLs to load documents from.
        chunk_size (int): The size of each text chunk. Default is 1000.
        chunk_overlap (int): The overlap size between chunks. Default is 200.

    Returns:
        retriever: A retriever object based on the FAISS vectorstore.
    """
    try:
        # Load documents from the URLs
        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]

        # Split the documents into chunks
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        doc_splits = text_splitter.split_documents(docs_list)

        # Create a FAISS vectorstore and initialize the retriever
        vectorstore = FAISS.from_documents(
            documents=doc_splits,
            embedding=OpenAIEmbeddings(),
        )
        return vectorstore.as_retriever()

    except Exception as e:
        print(f"Error creating retriever: {e}")
        return None

def load_urls(file_path):
    """
    Load the name, description, and URLs from a text file.
    
    :param file_path: Path to the text file.
    :return: A tuple (name, description, urls).
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Warning: File not found: {file_path}")
        return None, None, []

    # Extract the name from the file name (without path and extension)
    name = os.path.splitext(os.path.basename(file_path))[0]

    # Initialize variables
    description = None
    urls = []

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]  # Remove empty lines

    if lines:
        description = lines[0]  # First line as the description
        urls = lines[1:]  # Remaining lines as URLs
    else:
        print(f"Warning: No content found in the file: {file_path}")

    return name, description, urls