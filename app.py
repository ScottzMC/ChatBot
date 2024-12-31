from flask import Flask, request, jsonify, render_template
from chatbot import Chatbot

# Initialize Flask app
app = Flask(__name__)

# Sample FAQ data
faq = {
    "What is your name?": "I am a chatbot, here to assist you.",
    "How can I help you?": "You can ask me questions about various topics.",
    "What is Python?": "Python is a versatile programming language."
}

# Initialize Chatbot with FAQ data
bot = Chatbot(faq)


@app.route("/")
def home():
    """
    Render the homepage.
    """
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_response():
    """
    API endpoint to get the chatbot's response to a user query.
    :return: A JSON response containing the chatbot's reply.
    """
    user_query = request.json.get("query", "")
    if not user_query:
        return jsonify({"response": "Please provide a valid query!"})

    response = bot.get_response(user_query)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)