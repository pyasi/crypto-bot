# class Portfolio(object):
#
#     def __init__(self):
#         self.user = user
#         self.coins
#
#     def create_portfolio_from_coins(self, coin_data):
#     """
#
#     """
#     portfolio = []
#     for coin, ticker, amount, price in coin_data:
#         current_coin = Coin(coin, ticker, amount)
#         is_new = True
#         for old_coin in portfolio:
#             if old_coin.display_name == current_coin.display_name:
#                 old_coin.amount = old_coin.amount + current_coin.amount
#                 is_new = False
#                 break
#         if is_new:
#             portfolio.append(current_coin)
#
#     return portfolio