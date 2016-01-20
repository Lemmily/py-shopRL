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

class Economy:
    def __init__(self):
        self.businesses = []
        self.trade_houses = []

    def update(self, time=1):
        for bus in self.businesses:
            bus.update(time)

        for tra in self.trade_houses:
            tra.update(time)


class Resource:
    def __init__(self, name="", category="", type="none", quantity=0.0):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.type = type
        self.needs = []


class Goods:
    def __init__(self):
        self.resource = None
        self.quantity = 0.0
        self.raw_cost = 0.0  # how much JUST the base ingredient cost.
        self.total_cost = 0.0  # how much it cost to make ingredients + labour transport etc.
        self.supplyDemand = 0.0
        self.bought_for = 0.0
        self.raw_materials = []


class Agent:
    def __init__(self, budget, home_trade_house):
        self.item_knowledge = {}
        self.needs = {}
        self.budget = budget
        self.home = home_trade_house


class Auction:
    def __init__(self, commodity):
        self.commodity = commodity
        self.sell_requests = []
        self.buy_requests = []

    def add_request(self, request):
        if request.buy is True:
            self.buy_requests.append(request)
        else:
            self.sell_requests.append(request)


class Request:
    def __init__(self, commodity, buy, requester=None, amount=0):
        self.commodity = commodity
        self.buy = buy
        self.requester = requester
        self.quantity = commodity.quantity if commodity.quantity != 0 else amount
        # some kind of financial estimates for price go here too.


class TradeHouse:
    def __init__(self):
        self.agents = []
        self.jobs = {}
        # self.agents_with_jobs = {}
        self.auctions_by_commodity = {}
        self.auctions = []

    def make_request(self, request):
        if request.commodity.name in self.auctions_by_commodity:
            self.auctions_by_commodity[request.commodity.name].add_request(request)
        else:
            # make new auction
            auction = Auction(Resource(request.commodity.name, request.commodity.category, request.commodity.type))
            self.auctions_by_commodity[request.commodity.name] = auction
            self.auctions.append(auction)

            # add the request
            self.auctions_by_commodity[request.commodity.name].add_request(request)

    def update(self, time):
        pass

    def resolve_requests(self):
        pass


class Business:
    def __init__(self):
        self.agents = []
        self.jobs = {}
        self.active_agents = {}

        # both of these by commodity.
        self.active_bids = {}
        self.active_sells = {}


trade_house = TradeHouse()
agent = Agent(100, trade_house)
trade_house.agents.append(agent)


business = Business()
iron = Resource("iron", "refined ore", "metal")
trade_house.make_request(Request(iron, False, agent, 20))
trade_house.make_request(Request(iron, True, 5))
trade_house.make_request(Request(iron, True, 5))
trade_house.make_request(Request(iron, True, 5))


trade_house.resolve_requests();