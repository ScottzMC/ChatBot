import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt_tab')

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

    def get_response(self, user_query):
        """
        Get the chatbot's response to a user query.
        :param user_query: The user's input text.
        :return: A response string.
        """
        response = self.find_best_match(user_query)
        if response:
            return response
        return "I'm sorry, I don't have an answer for that. Please try asking something else!"


# Example usage
if __name__ == "__main__":
    faq = {
        "What is your name?": "I am a chatbot, here to assist you.",
        "How can I help you?": "You can ask me questions about various topics.",
        "What is Python?": "Python is a versatile programming language."
    }

    bot = Chatbot(faq)
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye!")
            break
        print(f"Chatbot: {bot.get_response(user_input)}")