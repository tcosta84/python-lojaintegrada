from lojaintegrada import Api


def test_get_products(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_products()

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/produto/',
        limit=50
    )

    assert order == mock_get_objects.return_value


def test_get_products_with_custom_limit(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_products(limit=20)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/produto/',
        limit=20
    )

    assert order == mock_get_objects.return_value


def test_get_products_with_custom_filters(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_products(situacao_id=4)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/produto/',
        limit=50,
        situacao_id=4
    )

    assert order == mock_get_objects.return_value
