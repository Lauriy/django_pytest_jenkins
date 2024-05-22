import pytest


@pytest.mark.django_db
@pytest.mark.parametrize("test_id", range(1, 501))
def test_do_stuff(client, stuff_instance, test_id):
    response = client.get(f"/do-stuff/{stuff_instance.id}")
    assert response.status_code == 200
    assert response.json()['updatedAt']
