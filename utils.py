import math
import networkx as nx
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def compute_cosine_similarities(corpus):
    vectorizer = TfidfVectorizer(
        input="filename", stop_words="english", min_df=2, max_df=0.9, ngram_range=(1, 2)
    )
    X = vectorizer.fit_transform(corpus)
    return cosine_similarity(X)


def angular_distance(cosine_similarity):
    cos = np.clip(cosine_similarity, -1.0, 1.0)
    return np.arccos(cos) * 2 / math.pi


def build_graph(cosine_similarities, distance_function=angular_distance, top_k=3):
    G = nx.Graph()
    G.add_nodes_from(range(len(cosine_similarities)))

    # convert top k similarities to distance and add as edges
    for i in range(len(cosine_similarities)):
        top_k_similar = sorted(
            enumerate(cosine_similarities[i]), key=lambda x: x[1], reverse=True
        )[
            1 : top_k + 2
        ]  # start at 1 to exclude similarity 1.0 (self)

        for j, sim in top_k_similar:
            G.add_edge(i, j, weight=distance_function(sim))

    return G


def build_reading_plan(G, read, want_to_read):
    distances, paths = nx.single_source_dijkstra(G, want_to_read)
    valid_paths = [(distances[i], paths[i]) for i in range(len(distances)) if i in read]
    reading_plan = min(valid_paths, key=lambda x: x[0])[1]
    return list(reversed(reading_plan))
