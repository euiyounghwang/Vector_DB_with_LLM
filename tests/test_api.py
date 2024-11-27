
import pytest


@pytest.mark.skip(reason="no way of currently testing this")
def test_skip():
    assert 1 != 1


# @pytest.mark.skip(reason="no way of currently testing this")
def test_api(mock_client):
    response = mock_client.get("/cluster/health?es_url=http://localhost:9201")
    assert response is not None
    assert response.status_code == 200
    assert 'cluster_name' in response.json()

