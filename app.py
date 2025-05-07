import streamlit as st
import os
import numpy as np
import networkx as nx  # imported for type hinting
from utils import build_reading_plan, compute_cosine_similarities, build_graph

CORPUS_DIR = "corpus"


# caching functions for expensive operations
@st.cache_data
def load_corpus_data():
    """
    Loads book titles from the CORPUS_DIR.
    Returns a tuple: (corpus_paths, book_titles, title_to_idx_map, idx_to_title_map, error_occurred_flag).
    """
    if not os.path.isdir(CORPUS_DIR):
        return (
            [],
            [],
            {},
            {},
            True,
        )  # True = error state

    try:
        corpus_filenames = sorted(
            [f for f in os.listdir(CORPUS_DIR) if f.endswith(".txt")]
        )
    except OSError:  # catch potential OS errors during listdir
        return [], [], {}, {}, True

    if not corpus_filenames:
        return [], [], {}, {}, False

    corpus_paths = [os.path.join(CORPUS_DIR, f) for f in corpus_filenames]
    titles = [os.path.basename(p) for p in corpus_paths]

    title_to_idx_map = {title: i for i, title in enumerate(titles)}
    idx_to_title_map = {i: title for i, title in enumerate(titles)}

    return corpus_paths, titles, title_to_idx_map, idx_to_title_map, False


@st.cache_data
def calculate_book_similarities(corpus_file_paths):
    """Computes cosine similarities between books in the corpus."""
    if not corpus_file_paths:
        return np.array([])
    return compute_cosine_similarities(corpus_file_paths)


@st.cache_data
def create_similarity_graph(_similarity_matrix):
    """Builds a graph of books based on their similarity matrix."""
    if not isinstance(_similarity_matrix, np.ndarray) or _similarity_matrix.size == 0:
        return nx.Graph()
    return build_graph(_similarity_matrix)


# --- Streamlit App UI ---

st.set_page_config(page_title="prologue", layout="centered")
st.title("prologue")

# load initial data from the corpus
corpus_file_paths, all_book_titles, title_to_idx, idx_to_title, load_error = (
    load_corpus_data()
)

if load_error:
    st.error(
        f"Critical Error: The corpus directory '{CORPUS_DIR}' was not found or is inaccessible. "
        "Please ensure it exists and contains '.txt' book files."
    )
    st.stop()
elif not all_book_titles:
    st.warning(
        f"No '.txt' book files found in the '{CORPUS_DIR}' directory. "
        "Please add some books to generate a reading plan."
    )
    st.stop()

similarity_matrix = calculate_book_similarities(corpus_file_paths)
book_graph = create_similarity_graph(similarity_matrix)

# UI for selecting books
selected_read_titles = st.multiselect(
    "Which of these books have you already read?", options=all_book_titles, default=[]
)

# filter out read books from "want to read"
available_target_books = sorted(
    [title for title in all_book_titles if title not in selected_read_titles]
)

selected_want_to_read_title = st.selectbox(
    "Which book do you want to read next?",
    options=available_target_books,
    index=None,
    placeholder=(
        "Select a book..."
        if available_target_books
        else "No other books available to select"
    ),
)

if st.button("Generate Reading Plan"):
    if not selected_read_titles:
        st.warning("Please select at least one book you have read.")
    elif not selected_want_to_read_title:
        st.warning("Please select a book you want to read.")
    elif book_graph.number_of_nodes() == 0:
        st.error(
            "The book similarity graph could not be built, possibly due to issues with the corpus data."
        )
    else:
        idx_read = [title_to_idx[title] for title in selected_read_titles]
        idx_want_to_read = title_to_idx[selected_want_to_read_title]

        try:
            reading_plan_indices = build_reading_plan(
                book_graph, idx_read, idx_want_to_read
            )

            if reading_plan_indices:
                st.subheader(f"Your Reading Plan for '{selected_want_to_read_title}':")

                plan_display_steps = []
                for i, idx_title in enumerate(reading_plan_indices):
                    plan_display_steps.append(f"{i + 1}. {idx_to_title[idx_title]}")

                st.markdown("\n".join(plan_display_steps))
                st.markdown("---")
                st.markdown("Enjoy your reading journey!")
            else:
                st.info(
                    f"A direct reading path could not be determined for '{selected_want_to_read_title}' based on your read books and current similarity settings."
                )

        except ValueError:
            st.error(
                f"Could not generate a reading plan. No suitable path found from the books you've read to '{selected_want_to_read_title}'. "
                "Consider selecting different books or adding more books to your 'read' list."
            )
        except nx.NodeNotFound:
            st.error(
                f"Error in graph processing. One of the selected books might not be properly represented in the book graph. This can happen if the corpus is very small or books are too dissimilar."
            )
        except Exception as e:
            st.error(
                f"An unexpected error occurred while generating the plan: {str(e)}"
            )
