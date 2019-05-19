import pytest

from lojaintegrada import Api


def test_get_objects(mocker):
    mock_make_request = mocker.patch.object(Api, '_make_request')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    objs = api._get_objects(
        'https://api.awsli.com.br/api/v1/pedido/search'
    )
    page = next(objs)

    mock_make_request.assert_called_with(
        'GET',
        'https://api.awsli.com.br/api/v1/pedido/search',
        params={}
    )

    assert page == mock_make_request.return_value


def test_get_objects_with_params(mocker):
    mock_make_request = mocker.patch.object(Api, '_make_request')

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    objs = api._get_objects(
        'https://api.awsli.com.br/api/v1/pedido/search',
        limit=20
    )
    page = next(objs)

    mock_make_request.assert_called_with(
        'GET',
        'https://api.awsli.com.br/api/v1/pedido/search',
        params={'limit': 20}
    )

    assert page == mock_make_request.return_value


def test_get_objects_multiple_pages(mocker):
    mock_make_request = mocker.patch.object(Api, '_make_request')

    expected_first_data = {
        'meta': {
            'next': '/api/v1/pedido/search/?limit=50&offset=50'
        }
    }

    expected_second_data = {
        'meta': {
            'next': None
        }
    }

    mock_make_request.side_effect = [
        expected_first_data, expected_second_data
    ]

    api = Api(api_key='fake-api-key', app_key='fake-app-key')
    objs = api._get_objects(
        'https://api.awsli.com.br/api/v1/pedido/search'
    )

    first_page = next(objs)
    mock_make_request.assert_called_with(
        'GET',
        'https://api.awsli.com.br/api/v1/pedido/search',
        params={}
    )
    assert first_page == expected_first_data

    second_page = next(objs)
    mock_make_request.assert_called_with(
        'GET',
        'https://api.awsli.com.br/api/v1/pedido/search/?limit=50&offset=50',
        params={}
    )
    assert second_page == expected_second_data

    assert mock_make_request.call_count == 2

    with pytest.raises(StopIteration):
        next(objs)
