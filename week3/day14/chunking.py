from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter
)

from sentence_transformers import SentenceTransformer
import numpy as np


# =========================================================
# SAMPLE TEXT
# =========================================================

text = """
Artificial Intelligence is transforming the world. It enables machines
to perform tasks that normally require human intelligence.

Machine Learning is a subset of Artificial Intelligence. It allows
computers to learn patterns from data without being explicitly programmed.

Deep Learning is a subset of Machine Learning. It uses neural networks
with multiple layers to solve complex problems.

Python is one of the most popular programming languages for Artificial
Intelligence and Machine Learning. Libraries such as NumPy, Pandas,
TensorFlow and PyTorch are widely used.
"""


# =========================================================
# 1. PARAGRAPH CHUNKING
# =========================================================

def paragraph_chunking(text):
    chunks = text.split("\n\n")

    # Remove empty chunks
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]

    return chunks


# =========================================================
# 2. FIXED SIZE CHUNKING
# =========================================================

def fixed_chunking(text, chunk_size=100, overlap=20):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start = end - overlap

    return chunks


# =========================================================
# 3. RECURSIVE CHUNKING
# =========================================================

def recursive_chunking(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=30,
        separators=[
            "\n\n",  # Paragraph
            "\n",    # New line
            ". ",    # Sentence
            " ",     # Word
            ""       # Character
        ]
    )

    chunks = splitter.split_text(text)

    return chunks


# =========================================================
# 4. SEMANTIC CHUNKING
# =========================================================

def semantic_chunking(text):

    # Split text into sentences
    sentences = [
        sentence.strip()
        for sentence in text.replace("\n", " ").split(".")
        if sentence.strip()
    ]

    # Load embedding model
    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    # Create embeddings
    embeddings = model.encode(sentences)

    chunks = []
    current_chunk = [sentences[0]]

    # Similarity threshold
    threshold = 0.5

    for i in range(1, len(sentences)):

        previous_embedding = embeddings[i - 1]
        current_embedding = embeddings[i]

        # Cosine Similarity
        similarity = np.dot(
            previous_embedding,
            current_embedding
        ) / (
            np.linalg.norm(previous_embedding)
            *
            np.linalg.norm(current_embedding)
        )

        # If sentences are semantically similar
        # keep them in the same chunk
        if similarity >= threshold:

            current_chunk.append(sentences[i])

        else:

            chunks.append(
                ". ".join(current_chunk) + "."
            )

            current_chunk = [sentences[i]]

    # Add final chunk
    if current_chunk:
        chunks.append(
            ". ".join(current_chunk) + "."
        )

    return chunks


# =========================================================
# FUNCTION TO PRINT CHUNKS
# =========================================================

def print_chunks(title, chunks):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    for i, chunk in enumerate(chunks, 1):

        print(f"\nChunk {i}:")
        print(chunk)


# =========================================================
# RUN ALL CHUNKING METHODS
# =========================================================


# Paragraph Chunking
paragraph_chunks = paragraph_chunking(text)

print_chunks(
    "PARAGRAPH CHUNKING",
    paragraph_chunks
)


# Fixed Size Chunking
fixed_chunks = fixed_chunking(
    text,
    chunk_size=100,
    overlap=20
)

print_chunks(
    "FIXED SIZE CHUNKING",
    fixed_chunks
)


# Recursive Chunking
recursive_chunks = recursive_chunking(text)

print_chunks(
    "RECURSIVE CHUNKING",
    recursive_chunks
)


# Semantic Chunking
semantic_chunks = semantic_chunking(text)

print_chunks(
    "SEMANTIC CHUNKING",
    semantic_chunks
)