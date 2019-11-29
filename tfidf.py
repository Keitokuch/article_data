import numpy as np
import scipy.sparse
#  from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_distances
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
#  from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import pymysql
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import time
import json
from dbconfig import db_config


def timer():
    while True:
        last = time.time()
        yield time.time() - last


class Timer:
    def __init__(self):
        self.now = time.time()
        self.last = self.now

    def __call__(self, title=''):
        print(title, f'{next(self):.3f}s')

    def __next__(self):
        self.last = self.now
        self.now = time.time()
        return self.now - self.last


def dummy_func(x):
    return x


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)


tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
def lemmatize(text):
    tokens = tokenizer.tokenize(text.lower())
    filtered = filter(lambda token: token not in stop_words, tokens)
    return [lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in filtered]


start = time.time()
timer = Timer()
connection = pymysql.connect(**db_config)
with connection.cursor() as cursor:
    query = """
            SELECT *
            FROM article_lemma
            ;
    """
    cursor.execute(query)
    lemma_abstract = cursor.fetchall()

print(f'select {time.time() - start}s')
start = time.time()
timer('select')

text = [json.loads(item['lemma_list']) for item in lemma_abstract]
ids = [item['article_id'] for item in lemma_abstract]
print(f'text {time.time() - start}s')
start = time.time()
timer('text')

#  tfidf = TfidfVectorizer(max_df=0.2,
                        #  lowercase=False, analyzer='word',
                        #  tokenizer=dummy_func, preprocessor=dummy_func,
                        #  token_pattern=None)
#  vectors = tfidf.fit_transform(text)
vectors = scipy.sparse.load_npz('lemma_vectors.npz')
print(f'vectorize {time.time() - start}s')
timer('vectorize')
print(type(vectors), vectors.shape)

#  np.save('lemma_vectors', vectors, allow_pickle=False)
scipy.sparse.save_npz('lemma_vectors.npz', vectors)

knn = NearestNeighbors(n_neighbors=5, metric='cosine')
knn.fit(vectors)

timer('knn')
#  query_phrase = "Artificial intelligence machine learning"
#  query = lemmatize(query_phrase)
#  print(query)
#  query_vector = tfidf.transform([query])

#  t1 = tfidf.inverse_transform(vectors[0])
#  print(t1)
#  print(text[5])
#  print(text[1003])
dists, indices = knn.kneighbors(vectors[1003])
for i in range(5):
    print('#{} distance: {}, text:\n{} \n'.format(i, dists[0][i], text[indices[0][i]]))
