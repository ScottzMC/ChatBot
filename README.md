# ChatBot
 
# AI Chatbot with Flask and NLP 🧠💬

An AI-powered chatbot built with Python, Flask, and Natural Language Processing (NLP). This chatbot is designed to answer frequently asked questions (FAQs) using TF-IDF and cosine similarity and provides a polite fallback response for unmatched queries.

## 📚 Features
- **FAQ Matching**: Uses NLP techniques to process user input and match it with predefined FAQs.
- **Fallback Response**: Handles queries that don't match the FAQs with a generic response.
- **Web Interface**: A user-friendly web interface built using Flask and HTML.
- **Extensible**: Easily add new FAQs or improve functionality.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **NLP**: NLTK, TF-IDF (scikit-learn)
- **Frontend**: HTML, CSS (via Flask templates)

---

## 🚀 How It Works
1. User inputs a query via the web interface.
2. The query is preprocessed using NLP techniques (tokenization, lemmatization, stopword removal).
3. The chatbot calculates the similarity between the query and predefined FAQs using TF-IDF and cosine similarity.
4. If a match is found:
   - The corresponding FAQ answer is returned.
   - If no match is found, a fallback response is provided.
5. The response is displayed on the web interface.

---

## 📂 Project Structure
chatbot_project/
│
├── app.py            # Flask backend
├── chatbot.py        # Core chatbot logic (FAQs, NLP handling)
├── templates/
│   └── index.html    # Frontend HTML interface
├── static/
│   └── style.css     # (Optional) CSS styling
└── requirements.txt  # Dependencies

---

## 🧑‍💻 Setup Instructions

### **1. Clone the Repository**
```bash
git clone https://github.com/<your-username>/ChatBot.git
cd ChatBot

### **2. Install Dependencies**

python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt

### **3. Run the Application**
Start the flask server
python app.py

Visit the project
http://127.0.0.1:5000/

## 📝 Adding/Updating FAQs
1. Open chatbot.py.
2. Update the faq dictionary with new questions and answers:
faq = {
    "What is your name?": "I am a chatbot, here to assist you.",
    "How can I help you?": "You can ask me questions about various topics.",
    "What is Python?": "Python is a versatile programming language.",
    "Your new question here": "Your new answer here"
}
