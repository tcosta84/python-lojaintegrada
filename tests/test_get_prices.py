from lojaintegrada import Api


def test_get_prices(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_prices()

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/produto_preco',
        limit=50
    )

    assert order == mock_get_objects.return_value


def test_get_prices_with_custom_limit(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_prices(limit=20)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/produto_preco',
        limit=20
    )

    assert order == mock_get_objects.return_value
