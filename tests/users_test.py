def test_get_user_from_id(client, h_principal):
    response = client.get(
        '/principal/user',
        headers=h_principal
    )

    assert response.status_code == 200

    # data = response.json['data']
    # for assignment in data:
    #     assert assignment['teacher_id'] == 1