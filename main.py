from flask import Flask,request,render_template,redirect,flash
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import itertools
import os
import sys

from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.corpora.dictionary import Dictionary
from collections import defaultdict
from gensim.models.tfidfmodel import TfidfModel

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_PATH'] = 'static'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
articles = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("upload.html")

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    #if request.method == 'POST' in request.files:
    #    for f in request.files:
    #        f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
    #    return 'Upload completed.'
    #return render_template('uploader.html')
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))
      #return render_template("uploader.html")
      return redirect("/")

def use():
    for i in range(10):
    # Read TXT file
        f = open(f"static\wiki_article_{i}.txt", "r")
        article = f.read()
        # Tokenize the article: tokens
        tokens = word_tokenize(article)
        # Convert the tokens into lowercase: lower_tokens
        lower_tokens = [t.lower() for t in tokens]
        # Retain alphabetic words: alpha_only
        alpha_only = [t for t in lower_tokens if t.isalpha()]
        # Remove all stop words: no_stops
        no_stops = [t for t in alpha_only if t not in ("english")]
        # Instantiate the WordNetLemmatizer
        wordnet_lemmatizer = WordNetLemmatizer()
        # Lemmatize all tokens into a new list: lemmatized
        lemmatized = [wordnet_lemmatizer.lemmatize(t) for t in no_stops]
        # list_article
        articles.append(lemmatized)
    dictionary = Dictionary(articles)
    computer_id = dictionary.token2id.get("computer")
    corpus = [dictionary.doc2bow(a) for a in articles]
    doc = corpus[9]
    tfidf = TfidfModel(corpus)
    tfidf_weights = tfidf[doc]
    #print(tfidf_weights[:5])
    sorted_tfidf_weights = sorted(tfidf_weights, key=lambda w: w[1], reverse=True)
    for term_id, weight in sorted_tfidf_weights[:5]:
        print((f"<p> {dictionary.get(term_id), weight} </p>"))
        


@app.route('/uploadyet')
def use_file():
    return render_template('uploadyet.html', output=use())


if __name__ == '__main__':
    app.run(debug=True)