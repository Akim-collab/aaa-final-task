import pytest
from click.testing import CliRunner

from cli import Pizza, deliver, pickup, Margherita, Pepperoni, Hawaiian, show_menu


def test_margherita_creation():
    margherita = Margherita('L')
    assert margherita.size == 'L'
    assert margherita.ingredients == ['tomato sauce', 'mozzarella', 'tomatoes']


def test_pepperoni_creation():
    pepperoni = Pepperoni('XL')
    assert pepperoni.size == 'XL'
    assert pepperoni.ingredients == ['tomato sauce', 'mozzarella', 'pepperoni']


def test_hawaiian_creation():
    hawaiian = Hawaiian('L')
    assert hawaiian.size == 'L'
    assert hawaiian.ingredients == ['tomato sauce', 'mozzarella', 'chicken', 'pineapples']


def test_pizza_equality():
    pizza1 = Pizza('L', ['tomato sauce', 'mozzarella', 'tomatoes'])
    pizza2 = Pizza('L', ['tomato sauce', 'mozzarella', 'tomatoes'])
    assert pizza1 == pizza2


def test_pizza_dict_representation():
    pizza = Pizza('L', ['tomato sauce', 'mozzarella', 'tomatoes'])
    expected_dict = {'size': 'L', 'ingredients': ['tomato sauce',
                                                  'mozzarella', 'tomatoes']}
    assert pizza.dict() == expected_dict


def test_show_menu():
    runner = CliRunner()
    result = runner.invoke(show_menu)
    assert 'Margherita 🍕 : tomato sauce, mozzarella, tomatoes' in result.output
    assert 'Pepperoni 🍕 : tomato sauce, mozzarella, pepperoni' in result.output


def test_delivery():
    pizza = Pizza('XL', ['tomato sauce', 'mozzarella', 'pepperoni'])
    result = deliver(pizza)
    assert 'Pizza delivered' in result
    assert 'XL - tomato sauce, mozzarella, pepperoni' in result


def test_pickup():
    pizza = Pizza('L', ['tomato sauce', 'mozzarella', 'chicken', 'pineapples'])
    result = pickup(pizza)
    assert 'Pizza ready for pickup' in result
    assert 'L - tomato sauce, mozzarella, chicken, pineapples' in result


if __name__ == '__main__':
    pytest.main()
