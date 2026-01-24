
import pytest
import os
import shutil
from pathlib import Path
import numpy as np
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.lightweight_vector_db import LightweightVectorDB, HNSWIndex

@pytest.fixture
def vector_db():
    # Setup
    db_path = "tests/temp_vector_db"
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    db = LightweightVectorDB(db_path=db_path)
    yield db

    # Teardown
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

def test_store_and_search(vector_db):
    documents = [
        ("Python is a programming language", {"category": "programming"}),
        ("Machine learning is cool", {"category": "ai"}),
        ("Banana is a fruit", {"category": "food"}),
    ]

    for text, meta in documents:
        vector_db.store_and_index(text, meta)

    # Search
    # Note: EmbeddingModel in this codebase is a simulation that returns random vectors seeded by text hash
    # So it should be deterministic.

    results = vector_db.search("programming", k=1)
    assert len(results) >= 1
    # We can't guarantee semantic match with random embeddings, but we check execution

    # To test correctness, we should use HNSWIndex directly with known vectors

def test_hnsw_index_direct():
    index = HNSWIndex(dimension=384)
    vec1 = np.random.randn(384).astype(np.float32)
    vec1 /= np.linalg.norm(vec1)

    vec2 = np.random.randn(384).astype(np.float32)
    vec2 /= np.linalg.norm(vec2)

    index.add(1, vec1)
    index.add(2, vec2)

    # Search for vec1, should be closest to vec1
    results = index.search(vec1, k=1)
    assert results[0][0] == 1
    assert results[0][1] < 0.0001 # Distance should be near 0
