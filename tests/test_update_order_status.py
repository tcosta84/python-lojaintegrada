from lojaintegrada import Api


def test_update_order_status(mocker):
    mock_make_request = mocker.patch.object(Api, '_make_request')
    expected_data = {'codigo': 'pedido_pago'}

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    res = api.update_order_status(12345, 'pedido_pago')

    mock_make_request.assert_called_with(
        'PUT',
        'https://api.awsli.com.br/api/v1/situacao/pedido/12345',
        data=expected_data
    )

    assert res == mock_make_request.return_value
