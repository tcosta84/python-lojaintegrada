import logging
from unittest import mock
import pytest
from requests import Session
from requests.exceptions import HTTPError, RequestException

from lojaintegrada import LIApi, ApiError


logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO,
    datefmt='%I:%M:%S'
)


def test_build_session(mocker):
    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')

    assert isinstance(api.session, Session)
    assert api.session.headers['Content-type'] == 'application/json'
    assert api.session.headers['Authorization'] == 'chave_api fake-api-key aplicacao fake-app-key'


def test_get_brand(mocker):
    mock_make_request = mocker.patch.object(LIApi, '_make_request')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    brand = api.get_brand(12345)

    mock_make_request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/marca/12345'
    )

    assert brand == mock_make_request.return_value


def test_get_category(mocker):
    mock_make_request = mocker.patch.object(LIApi, '_make_request')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    category = api.get_category(12345)

    mock_make_request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/categoria/12345'
    )

    assert category == mock_make_request.return_value


def test_get_customer(mocker):
    mock_make_request = mocker.patch.object(LIApi, '_make_request')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    customer = api.get_customer(12345)

    mock_make_request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/cliente/12345'
    )

    assert customer == mock_make_request.return_value


def test_get_order(mocker):
    mock_make_request = mocker.patch.object(LIApi, '_make_request')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_order(12345)

    mock_make_request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/pedido/12345'
    )

    assert order == mock_make_request.return_value


def test_get_orders(mocker):
    mock_get_objects = mocker.patch.object(LIApi, '_get_objects')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_orders()

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/pedido/search',
        limit=50
    )

    assert order == mock_get_objects.return_value


def test_get_orders_with_custom_limit(mocker):
    mock_get_objects = mocker.patch.object(LIApi, '_get_objects')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_orders(limit=20)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/pedido/search',
        limit=20
    )

    assert order == mock_get_objects.return_value


def test_get_orders_with_custom_filters(mocker):
    mock_get_objects = mocker.patch.object(LIApi, '_get_objects')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_orders(situacao_id=4)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/pedido/search',
        limit=50,
        situacao_id=4
    )

    assert order == mock_get_objects.return_value


def test_get_price(mocker):
    mock_make_request = mocker.patch.object(LIApi, '_make_request')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_price(12345)

    mock_make_request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/produto_preco/12345'
    )

    assert res == mock_make_request.return_value


def test_get_product(mocker):
    mock_make_request = mocker.patch.object(LIApi, '_make_request')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    product = api.get_product(12345)

    mock_make_request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/produto/12345'
    )

    assert product == mock_make_request.return_value


def test_get_product_images(mocker):
    mock_make_request = mocker.patch.object(LIApi, '_make_request')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_product_images(12345)

    mock_make_request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/produto_imagem/?produto=12345'
    )

    assert res == mock_make_request.return_value


def test_get_products(mocker):
    mock_get_objects = mocker.patch.object(LIApi, '_get_objects')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_products()

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/produto/',
        limit=50
    )

    assert order == mock_get_objects.return_value


def test_get_products_with_custom_limit(mocker):
    mock_get_objects = mocker.patch.object(LIApi, '_get_objects')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_products(limit=20)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/produto/',
        limit=20
    )

    assert order == mock_get_objects.return_value


def test_get_products_with_custom_filters(mocker):
    mock_get_objects = mocker.patch.object(LIApi, '_get_objects')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    order = api.get_products(situacao_id=4)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/produto/',
        limit=50,
        situacao_id=4
    )

    assert order == mock_get_objects.return_value


def test_get_status_history(mocker):
    mock_get_objects = mocker.patch.object(LIApi, '_get_objects')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_status_history()

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/situacao_historico/search',
        limit=50,
        numero=None
    )

    assert res == mock_get_objects.return_value


def test_get_status_history_with_custom_limit(mocker):
    mock_get_objects = mocker.patch.object(LIApi, '_get_objects')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_status_history(limit=20)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/situacao_historico/search',
        limit=20,
        numero=None
    )

    assert res == mock_get_objects.return_value


def test_get_status_history_with_order_id(mocker):
    mock_get_objects = mocker.patch.object(LIApi, '_get_objects')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_status_history(order_id=12345)

    mock_get_objects.assert_called_with(
        'https://api.awsli.com.br/api/v1/situacao_historico/search',
        limit=50,
        numero=12345
    )

    assert res == mock_get_objects.return_value


def test_get_stock(mocker):
    mock_make_request = mocker.patch.object(LIApi, '_make_request')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_stock(12345)

    mock_make_request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/produto_estoque/12345'
    )

    assert res == mock_make_request.return_value


def test_update_order_status(mocker):
    mock_make_request = mocker.patch.object(LIApi, '_make_request')
    expected_data = {'codigo': 'pedido_pago'}

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.update_order_status(12345, 'pedido_pago')

    mock_make_request.assert_called_with(
        'PUT',
        'https://api.awsli.com.br/api/v1/situacao/pedido/12345',
        data=expected_data
    )

    assert res == mock_make_request.return_value


def test_get_paid_orders(mocker):
    mock_get_orders = mocker.patch.object(LIApi, 'get_orders')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_paid_orders()

    mock_get_orders.assert_called_with(
        limit=50,
        situacao_id=4
    )

    assert res == mock_get_orders.return_value


