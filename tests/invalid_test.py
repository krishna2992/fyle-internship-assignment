def test_index(client, h_teacher_1):
    response = client.get('/')
    assert response.status_code == 200

    assert response.json['status'] == 'ready'


def test_get_assignments_invalid_1(client, h_teacher_1):
    response = client.get(
        '/invalid/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 404

def test_get_assignments_unauthorised_1(client, h_teacher_1):
    response = client.get(
        '/invalid/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 404

    