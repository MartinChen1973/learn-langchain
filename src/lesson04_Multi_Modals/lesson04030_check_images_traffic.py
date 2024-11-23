# 1. 演示用压缩过的图片仍能精准判断图片中的内容，可以有效降低费用。

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
import base64
from PIL import Image

# Load environment variables
load_dotenv(find_dotenv())

# Initialize the ChatOpenAI model
model = ChatOpenAI(model="gpt-4o")

def compress_image(image_path, max_size=(100, 100)):
    """Compress the image to the specified maximum size."""
    with Image.open(image_path) as img:
        img.thumbnail(max_size, Image.LANCZOS)  # Use LANCZOS filter for resizing
        compressed_image_path = image_path.replace('.png', '_compressed.png')  # Create a new file name
        img.save(compressed_image_path, format='PNG')  # Save the compressed image
    return compressed_image_path

def get_image_text(question, image_path):
    # Compress the image
    compressed_image_path = compress_image(image_path)
    
    # Read and encode the local image file in base64
    with open(compressed_image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    
    # Create a HumanMessage with the image and question
    message = HumanMessage(
        content=[
            {"type": "text", "text": question},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
    
    # Invoke the model to get the response
    response = model.invoke([message])
    
    return response.content

# List of image paths to check
question_to_images = {
    "图中有人在闯红灯吗？（仅回答“是”或“否”，不要解释，不要标点符号）": "src/lesson04_Multi_Modals/images/pedestrian_jaywalking.png",
    # "图中路口有车辆在等待吗？（仅回答“是”或“否”，不要解释，不要标点符号）": "src/lesson04_Multi_Modals/images/empty_street.png",
}

# Check network status for each image
for question, image_path in question_to_images.items():
    try:
        image_text = get_image_text(question, image_path)
        print(f"Question: {question}\nResponse: {image_text}\n")
    except Exception as e:
        print(f"An error occurred while processing {image_path}. Error: {e}")
