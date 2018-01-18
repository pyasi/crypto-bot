from app.coin import Coin


# TODO evaluate need for logic. Currently accounts for multiple records of same coin for same users
def create_portfolio(data):
    """
    Create a portfolio using the users DB data

    :param data: Row data of user's coins from the DB
    :return: list of Coins and the amount the user has
    """
    portfolio = []
    for coin, ticker, amount in data:
        current_coin = Coin(coin, ticker, amount)
        if current_coin.amount > 0:
            portfolio.append(current_coin)
    return portfolio


def is_float(value):
    """
    Determine if a value is a float

    :return: True of False
    """
    try:
        float(value)
        return True
    except ValueError:
        return False
