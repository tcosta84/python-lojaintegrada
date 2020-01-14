from lojaintegrada import Api


def test_update_order_status(mocker):
    mock_make_request = mocker.patch.object(Api, '_make_request')
    shipping_id = '12345'
    tracking_code = 'PU13898292932BR'
    expected_data = {'objeto': tracking_code}

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    res = api.update_tracking_code(shipping_id, tracking_code)

    mock_make_request.assert_called_with(
        'PUT',
        'https://api.awsli.com.br/api/v1/pedido_envio/{}'.format(
            shipping_id
        ),
        data=expected_data
    )

    assert res == mock_make_request.return_value
