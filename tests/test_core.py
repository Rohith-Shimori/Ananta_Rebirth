from core.controller import AnantaController


def test_query_returns_response():
    c = AnantaController()
    resp = c.query("hello")
    assert isinstance(resp, dict)
    # Basic contract: response text should be present
    assert "response" in resp
    assert isinstance(resp.get("response"), str)
