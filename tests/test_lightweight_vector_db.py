
import pytest
import numpy as np
import shutil
from pathlib import Path
from memory.lightweight_vector_db import LightweightVectorDB, HNSWIndex

@pytest.fixture
def vector_db(tmp_path):
    # Use a temporary directory for the DB
    db_path = tmp_path / "vector_db"
    db = LightweightVectorDB(str(db_path))
    return db

def test_add_and_search(vector_db):
    # Create some dummy vectors
    # LightweightVectorDB uses EmbeddingModel which generates random vectors for now
    # but store_and_index calls embedder.encode

    id1 = vector_db.store_and_index("apple", {"type": "fruit"})
    id2 = vector_db.store_and_index("banana", {"type": "fruit"})
    id3 = vector_db.store_and_index("car", {"type": "vehicle"})

    assert id1 == 0
    assert id2 == 1
    assert id3 == 2

    # Search
    # Since embeddings are random in the current implementation of EmbeddingModel,
    # we can't guarantee semantic search results.
    # But we can verify that search returns results in correct format

    results = vector_db.search("fruit", k=2)
    assert len(results) <= 2
    for res in results:
        assert "id" in res
        assert "distance" in res
        assert "metadata" in res
        assert "data" in res # from cache or disk

def test_hnsw_index_vectorization():
    # Test the HNSWIndex directly to verify vectorization logic
    index = HNSWIndex(dimension=4)

    # Add vectors
    v1 = np.array([1, 0, 0, 0], dtype=np.float32)
    v2 = np.array([0, 1, 0, 0], dtype=np.float32)
    v3 = np.array([0, 0, 1, 0], dtype=np.float32)

    index.add(0, v1)
    index.add(1, v2)
    index.add(2, v3)

    assert index.dirty == True

    # Search with v1 (should match v1 perfectly, dist=0)
    query = np.array([1, 0, 0, 0], dtype=np.float32)
    results = index.search(query, k=3)

    assert index.dirty == False # Should be clean after search
    assert len(results) == 3

    # Top result should be idx 0
    assert results[0][0] == 0
    assert results[0][1] < 1e-6 # Distance should be near 0

    # Check v2 (orthogonal, dist should be 1.0)
    # results order might vary for v2 and v3 as both have dist 1.0
    found_v2 = False
    for idx, dist in results:
        if idx == 1:
            found_v2 = True
            assert abs(dist - 1.0) < 1e-6
    assert found_v2

def test_rebuild_index():
    index = HNSWIndex(dimension=4)
    v1 = np.array([1, 0, 0, 0], dtype=np.float32)
    index.add(0, v1)

    assert index.dirty
    index._rebuild_index()
    assert not index.dirty
    assert len(index.ids) == 1
    assert index.vectors_matrix.shape == (1, 4)

    # Add another
    v2 = np.array([0, 1, 0, 0], dtype=np.float32)
    index.add(1, v2)
    assert index.dirty

    # Search should trigger rebuild
    index.search(v1, k=1)
    assert not index.dirty
    assert len(index.ids) == 2
    assert index.vectors_matrix.shape == (2, 4)
