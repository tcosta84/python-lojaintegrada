from lojaintegrada import Api


def test_get_customer(mocker):
    mock_make_request = mocker.patch.object(Api, '_make_request')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    customer = api.get_customer(12345)

    mock_make_request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/cliente/12345'
    )

    assert customer == mock_make_request.return_value
