import os
from utils import build_reading_plan, compute_cosine_similarities, build_graph

CORPUS_DIR = "corpus"

corpus = sorted(
    [os.path.join(CORPUS_DIR, f) for f in os.listdir(CORPUS_DIR) if f.endswith(".txt")]
)

# helper dictionaries
title_to_idx = {os.path.basename(p): i for i, p in enumerate(corpus)}
idx_to_title = {i: os.path.basename(p) for i, p in enumerate(corpus)}


if __name__ == "__main__":
    similarities = compute_cosine_similarities(corpus)
    G = build_graph(similarities)

    want_to_read = "black-beauty.txt"
    read = [
        "little-red-hen.txt",
        "twenty-thousand-leagues.txt",
    ]

    # get indices of read & want_to_read
    idx_want_to_read = title_to_idx[want_to_read]
    idx_read = [title_to_idx[title] for title in read]
    reading_plan = build_reading_plan(G, idx_read, idx_want_to_read)

    print(f"Based on the books you've read, here is a reading plan for {want_to_read}:")
    print("---")
    print(
        "\n".join(
            [
                f"{i + 1}. {idx_to_title[idx_title]}"
                for i, idx_title in enumerate(reading_plan)
            ]
        )
    )
    print("---")
    print("Enjoy!")
