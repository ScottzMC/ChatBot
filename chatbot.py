import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import openai
import os
from dotenv import load_dotenv

from urllib.request import urlopen
import socket

# Increase timeout for downloads
socket.setdefaulttimeout(1000)

# Download required data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading stopwords...")
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading punkt...")
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("Downloading wordnet...")
    nltk.download('wordnet')

# Load API key from .env file (make sure to create one with OPENAI_API_KEY=<your_key>)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class Chatbot:
    def __init__(self, faq_data):
        """
        Initialize the chatbot with FAQ data and NLP tools.
        :param faq_data: A dictionary where keys are questions and values are answers.
        """
        self.faq_data = faq_data
        self.questions = list(faq_data.keys())
        self.answers = list(faq_data.values())
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.questions)
        self.stop_words = set(stopwords.words('english'))

        # Set OpenAI API key
        openai.api_key = OPENAI_API_KEY

    def preprocess(self, text):
        """
        Preprocess text by tokenizing, removing stopwords, and lemmatizing.
        :param text: The input text string.
        :return: A preprocessed text string.
        """
        tokens = word_tokenize(text.lower())
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word.isalnum()]
        tokens = [word for word in tokens if word not in self.stop_words]
        return " ".join(tokens)

    def find_best_match(self, user_query):
        """
        Find the best matching FAQ for the user's query using cosine similarity.
        :param user_query: The user's input text.
        :return: The best match's answer or None if no match is found.
        """
        preprocessed_query = self.preprocess(user_query)
        query_vector = self.vectorizer.transform([preprocessed_query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)
        best_match_idx = np.argmax(similarities)

        if similarities[0, best_match_idx] > 0.3:  # Threshold for similarity
            return self.answers[best_match_idx]
        return None

    def openai_fallback(self, user_query):
        """
        Generate a response using OpenAI GPT when no FAQ match is found.
        :param user_query: The user's input text.
        :return: A response string from OpenAI GPT.
        """
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"You are a helpful assistant. Answer the following: {user_query}",
                max_tokens=150,
                temperature=0.7,
            )
            return response['choices'][0]['text'].strip()
        except Exception as e:
            return "I'm having trouble connecting to the external system. Please try again later."
    def get_response(self, user_query):
        """
        Get the chatbot's response to a user query.
        """
        response = self.find_best_match(user_query)
        if response:
            return response
        # Fallback to OpenAI GPT if no match is found
        return self.openai_fallback(user_query)

# Example FAQ data for testing
if __name__ == "__main__":
    faq = {
        "What is your name?": "I am a chatbot, here to assist you.",
        "How can I help you?": "You can ask me questions about various topics."
    }

    bot = Chatbot(faq)
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye!")
            break
        print(f"Chatbot: {bot.get_response(user_input)}")