import random
# import libtcodpy as libtcod
import time as pyTime

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
        self.agents = []
        self.businesses = []
        self.trade_houses = []

    def update(self, time=1):
        for bus in self.businesses:
            bus.update(time)

        for tra in self.trade_houses:
            tra.update(time)

        for age in self.agents:
            age.update(time)


class Resource:
    def __init__(self, name="", category="", variant="none", quantity=0.0):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.variant = variant
        self.needs = []

    def __str__(self):

        s = self.category + ": " + self.name + " - " + self.variant + " num: "
        s += str(self.quantity)
        if len(self.needs) > 0:
            for res in self.needs:
                s += res[0]
                s += " "
                s += res[1]

        return s


class Goods:
    def __init__(self):
        self.resource = None
        self.quantity = 0.0
        self.raw_cost = 0.0  # how much JUST the base ingredient cost.
        self.total_cost = 0.0  # how much it cost to make ingredients + labour transport etc.
        self.supply_demand = 0.0
        self.bought_for = 0.0
        self.raw_materials = []


class Agent:
    def __init__(self, budget, home_trade_house, job=None):
        self.item_knowledge = {}
        self.needs = {}
        self.budget = budget
        self.home = home_trade_house
        self.job = job

    def update(self, dt):
        if self.job is not None:
            self.job.work_on_job(dt)

        if self.job.is_finished:
            self.job = None

    def purchase(self, request, price):
        # request - the request this agent is purchasing FROM.
        # price - the agreed price that they will purchase for.
        pass


class Job:
    """
    A job can be made up of several tasks.
    eg, for making something.
    1. Acquire correct items
    2. Do intermediary craft step
    3. Craft Item.
    """

    def __init__(self, owner, task, resource):
        self.current_task = task  # TODO: this is just a description atm.
        self.resource = resource
        self.is_finished = False
        self.owner = owner

    def work_on_job(self, time):
        self.current_task.work(time * self.owner.get_productivity())


class Task:
    def __init__(self, producing, requires, work_needed):
        """
        :param producing: What the task will produce? Goal?
        :param requires: What the task will require for resourcing
        :param work_needed: Possibly was the number of "work units"

        """
        self.producing = producing
        self.requires = requires
        self.work_needed = work_needed

    def get_workplace(self):
        if self.requires["workplace"] is not None:
            return self.requires["workplace"]

        return "factory"

    def work(self, work):
        self.work_needed -= work


def check_for_items():
    pass


class Auction(Job):
    def __init__(self, owner, commodity):
        Job.__init__(self, owner, "run auction", commodity)

        self.commodity = commodity
        self.sell_requests = []
        self.buy_requests = []

    def add_request(self, request):
        if request.buy is True:
            self.buy_requests.append(request)
        else:
            self.sell_requests.append(request)

    def get_buyers(self):
        return self.buy_requests

    def get_sellers(self):
        return self.sell_requests


class Request:
    def __init__(self, commodity, buy, requester=None, amount=0, price=5):
        self.commodity = commodity
        self.buy = buy
        self.requester = requester
        self.quantity = commodity.quantity if commodity.quantity != 0 else amount
        # some kind of financial estimates for price go here too.
        self.price = price


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
            auction = Auction(self,
                              Resource(request.commodity.name, request.commodity.category, request.commodity.variant))
            self.auctions_by_commodity[request.commodity.name] = auction
            self.auctions.append(auction)

            # add the request
            self.auctions_by_commodity[request.commodity.name].add_request(request)

    def update(self, time):
        pass

    def resolve_requests(self):
        for commodity in self.auctions_by_commodity.keys():
            buyers = self.auctions_by_commodity[commodity].get_buyers()

            # shuffle the buyers so none get priority.
            random.shuffle(buyers)
            if len(buyers) <= 0:
                continue
            for buyer in buyers:
                price_base = buyer.quantity * buyer.price  # todo: price base, from agent? from current market?

                prices = {}

                # find all the sellers (doesn't matter about order.
                sellers = self.auctions_by_commodity[commodity].get_sellers()
                for seller in sellers:
                    prices[seller.price] = seller
                    # do something to choose which. each
                order = sorted(prices)
                print order
                # fulfil this order with cheapest price.
                for i in range(len(order)):
                    if buyer.quantity < prices[order[i]].quantity:
                        price = (prices[order[i]].price + buyer.price) / 2
                        buyer.requester.purchase(prices[order[i]], price)


class Business:
    def __init__(self):
        self.inactive_agents = []
        self.unowned_jobs = {}
        self.jobs = {}  # key :job type or importance??, value: list of jobs?
        self.active_agents = {}  # key : ??? , value: ??
        self.all_agents = []

        # both of these by commodity.
        self.active_bids = {}
        self.active_sells = {}

    def update(self, dt):
        for job in self.unowned_jobs:
            if len(self.inactive_agents) > 0:
                agent = self.inactive_agents[0]
                self.inactive_agents.remove(0)
                agent.job = job
                job.owner = agent
                self.active_agents[job] = agent


def run_test():
    time = pyTime.time()

    trade_house = TradeHouse()
    agent = Agent(100, trade_house)
    agent_two = Agent(100, trade_house)
    trade_house.agents.append(agent)
    trade_house.agents.append(agent_two)

    business = Business()
    iron = Resource("iron", "refined ore", "metal")
    print iron
    money = Resource("money", "money", "money")
    trade_house.make_request(Request(iron, False, agent, 20))
    trade_house.make_request(Request(iron, False, agent, 15))
    trade_house.make_request(Request(iron, True, agent_two, 5))
    trade_house.make_request(Request(iron, True, agent_two, 5))
    trade_house.make_request(Request(iron, True, agent_two, 5))

    trade_house.resolve_requests()

    running = True
    while running:
        new_time = pyTime.time()
        time_passed = time - new_time
        time += new_time
        dt = 1 / time_passed

        business.update(dt)
        trade_house.update(dt)


run_test()
