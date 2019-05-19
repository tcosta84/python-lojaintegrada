# Loja Integrada API Wrapper

A simple Python API Wrapper for e-commerce platform [Loja Integrada](https://lojaintegrada.com.br/).

## Install

Via Pip:

``` bash
$ pip install lojaintegradapy
```

Via GIT:

``` bash
$ pip install git+https://git@github.com/tcosta84/python-lojaintegrada.git
```

## Usage

``` python

from lojaintegrada import Api

api = Api('your-api-key', 'your-app-key')

for page in api.get_orders():
	for obj in page['objects']:
		order_id = obj['numero']
		order_data = api.get_order(order_id)
```

By default, an automatic retry will be done every time a rate limit error (throttling) occurs (http status code "429").

## Testing

``` bash
$ make test
```

## Security

If you discover any security related issues, please email thiagodacosta@gmail.com instead of using the issue tracker.

## Credits

- [Thiago Costa][link-author]
- [All Contributors][link-contributors]

## License

The MIT License (MIT). Please see [License File](LICENSE) for more information.

[link-author]: https://twitter.com/goathi
[link-contributors]: ../../contributors