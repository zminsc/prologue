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


def build_graph(cosine_similarities, threshold=0.1, distance_function=angular_distance):
    G = nx.Graph()
    G.add_nodes_from(range(len(cosine_similarities)))

    # convert all similarities above threshold to distance and add as edges
    for i in range(len(cosine_similarities)):
        for j in range(i + 1, len(cosine_similarities[i])):
            if cosine_similarities[i][j] <= threshold:
                continue

            G.add_edge(i, j, weight=distance_function(cosine_similarities[i][j]))

    return G


def build_reading_plan(G, read, want_to_read):
    distances, paths = nx.single_source_dijkstra(G, want_to_read)
    valid_paths = [(distances[i], paths[i]) for i in range(len(distances)) if i in read]
    reading_plan = min(valid_paths, key=lambda x: x[0])[1]
    return list(reversed(reading_plan))
