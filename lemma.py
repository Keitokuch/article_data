import csv
from pymysql.err import *
import nltk
import pymysql
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import json
from dbconfig import db_config


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


# csv fields: 0 = article_id; 1 = title; 2 = authors; 9 = link; 10 = abstract;
# 11 = date; 12 = journal_name; 13 = journal_id;
connection = pymysql.connect(**db_config)
with open("0.csv") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    with connection.cursor() as cursor:
        query = """
        INSERT INTO article_lemma
        VALUE (%(id)s, %(lemma)s)
        ;
        """
        i = 0
        for row in reader:
            aid = int(row[0])
            if aid > 800000 and aid != 1778082:
                break
            if row[10] != '':
                title_list = lemmatize(row[0])
                abstract_list = lemmatize(row[10])
                lemma = title_list + abstract_list
                lemma_json = json.dumps(lemma)
                try:
                    ret = cursor.execute(query, {'id': row[0],
                                                 'lemma': lemma_json
                                                 }
                                         )
                    i += 1
                except MySQLError as err:
                    if err.args[0] != 1062:
                        print(err)
                        print(row[0])
            else:
                print('empty abstract', i)
print(i)


connection.commit()
connection.close()
