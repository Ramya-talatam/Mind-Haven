#from flask import Flask,render_template, request, jsonify
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
import string

#app = Flask(__name__)

# Sample journal content
journal_entries = [
    "Today was a great day. I accomplished a lot and felt really productive.",
    "I'm feeling a bit tired today. It's been a tough week at work.",
    "I spent the evening reading a fascinating book about space exploration."
]

# Initialize TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Initialize sentiment analysis
def fun(journal_entry):
    journal_entries=journal_entry.split(".")
    positive_words = []
    negative_words = []

    for entry in journal_entries:
        analysis = TextBlob(entry)
        for word in word_tokenize(entry):
            if "'" in word:
                word = "."
            if word not in string.punctuation and word.lower() not in tfidf_vectorizer.get_stop_words():
                word_polarity = TextBlob(word.lower()).sentiment.polarity
                if analysis.sentiment.polarity >= 0.05 and word_polarity > 0:
                    positive_words.append([word.lower(), word_polarity])
                elif analysis.sentiment.polarity <= -0.05 and word_polarity < 0:
                    negative_words.append([word.lower(), word_polarity])

    tfidf_matrix = tfidf_vectorizer.fit_transform(journal_entries)
    tfidf_scores = tfidf_matrix.sum(axis=0)
    tfidf_features = tfidf_vectorizer.get_feature_names_out()
    focused_words = [tfidf_features[i] for i in tfidf_scores.argsort()[0, -5:]]
    f=[item for sublist in focused_words for item in sublist[0]]
    return [positive_words, negative_words, f,TextBlob(journal_entry).sentiment.polarity]
# @app.route('/analyze', methods=['POST'])
# def analyze():
#     journal_text = request.form.get('journalText')
#     positive_words, negative_words, focused_words= fun(journal_text)
#     response = {
#         'positive_words': positive_words,
#         'negative_words': negative_words,
#         'focused_words': focused_words,
#         'overall_polarity': TextBlob(journal_text).sentiment.polarity
#     }
#     return jsonify(response)
# @app.route('/')
# def index():
#     return render_template('index.html')
# if __name__ == '__main__':
#     app.run(debug=True)
