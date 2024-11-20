# 1. 演示如何使用多模态输入来用“是否”来检查图片（网络连接状态）。

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import base64

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")

def get_image_text(image_path):
    # Read and encode the local image file in base64
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    
    # Create a HumanMessage with the image
    message = HumanMessage(
        content=[
            {"type": "text", "text": "describe the text in this image"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
    
    # Invoke the model to get the response
    response = model.invoke([message])
    
    return response.content

def check_network_status(image_text):
    # Create a HumanMessage asking if the network is connected based on the text in the image
    message = HumanMessage(
        content=f"Based on the following text from the image, is the network connected or not? Please provide a straight answer only: 'Connected' or 'Not connected'.\n\nText: {image_text}"
    )
    
    # Invoke the model to get the response
    response = model.invoke([message])
    
    return response.content

# List of image paths to check
image_paths = [
    # "src/lesson07_Multi_Modals/images/Connected.gif",
    "src/lesson07_Multi_Modals/images/NotConnected1.jpg",
    # "src/lesson07_Multi_Modals/images/NotConnected2.jpg",
]

# Check network status for each image
for image_path in image_paths:
    try:
        image_text = get_image_text(image_path)
        status = check_network_status(image_text)
        print(f"Image Path: {image_path}\nPic texts: {image_text}\n\nStatus: {status}\n")
        print("="*40)
    except Exception as e:
        print(f"An error occurred while processing {image_path}. Error: {e}")
