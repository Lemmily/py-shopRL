__author__ = 'Emily'


# class TradeHouse():
#     """
#         Home of the auctions and trade within a city.
#     """
#     def __init__(self):
#         #key - time of day auction held at.. value - Auction object
#         self.auctions = {}
#
#         #goods being sold on market
#         self.sells = {}
#
#         #goods wanting to be purchased on market.
#         self.bids = {}
#
#     def update(self, hour):
#         """
#             updated hourly
#         """
#         if self.auctions[hour] is not None:
#             self.do_auction(self.auctions[hour])
#
#     def do_auction(self, auction):
#         pass
#
#
# class Auction():
#     """
#         Stored information about an auction
#         Owner - who's to be paid once completed
#         For_sale - object/cargo/resource/etc that is for sale.
#     """
#     def __init__(self, for_sale, owner):
#         self.for_sale = for_sale
#         self.owner = owner
#
#         self.bidders = []
