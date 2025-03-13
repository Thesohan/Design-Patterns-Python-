"""
Design a stock exchange that serves two kind of traders:
 1) institutional traders
 2) individual traders.

Institutional traders, who might have more significant capital and influence,
have an additional feature compared to individual traders - they receive real-time notifications for any buy or sell
orders of stocks they have subscribed to
"""

"""
Framework to solve LLD:

1️⃣ Understand requirements:
2️⃣ Identify entities:
3️⃣ Create class diagram
4️⃣ Apply design patterns:
5️⃣ Implement thread-safe code
6️⃣ Write tests
7️⃣ Discuss scaling


Entities: 

StockExchange:

    ---> has traders
    ---> has stocks

    ---) process_orders
    ---) register_stocks
    ---> register_traders


Trader:
   ---) place_order
   ---) subscribe_stock

   ---> Institutional
      ---) notify

   ---> Individual

Stock:
    has name
    has quantity
    has price
    has subscribers (list of InsitutionalTraders)
    has buy_orders and sell_orders
     ----) update_price
     ----) notify_subscribers
     ----) match_orders
     ---) add_order(order)

Order:
    has order_type
    has trader
    has stock
    has price

OrderType:
    BUY
    SELL

"""
from abc import ABC, abstractmethod
from enum import StrEnum

class TraderType(StrEnum):
    INSTITUTIONAL = "INSTITUTIONAL"
    INDIVIDUAL = "INDIVIDUAL"

class Trader(ABC):
    _registry:dict[TraderType,"Trader"] = {}

    def __init__(self,name:str,trader_id:str)->None:
        self.name:str = name
        self.subscribed_stocks:set[Stock] = set()
        self.trader_id = trader_id

    def subscribe_stock(self,stock)->None:
        self.subscribed_stocks.add(stock)

    @classmethod
    def register(cls,trader_type:TraderType,trader:"Trader")->None:
        if trader_type not in cls._registry:
            cls._registry[trader_type] = trader
        
    @classmethod
    def get_trader_class(cls,trader_type:TraderType)->"Trader":
        if trader_type in cls._registry:
            return cls._registry[trader_type]
        raise ValueError(f"{trader_type} not found")

    @abstractmethod
    def place_order(self,order:"Order")->None:
        pass 

    def __str__(self)->str:
        return f"{self.trader_id}"

class InsitutionalTrader(Trader):

    def place_order(self,order:"Order")->None:
        print(f"Institutional trader placed order :{order}")  

    def notify(self,stock:"Stock"):
        print(f"Notification sent to trader:{self}, price updated for stock: {stock}")

Trader.register(trader_type=TraderType.INSTITUTIONAL,trader=InsitutionalTrader)

class IndividualTrader(Trader):

    def place_order(self,order:"Order")->None:
        print(f"individual trader placed order {order}") 

Trader.register(trader_type=TraderType.INDIVIDUAL, trader=IndividualTrader)


class OrderType(StrEnum):

    SELL = "SELL"
    BUY = "BUY"

class Stock:

    def __init__(self,name:str,quantity:int,price:float,)->None:
        self.name = name 
        self.quantity = quantity
        self.price = price
        self.subscribers:set[InsitutionalTrader] = set()
        self.buy_orders:list[Order] = []
        self.sell_orders:list[Order] = []
        

    def update_price(self):
        new_price = self.price
        if self.buy_orders and self.sell_orders:
            new_price = (self.buy_orders[0].price + self.sell_orders[0].price) / 2
        elif self.buy_orders:
            new_price = self.buy_orders[0].price
        elif self.sell_orders:
            new_price = self.sell_orders[0].price
        if self.price == new_price:
            return  # No orders, keep the same price
        print(f"Stock {self.name} price updated from ${self.price} to ${new_price}")
        self.price = new_price
        self.notify_subscribers() 

    def notify_subscribers(self):
        for subscriber in self.subscribers:
            subscriber.notify(stock=self)

    def match_orders(self):
        pass

    def add_subscriber(self,trader:Trader)->None:
        self.subscribers.add(trader)

    def process_order(self,order:"Order")->None:
        if order.order_type == OrderType.BUY:
            self.buy_orders.append(order)
        elif order.order_type == OrderType.SELL:
            self.sell_orders.append(order)
        self.match_orders()
        self.update_price()

    def __str__(self):
        return f'{self.name}'

class Order:

    def __init__(self,order_type:OrderType,trader:Trader,stock:Stock,price:float,quantity:int):
        self.order_type: OrderType = order_type
        self.trader: Trader = trader
        self.stock: Stock = stock
        self.price: float = price
        self.quantity: int = quantity
    

class StockExchangeName(StrEnum):

    NSE = "NSE"
    BSE = "BSE"


class StockExchange(ABC):
    _registry:dict[StockExchangeName,"StockExchange"] = {}

    def __init__(self):
        self.traders:list[Trader] = []
        self.stocks: dict[str,Stock] = {}

    @classmethod
    def register(cls,stock_exchange_name:StockExchangeName,stock_exchange:"StockExchange")->None:
        if stock_exchange_name not in cls._registry:
            cls._registry[stock_exchange_name] = stock_exchange
        
    @classmethod
    def get_stock_exchange(cls,stock_exchange_name:StockExchangeName)->"StockExchange":
        if stock_exchange_name in cls._registry:
            return cls._registry[stock_exchange_name]
        raise ValueError(f"{stock_exchange_name} not found")
    
    @abstractmethod
    def process_orders(order:Order)->None:
        pass 

    @abstractmethod
    def register_stocks(self,stock:Stock)->None:
        pass 

    @abstractmethod
    def register_traders(self,trader:Trader)->None:
        pass 
    
    def susbsribe_stock_to_trader(self,stock:Stock,trader:Trader)->None:
        if stock.name in self.stocks and trader in self.traders:
            trader.subscribe_stock(stock)
            if isinstance(trader,InsitutionalTrader):
                self.stocks[stock.name].add_subscriber(trader=trader)
            print(f"subscribed stock: {stock} by trader: {trader}")

class NSE(StockExchange):

    def process_orders(self,order:Order)->None:
        if order.stock.name not in self.stocks:
            raise ValueError(f"stock not registered: {order.stock}")
        self.stocks[order.stock.name].process_order(order=order)


    def register_stocks(self,stock:Stock)->None:
        if stock.name not in self.stocks:
            self.stocks[stock.name] = stock
            print(f"stock added in NSE {stock}")

    def register_traders(self,trader:Trader)->None:
        if trader not in self.traders:
            self.traders.append(trader) 
            print(f"trader added in nse {trader}")

StockExchange.register(stock_exchange_name=StockExchangeName.NSE,stock_exchange=NSE)


if __name__ == "__main__":

    stock_exchange = StockExchange.get_stock_exchange(stock_exchange_name=StockExchangeName.NSE)
    apple_stock = Stock(name="App",quantity=100,price=100)
    stock_ex:StockExchange = stock_exchange()
    stock_ex.register_stocks(stock=apple_stock)
    insitutional_trader = Trader.get_trader_class(trader_type=TraderType.INSTITUTIONAL)
    trader:InsitutionalTrader = insitutional_trader(name='Sohan',trader_id='T1')
    stock_ex.register_traders(trader=trader)
    stock_ex.susbsribe_stock_to_trader(stock=apple_stock,trader=trader)

    order = Order(order_type=OrderType.BUY,trader=trader,stock=apple_stock,price=100,quantity=2)
    stock_ex.process_orders(order=order)