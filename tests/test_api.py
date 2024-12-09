
import pytest
from injector import doc, ES_HOST, es_version

@pytest.mark.skip(reason="no way of currently testing this")
def test_skip():
    assert 1 != 1


def test_api(mock_client):
    response = mock_client.get("/")
    assert response is not None
    assert response.status_code == 200
    assert response.json() == {
        "message": "Vector & LLM Search API"
        }
   


# @pytest.mark.skip(reason="no way of currently testing this")
def test_es_api(mock_client):
    print(doc)
    print(es_version)
    response = mock_client.get("/cluster/health?es_url={}".format(ES_HOST))
    assert response is not None
    assert response.status_code == 200
    assert 'cluster_name' in response.json()

