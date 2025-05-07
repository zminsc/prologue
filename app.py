import math
import networkx as nx
import numpy as np
import os
from utils import compute_similarities

CORPUS_DIR = "corpus"

corpus = sorted(
    [os.path.join(CORPUS_DIR, f) for f in os.listdir(CORPUS_DIR) if f.endswith(".txt")]
)
read = [
    "little-red-hen.txt",
    "twenty-thousand-leagues.txt",
]
want_to_read = "natural-selection.txt"


if __name__ == "__main__":
    similarities = compute_similarities(corpus)

    # convert cosine similarities to angular distances
    for i in range(len(similarities)):
        for j in range(len(similarities[i])):
            if similarities[i][j] <= 0.1:
                similarities[i][j] = 0.0
            else:
                cos = np.clip(similarities[i][j], -1.0, 1.0)
                similarities[i][j] = np.arccos(cos) * 2 / math.pi

    # build the graph
    G = nx.Graph()

    # add nodes
    G.add_nodes_from(range(len(similarities)))

    # add edges
    for i in range(len(similarities)):
        for j in range(len(similarities[i])):
            if similarities[i][j] > 0.0:
                G.add_edge(i, j, weight=float(similarities[i][j]))

    # get indices of read & want_to_read
    read = [list.index(corpus, "corpus/" + title) for title in read]
    want_to_read = list.index(corpus, "corpus/" + want_to_read)

    distances, paths = nx.single_source_dijkstra(G, want_to_read)  # type: ignore

    print(f"Shortest distance and path from {corpus[want_to_read]} to:")
    for i in read:
        print(f"{corpus[i]}: {distances[i]}, path=[")
        print(",\n".join([f"\t{corpus[idx]}" for idx in paths[i]]))
        print("]")
