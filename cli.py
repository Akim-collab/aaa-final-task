import click
from typing import List
import random
from functools import wraps


def log(template: str = '{}'):
    """
    Decorator that logs the name of the decorated function
    and the time taken to execute it.

    Parameters:
    - template (str, optional): A string template for
    the log message. Default is '{}',
      which represents the time taken in seconds.

    Returns:
    - function: The decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper function that calculates the time
            taken to execute the decorated function
            and logs the result.

            Parameters:
            - args: Positional arguments passed to the decorated function.
            - kwargs: Keyword arguments passed to the decorated function.

            Returns:
            - Any: The result of the decorated function.
            """
            result = func(*args, **kwargs)
            time_taken = random.randint(2, 8)
            click.echo(f'{func.__name__} — '
                       f'{template.format(time_taken)}')
            return result

        return wrapper

    return decorator


class Pizza:
    def __init__(self, size: str, ingredients: List[str]):
        """
        Represents a Pizza object with a specific size and list of ingredients.

        Parameters:
        - size (str): Size of the pizza (e.g., 'L' or 'XL').
        - ingredients (List[str]): List of ingredients on the pizza.

        Returns:
        - Pizza: A Pizza object.
        """
        self.size = size
        self.ingredients = ingredients

    def dict(self) -> dict:
        """
        Returns the pizza details as a dictionary.

        Returns:
        - dict: A dictionary containing 'size' and 'ingredients'.
        """
        return {'size': self.size, 'ingredients': self.ingredients}

    def __eq__(self, other: 'Pizza') -> bool:
        """
        Compares two Pizza objects for equality.

        Parameters:
        - other (Pizza): Another Pizza object to compare.

        Returns:
        - bool: True if the pizzas are equal, False otherwise.
        """
        return self.size == other.size and self.ingredients == other.ingredients


class Margherita(Pizza):
    def __init__(self, size: str):
        """
        Represents a Margherita pizza.

        Parameters:
        - size (str): Size of the pizza (e.g., 'L' or 'XL').

        Returns:
        - Margherita: A Margherita pizza object.
        """
        super().__init__(size, ['tomato sauce', 'mozzarella', 'tomatoes'])


class Pepperoni(Pizza):
    def __init__(self, size: str):
        """
        Represents a Pepperoni pizza.

        Parameters:
        - size (str): Size of the pizza (e.g., 'L' or 'XL').

        Returns:
        - Pepperoni: A Pepperoni pizza object.
        """
        super().__init__(size, ['tomato sauce', 'mozzarella', 'pepperoni'])


class Hawaiian(Pizza):
    def __init__(self, size: str):
        """
        Represents a Hawaiian pizza.

        Parameters:
        - size (str): Size of the pizza (e.g., 'L' or 'XL').

        Returns:
        - Hawaiian: A Hawaiian pizza object.
        """
        super().__init__(size, ['tomato sauce', 'mozzarella', 'chicken', 'pineapples'])


class Menu:
    pizzas = {
        'margherita': Margherita,
        'pepperoni': Pepperoni,
        'hawaiian': Hawaiian
    }


@click.group()
def cli():
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True, help='Flag to indicate pizza delivery')
@click.argument('pizza_name', nargs=1)
@click.argument('size', nargs=1, type=click.Choice(['L', 'XL']))
def order(pizza_name: str, size: str, delivery: bool):
    """
    Prepare and deliver/pickup pizza.

    Parameters:
    - pizza_name (str): Name of the pizza to be ordered.
    - size (str): Size of the pizza (L or XL).
    - delivery (bool): Flag indicating whether the pizza should be delivered.

    Returns:
    - None
    """
    pizza_name_lower = pizza_name.lower()
    if pizza_name_lower in Menu.pizzas:
        pizza_class = Menu.pizzas[pizza_name_lower]
        pizza = pizza_class(size)
        bake(pizza)
        if delivery:
            deliver(pizza)
        else:
            pickup(pizza)
    else:
        click.echo('Invalid pizza type. Please choose from the menu.')


@cli.command()
def show_menu():
    """
    Display available pizza menu.

    Returns:
    - None
    """
    for name, pizza_class in Menu.pizzas.items():
        pizza = pizza_class('L')
        click.echo(f'- {name.capitalize()} 🍕 : {", ".join(pizza.ingredients)}')


@log('Приготовили за {}с!')
def bake(pizza: Pizza):
    """Bakes pizza"""
    pass


@log('🛵 Доставили за {}с!')
def deliver(pizza):
    """
    Delivers a pizza.

    Parameters:
    - pizza (Pizza): Pizza object to be delivered.

    Returns:
    - str: A message indicating that the pizza has been delivered.
    """
    print(f'Pizza delivered: {pizza.size} - {", ".join(pizza.ingredients)}')
    return f'Pizza delivered: {pizza.size} - {", ".join(pizza.ingredients)}'


@log('🏠 Забрали за {}с!')
def pickup(pizza):
    """
    Allows for self-pickup of a pizza.

    Parameters:
    - pizza (Pizza): Pizza object for self-pickup.

    Returns:
    - str: A message indicating that the pizza is ready for pickup.
    """
    string = f'Pizza ready for pickup: {pizza.size} - ' \
             f'{", ".join(pizza.ingredients)}'
    print(string)
    return string


if __name__ == '__main__':
    cli()
