from lojaintegrada import Api


def test_get_brands(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    pages = api.get_brands()

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/marca',
        limit=50
    )

    assert pages == mock_get_objects.return_value


def test_get_brands_with_custom_limit(mocker):
    mock_get_objects = mocker.patch.object(Api, '_get_objects')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    pages = api.get_brands(limit=20)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/marca',
        limit=20
    )

    assert pages == mock_get_objects.return_value
