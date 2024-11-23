# 1. 演示用gpt4o模型描述图片的内容

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import base64

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")

def get_image_description(image_path):
    # Read and encode the local image file in base64
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    
    # Create a HumanMessage to request a description of the image
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Please provide a detailed description of this image."},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
    
    # Invoke the model to get the response
    response = model.invoke([message])
    
    return response.content

# List of image paths to describe
image_paths = [
    "src/lesson04_Multi_Modals/images/Connected.gif",
    # "src/lesson04_Multi_Modals/images/NotConnected1.jpg",
    # "src/lesson04_Multi_Modals/images/NotConnected2.jpg",
]

# Describe each image
for image_path in image_paths:
    try:
        description = get_image_description(image_path)
        print(f"Image Path: {image_path}\nDescription: {description}\n")
        print("-"*40)
    except Exception as e:
        print(f"An error occurred while processing {image_path}. Error: {e}")
