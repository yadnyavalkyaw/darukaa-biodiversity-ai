"""Tests for the retrievable knowledge layer and citation indexing."""

from darukaa.knowledge import CITATIONS_REGISTRY, KnowledgeRetriever


def test_citations_registry_integrity():
    assert len(CITATIONS_REGISTRY) >= 10
    for key, citation in CITATIONS_REGISTRY.items():
        assert citation.id == key
        assert len(citation.title) > 5
        assert len(citation.authors) > 2
        assert citation.year >= 1990
        assert citation.doi_or_url.startswith("http")


def test_retriever_query_relevance():
    retriever = KnowledgeRetriever()
    results = retriever.query("soil organic carbon water holding capacity fao", top_k=3)
    assert len(results) > 0

    top_res = results[0]
    assert top_res.relevance_score > 0.3
    assert top_res.citation is not None
    assert top_res.citation.id in CITATIONS_REGISTRY


def test_retriever_domain_filtering():
    retriever = KnowledgeRetriever()
    soil_results = retriever.query("carbon nitrogen diversity", domain="soil", top_k=5)
    for res in soil_results:
        assert res.domain == "soil"
