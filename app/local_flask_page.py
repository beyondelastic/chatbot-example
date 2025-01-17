# create a webserver using the flask framework
# import all modules needed

import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# create the flask object
app = Flask(__name__)

# Load Azure OpenAI configuration from environment variables
AZURE_OPENAI_API_KEY = os.getenv("API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("API_Endpoint")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("Deployment_Name")

@app.route("/")
def index():
    return """
    <html>
        <body>
            <h1>Welcome to the Basketball Equipment Shop</h1>
            <div id="chatbox">
                <p id="chatlog"></p>
                <input type="text" id="userInput" placeholder="Type a message...">
                <button onclick="sendMessage()">Send</button>
            </div>
            <script>
                function sendMessage() {
                    var userInput = document.getElementById('userInput').value;
                    fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({message: userInput}),
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('chatlog').innerHTML += '<br>User: ' + userInput;
                        document.getElementById('chatlog').innerHTML += '<br>Bot: ' + data.reply;
                        document.getElementById('userInput').value = '';
                    });
                }
            </script>
        </body>
    </html>
    """

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    bot_reply = generate_bot_reply(user_message)
    return jsonify({"reply": bot_reply})

def generate_bot_reply(message):
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY,
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are an AI assistant for an online basketball equipment shop. Provide helpful information about basketball products and assist with any inquiries related to basketball equipment. Keep your answers short and precise."},
            {"role": "user", "content": message}
        ],
        "max_tokens": 100,
    }
    response = requests.post(
        f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version=2024-08-01-preview",
        headers=headers,
        json=data,
    )
    
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"
    
    response_json = response.json()
    
    if "choices" not in response_json:
        return f"Error: Unexpected response format - {response_json}"
    
    return response_json["choices"][0]["message"]["content"].strip()


#run the flask object
if __name__ == "__main__":
    app.run(debug=True)


