import click
from typing import List
from functools import wraps
import time


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
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            click.echo(f'{func.__name__} — '
                       f'{template.format(end_time - start_time)}')
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

    def __eq__(self, other: object) -> bool:
        """
        Compares two Pizza objects for equality.

        Parameters:
        - other (Pizza): Another Pizza object to compare.

        Returns:
        - bool: True if the pizzas are equal, False otherwise.
        """
        if not isinstance(other, Pizza):
            return NotImplemented
        eq = self.size == other.size and self.ingredients == other.ingredients
        return eq


class Menu:
    pizzas = {
        'Margherita': Pizza('L', ['tomato sauce', 'mozzarella', 'tomatoes']),
        'Pepperoni': Pizza('XL', ['tomato sauce', 'mozzarella', 'pepperoni']),
        'Hawaiian': Pizza('L', ['tomato sauce', 'mozzarella',
                                'chicken', 'pineapples'])
    }


@click.group()
def cli():
    pass


@cli.command()
@click.argument('pizza', nargs=1)
@click.option('--delivery', default=False, is_flag=True,
              help='Flag to indicate pizza delivery')
def order(pizza: str, delivery: bool):
    """
    Prepare and deliver pizza.

    Parameters:
    - pizza (str): Name of the pizza to be ordered.
    - delivery (bool): Flag indicating whether
    the pizza should be delivered.

    Returns:
    - None
    """
    try:
        pizza_obj = Menu.pizzas.get(pizza)
        # Adjust time based on pizza size
        time_taken = 2 if pizza_obj.size == 'L' else 4
        click.echo(f'Приготовили за {time_taken}с!')
        if delivery:
            click.echo('🛵 Доставили за 1с!')
    finally:
        click.echo('Invalid pizza type. Please choose from the menu.')


@cli.command()
def menu():
    """
    Display available pizza menu.

    Returns:
    - None
    """
    for name, pizza in Menu.pizzas.items():
        click.echo(f'- {name} 🍕 : {", ".join(pizza.ingredients)}')


@log('🛵 Доставили за {}с!')
def delivery(pizza):
    """
    Delivers a pizza.

    Parameters:
    - pizza (Pizza): Pizza object to be delivered.

    Returns:
    - str: A message indicating that the pizza has been delivered.
    """
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
    return string


if __name__ == '__main__':
    cli()
