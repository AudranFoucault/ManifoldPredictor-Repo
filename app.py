from flask import Flask, request, render_template
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import os
import anthropic
import json

app = Flask(__name__)
CORS(app)
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(
    api_key = api_key,
    timeout = 15.0
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=['POST'])
def analyze():
    data = request.get_json(force=True)
    market_id = data["market_id"]
    url = f"https://api.manifold.markets/markets-by-ids?ids%5B%5D={market_id}"
    manifold_response = requests.get(url)
    manifold_data = manifold_response.json()
    first_item = manifold_data[0]
    question = first_item["question"]
    try:      
        yes_prob = round(manifold_data[0]["prob"], 2)
        no_prob = 1 - yes_prob
    except: 
        answers = manifold_data[0]["answers"]
        yes_prob = round(answers[0]["prob"], 2) 
        no_prob = 1 - yes_prob * 100

    response_format = '{"Yes": 0, "No": 0, "Confidence": ["Low", "Medium", "High"]}'
    prompt = prompt = f"You are a probability engine. For this question: {question}\n\nRespond ONLY with valid JSON, nothing else. Use this exact format:\n{response_format}\n\nNo explanations. No markdown. No text before or after. JSON ONLY."
    message = None
    try:
        message = client.messages.create(
            model = "claude-sonnet-4-20250514",
            max_tokens = 200,
            messages = [
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        print("ERROR", e)
    
    claude_response = message.content[0].text

    try:
        claude_data = json.loads(claude_response)
    except json.JSONDecodeError:
        print("Bad Response:", claude_response)
        exit()
    
    return {
        "question": question,
        "manifold_yes": yes_prob * 100,
        "manifold_no": no_prob * 100,
        "claude_yes": claude_data["Yes"],
        "claude_no": claude_data["No"]
    }
    
    
    
