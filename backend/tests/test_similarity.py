"""Unit tests for the cosine similarity used by semantic search / RAG."""
from app.ai.retrieval.similarity import cosine_similarity


def test_identical_vectors_have_similarity_one():
    assert cosine_similarity([1, 0, 0], [1, 0, 0]) == 1.0


def test_orthogonal_vectors_have_similarity_zero():
    assert cosine_similarity([1, 0], [0, 1]) == 0.0


def test_opposite_vectors_have_similarity_negative_one():
    assert cosine_similarity([1, 0], [-1, 0]) == -1.0


def test_empty_vectors_return_zero_instead_of_erroring():
    assert cosine_similarity([], []) == 0.0


def test_mismatched_length_returns_zero_instead_of_erroring():
    assert cosine_similarity([1, 2], [1, 2, 3]) == 0.0
