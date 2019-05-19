from lojaintegrada import Api


def test_mark_order_as_delivered(mocker):
    mock_update_order_status = mocker.patch.object(Api, 'update_order_status')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    res = api.mark_order_as_delivered(12345)

    mock_update_order_status.assert_called_with(12345, 'pedido_entregue')

    assert res == mock_update_order_status.return_value
