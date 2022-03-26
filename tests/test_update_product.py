from lojaintegrada import Api


def test_update_product(mocker):
    mock_make_request = mocker.patch.object(Api, '_make_request')
    product_id = '12345'
    data = {'sku': 'CTU7ZMWHB'}

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    res = api.update_product(product_id, data)

    mock_make_request.assert_called_with(
        'PUT',
        'https://api.awsli.com.br/api/v1/produto/{}'.format(
            product_id
        ),
        data=data
    )

    assert res == mock_make_request.return_value
