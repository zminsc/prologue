from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_similarities(corpus):
    vectorizer = TfidfVectorizer(
        input="filename", stop_words="english", min_df=2, max_df=0.9, ngram_range=(1, 2)
    )
    X = vectorizer.fit_transform(corpus)
    return cosine_similarity(X)
