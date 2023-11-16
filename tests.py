import pytest

from cli import Pizza, delivery, pickup


def test_pizza_creation():
    pizza = Pizza('L', ['tomato sauce', 'mozzarella', 'tomatoes'])
    assert pizza.size == 'L'
    assert pizza.ingredients == ['tomato sauce', 'mozzarella', 'tomatoes']


def test_pizza_equality():
    pizza1 = Pizza('L', ['tomato sauce', 'mozzarella', 'tomatoes'])
    pizza2 = Pizza('L', ['tomato sauce', 'mozzarella', 'tomatoes'])
    assert pizza1 == pizza2


def test_pizza_dict_representation():
    pizza = Pizza('L', ['tomato sauce', 'mozzarella', 'tomatoes'])
    expected_dict = {'size': 'L', 'ingredients': ['tomato sauce',
                                                  'mozzarella', 'tomatoes']}
    assert pizza.dict() == expected_dict


def test_delivery():
    pizza = Pizza('XL', ['tomato sauce', 'mozzarella', 'pepperoni'])
    result = delivery(pizza)
    assert 'Pizza delivered' in result
    assert 'XL - tomato sauce, mozzarella, pepperoni' in result


def test_pickup():
    pizza = Pizza('L', ['tomato sauce', 'mozzarella', 'chicken', 'pineapples'])
    result = pickup(pizza)
    assert 'Pizza ready for pickup' in result
    assert 'L - tomato sauce, mozzarella, chicken, pineapples' in result


if __name__ == '__main__':
    pytest.main()
