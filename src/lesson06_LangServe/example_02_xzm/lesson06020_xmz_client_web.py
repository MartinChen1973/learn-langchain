# 模拟的小程序客户端，用法:
# 1. 请先运行server端（参考server端的代码末尾用法）
# 2. （在vscode中）/Terminal/New Terminal打开一个终端窗口（此时应该位于项目根目录)
# 3. （在vscode中）按右上运行本文件
# 4. 在终端中找到如下的字样：Running on http://localhost:5021
# 5. 按Ctrl+鼠标左键点击

from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# Define the API URL
API_URL = "http://localhost:8930/ask"

# HTML template for the client interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Q&A System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        .container { max-width: 600px; margin: auto; }
        h1 { text-align: center; color: #333; }
        textarea { width: 100%; height: 100px; margin-bottom: 1em; font-size: 16px; }
        button { padding: 0.5em 1em; font-size: 16px; }
        .response { margin-top: 1em; background: #f9f9f9; padding: 1em; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Q&A System</h1>
        <textarea id="question" placeholder="Enter your question here..."></textarea>
        <button onclick="askQuestion()">Ask</button>
        <div id="response" class="response" style="display: none;"></div>
    </div>
    <script>
        async function askQuestion() {
            const question = document.getElementById('question').value;
            const responseDiv = document.getElementById('response');

            if (!question.trim()) {
                responseDiv.style.display = 'none';
                return alert('Please enter a question.');
            }

            const payload = { question: question };
            
            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const data = await response.json();
                responseDiv.style.display = 'block';
                responseDiv.textContent = data.answer || 'No answer provided.';
            } catch (error) {
                responseDiv.style.display = 'block';
                responseDiv.textContent = 'An error occurred. Please try again.';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """Serve the HTML page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    """Handle the question and forward it to the external API."""
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    # Forward the question to the external API
    try:
        response = requests.post(API_URL, json={"question": user_question})
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": f"API error: {response.status_code}"}), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": "Unable to connect to the external API"}), 500

if __name__ == '__main__':
    app.run(port=5021)
