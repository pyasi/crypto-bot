from coin import Coin


def create_portfolio(data):
    """"
    """
    portfolio = []
    for coin, ticker, amount, price in data:
        current_coin = Coin(coin, ticker, amount)
        is_new = True
        for old_coin in portfolio:
            if old_coin.display_name == current_coin.display_name:
                old_coin.amount = old_coin.amount + current_coin.amount
                is_new = False
                break
        if is_new:
            portfolio.append(current_coin)

    return portfolio

def is_float(value):
    """

    :param value:
    :return:
    """
    try:
        float(value)
        return True
    except ValueError:
        return False