"""
Tests for search.py: Typesense full-text search over photoblog.
"""
import pytest
from tests.conftest import _mock_typesense_client


def _ts_results(hits):
    return {"hits": hits, "found": len(hits)}


def _hit(id, headline, body):
    return {
        "document": {"id": id, "headline": headline, "body": body},
        "highlights": [{"snippet": body[:50]}],
    }


def test_search_no_query_returns_200(client):
    _mock_typesense_client.collections.__getitem__.return_value \
        .documents.search.return_value = _ts_results([])
    rv = client.get("/search")
    assert rv.status_code == 200


def test_search_with_query_returns_200(client):
    _mock_typesense_client.collections.__getitem__.return_value \
        .documents.search.return_value = _ts_results([
            _hit(1, "Photo of cats", "We have many cats at home"),
        ])
    rv = client.get("/search?q=cats")
    assert rv.status_code == 200


def test_search_passes_query_to_typesense(client):
    """Verify the Typesense client is called with the user's query string."""
    mock_search = (
        _mock_typesense_client.collections.__getitem__.return_value
        .documents.search
    )
    mock_search.return_value = _ts_results([])
    client.get("/search?q=hello+world")
    call_args = mock_search.call_args
    assert call_args is not None
    search_params = call_args[0][0]
    assert search_params["q"] == "hello world"


def test_search_empty_results(client):
    _mock_typesense_client.collections.__getitem__.return_value \
        .documents.search.return_value = _ts_results([])
    rv = client.get("/search?q=xyzzy")
    assert rv.status_code == 200