def test_get_paid_orders_with_custom_limit(mocker):
    mock_get_orders = mocker.patch.object(LIApi, 'get_orders')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_paid_orders(limit=20)

    mock_get_orders.assert_called_with(
        limit=20,
        situacao_id=4
    )

    assert res == mock_get_orders.return_value


def test_get_paid_orders_with_custom_filters(mocker):
    mock_get_orders = mocker.patch.object(LIApi, 'get_orders')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_paid_orders(cliente_id=12345)

    mock_get_orders.assert_called_with(
        limit=50,
        situacao_id=4,
        cliente_id=12345
    )

    assert res == mock_get_orders.return_value


def test_get_in_separation_orders(mocker):
    mock_get_orders = mocker.patch.object(LIApi, 'get_orders')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_in_separation_orders()

    mock_get_orders.assert_called_with(
        limit=50,
        situacao_id=15
    )

    assert res == mock_get_orders.return_value


def test_get_in_separation_orders_with_custom_limit(mocker):
    mock_get_orders = mocker.patch.object(LIApi, 'get_orders')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_in_separation_orders(limit=20)

    mock_get_orders.assert_called_with(
        limit=20,
        situacao_id=15
    )

    assert res == mock_get_orders.return_value


def test_get_in_separation_orders_with_custom_filters(mocker):
    mock_get_orders = mocker.patch.object(LIApi, 'get_orders')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.get_in_separation_orders(cliente_id=12345)

    mock_get_orders.assert_called_with(
        limit=50,
        situacao_id=15,
        cliente_id=12345
    )

    assert res == mock_get_orders.return_value


def test_mark_order_as_delivered(mocker):
    mock_update_order_status = mocker.patch.object(
        LIApi, 'update_order_status'
    )

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.mark_order_as_delivered(12345)

    mock_update_order_status.assert_called_with(12345, 'pedido_entregue')

    assert res == mock_update_order_status.return_value


def test_mark_order_as_in_separation(mocker):
    mock_update_order_status = mocker.patch.object(
        LIApi, 'update_order_status'
    )

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api.mark_order_as_in_separation(12345)

    mock_update_order_status.assert_called_with(12345, 'pedido_em_separacao')

    assert res == mock_update_order_status.return_value


def test_get_objects(mocker):
    mock_make_request = mocker.patch.object(LIApi, '_make_request')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
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
    mock_make_request = mocker.patch.object(LIApi, '_make_request')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
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
    mock_make_request = mocker.patch.object(LIApi, '_make_request')

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

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
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


def test_make_request(mocker):
    mock_session = mocker.patch('lojaintegrada.api.requests.Session')

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    res = api._make_request(
        'GET', 'https://api.awsli.com.br/api/v1/pedido/search'
    )

    mock_session.return_value.request.assert_called_with(
        'GET',
        'https://api.awsli.com.br/api/v1/pedido/search',
        json=None, params=None
    )

    mock_session.return_value.request.return_value.raise_for_status.assert_called_with()

    assert res == mock_session.return_value.request.return_value.json.return_value


def test_make_request_should_raise_general_exception_for_HTTPError(mocker):
    mock_session = mocker.patch('lojaintegrada.api.requests.Session')

    mock_session.return_value.request.side_effect = HTTPError(
        response=mock.Mock(
            status_code=400
        )
    )

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')

    with pytest.raises(ApiError):
        res = api._make_request(
            'GET', 'https://api.awsli.com.br/api/v1/pedido/search'
        )


def test_make_request_should_raise_general_exception_for_RequestException(mocker):
    mock_session = mocker.patch('lojaintegrada.api.requests.Session')

    mock_request = mock.Mock()
    mock_session.return_value.request.side_effect = RequestException(
        request=mock_request
    )

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')

    with pytest.raises(ApiError) as e:
        res = api._make_request(
            'GET', 'https://api.awsli.com.br/api/v1/pedido/search'
        )

    assert e.value.request == mock_request


def test_make_request_should_retry_when_rate_limit_reached(mocker):
    mock_sleep = mocker.patch('lojaintegrada.api.time.sleep')
    mock_session = mocker.patch('lojaintegrada.api.requests.Session')

    mock_session.return_value.request.side_effect = [
        HTTPError(
            response=mock.Mock(
                status_code=429
            )
        ),
        mock.DEFAULT
    ]

    api = LIApi(api_key='fake-api-key', app_key='fake-app-key')
    api._make_request('GET', 'https://api.awsli.com.br/api/v1/pedido/search')

    mock_sleep.assert_called_with(10)
    assert mock_session.return_value.request.call_count == 2
    mock_session.return_value.request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/pedido/search',
        json=None, params=None
    )


def test_make_request_should_retry_with_custom_dealy_when_rate_limit_reached(mocker):
    mock_sleep = mocker.patch('lojaintegrada.api.time.sleep')
    mock_session = mocker.patch('lojaintegrada.api.requests.Session')

    mock_session.return_value.request.side_effect = [
        HTTPError(
            response=mock.Mock(
                status_code=429
            )
        ),
        mock.DEFAULT
    ]

    api = LIApi(
        api_key='fake-api-key',
        app_key='fake-app-key',
        rate_limit_retry_delay=5
    )
    api._make_request('GET', 'https://api.awsli.com.br/api/v1/pedido/search')

    mock_sleep.assert_called_with(5)
    assert mock_session.return_value.request.call_count == 2
    mock_session.return_value.request.assert_called_with(
        'GET', 'https://api.awsli.com.br/api/v1/pedido/search',
        json=None, params=None
    )
