# 模拟的小程序客户端，用法请参考server端的代码

import requests

# Define the URL of the API endpoint
url = "http://localhost:8930/ask"

print("Welcome to the Q&A System! Type 'exit' to quit.\n")

while True:
    # Get the user's question
    user_question = input("Enter your question: ")
    
    # Exit condition
    if user_question.lower() == "exit":
        print("Thank you for using the Q&A System. Goodbye!")
        break
    
    # Define the question to be sent to the server
    question = {
        "question": user_question
    }

    # Send a POST request to the /ask endpoint with the question as JSON
    response = requests.post(url, json=question)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract and print only the answer
        answer_text = response.json().get("answer", "No answer provided")
        print(answer_text)
    else:
        # Print an error message if something went wrong
        print("Oops! Something went wrong.")
        print(f"Error {response.status_code}: {response.text}")

# Example questions:
# 小孩感冒了怎么办？
# 睡眠不足头晕怎么办？
# 得了阑尾炎怎么办？