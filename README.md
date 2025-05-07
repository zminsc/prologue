# prologue

**prologue** is a Streamlit-based web application designed to help users discover and follow a personalized reading plan, building your "prologue" to a book you want to read. It leverages document-search techniques such as tf-idf vectors and cosine similarity to build an interconnected graph of books. The texts in `corpus` are free to use and publicly available at [Project Gutenberg](https://gutenberg.org). Feel free to replace these texts with your own bookshelf!

## Prerequisites

To run this project locally, you'll need:

* Python (version 3.8 or higher)
* pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-directory>
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Prepare Your Corpus

Create a directory named `corpus` at the root of the project and populate it with `.txt` files containing the books you'd like to analyze. If you've cloned this repository, simply add or remove books as desired from the existing `corpus` folder.

Example:

```
prologue/
├── app.py
├── utils.py
├── requirements.txt
└── corpus/
    ├── book1.txt
    ├── book2.txt
    └── ...
```

## Running the Application

With your virtual environment activated, launch the Streamlit app:

```bash
streamlit run app.py
```

Your default web browser should automatically open and display the application. If not, navigate to the URL provided in the terminal, typically `http://localhost:8501`.

## Usage

1. Select books you've already read from the provided list.
2. Choose a book you'd like to read next.
3. Click on **Generate Reading Plan** to view a tailored reading pathway.

Enjoy discovering your next great read!
