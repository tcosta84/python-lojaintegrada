from lojaintegrada import Api


def test_get_status_history(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_status_history()

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/situacao_historico/search',
        limit=50,
        numero=None
    )

    assert res == mock_get_objects.return_value


def test_get_status_history_with_custom_limit(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_status_history(limit=20)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/situacao_historico/search',
        limit=20,
        numero=None
    )

    assert res == mock_get_objects.return_value


def test_get_status_history_with_order_id(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_status_history(order_id=12345)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/situacao_historico/search',
        limit=50,
        numero=12345
    )

    assert res == mock_get_objects.return_value
