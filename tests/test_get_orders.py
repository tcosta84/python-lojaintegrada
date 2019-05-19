from lojaintegrada import Api


def test_get_order(mocker):
    mock_make_request = mocker.patch.object(Api, '_make_request')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_order(12345)

    mock_make_request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/pedido/12345'
    )

    assert order == mock_make_request.return_value


def test_get_orders(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_orders()

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/pedido/search',
        limit=50
    )

    assert order == mock_get_objects.return_value


def test_get_orders_with_custom_limit(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_orders(limit=20)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/pedido/search',
        limit=20
    )

    assert order == mock_get_objects.return_value


def test_get_orders_with_custom_filters(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_orders(situacao_id=4)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/pedido/search',
        limit=50,
        situacao_id=4
    )

    assert order == mock_get_objects.return_value
