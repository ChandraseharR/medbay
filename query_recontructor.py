from sklearn.metrics.pairwise import cosine_similarity
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

wnl = WordNetLemmatizer()

def penn2morphy(penntag):
    morphy_tag = {'NN': 'n', 'JJ': 'a', 'VB': 'v', 'RB': 'r'}
    return morphy_tag.get(penntag[:2], 'n')

def lemmatize_sent(text):
    tokens = word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    lemmatized_words = [wnl.lemmatize(word.lower(), pos=penn2morphy(tag)) for word, tag in pos_tags]
    return lemmatized_words[0]

def remove_stopwords_from_file(content):
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(content)
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
    return filtered_tokens

def query_reconstruction(query_list):
    with open('./Dataset/tf_idf_matrix.pkl','rb') as file:
        df = pickle.load(file)
    reconstructed_query = []
    for i in query_list:
        cosine_similarities = cosine_similarity(i, df)
        top_two_indices = cosine_similarities[0].argsort()[-2:][::-1]
        for syptoms in top_two_indices:
            if cosine_similarities[0][syptoms] == 0.0:
                continue
            reconstructed_query.append(df.index[syptoms])
    return reconstructed_query

def query_list_creation(query):
    query_list = []
    with open('./Dataset/tfidf_vectorizer.pkl','rb') as vectoriser_file:
        tfidf_vectorizer = pickle.load(vectoriser_file)
    for i in query.split(','): 
        q = remove_stopwords_from_file(i) 
        vector = []
        for token in q:
            vector.append(lemmatize_sent(token))
        vector = ' '.join(vector)
        query_vector = tfidf_vectorizer.transform([vector])
        query_list.append(query_vector.toarray().tolist())
    return query_list

def recon(query):
    q_list = query_list_creation(query)
    return query_reconstruction(q_list)