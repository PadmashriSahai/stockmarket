from datetime import datetime ,timedelta

class StockMarket(object):

    def __init__(self):
        self.stock_data ={
            "TEA": {
                "Type": "Common",
                "Last_Dividend": 0,
                "Fixed_Dividend": None,
                "Par_Value": 100,
            },
            "POP": {
                "Type": "Common",
                "Last_Dividend": 8,
                "Fixed_Dividend": None,
                "Par_Value": 100
            },
            "ALE": {
                "Type": "Common",
                "Last_Dividend": 23,
                "Fixed_Dividend": None,
                "Par_Value": 60
            },
            "GIN": {
                "Type": "Preferred",
                "Last_Dividend": 8,
                "Fixed_Dividend": 2,
                "Par_Value": 100
            },
            "JOE": {
                "Type": "Common",
                "Last_Dividend": 13,
                "Fixed_Dividend": None,
                "Par_Value": 250
            },
        }

        self.trade_data = {}

    def get_symbol(self,symbol):
        """Get the symbol for the stock dictionary
        Input: Symbol """

        stock = self.stock_data.get(symbol,None)
        if stock is None:
            raise ValueError("Stock" + symbol + "doesn't exist")

        return stock


    def calculate_dividend(self,price,symbol):
        """ Calculate dividend
        :param str symbol:
        :param float price:
        :return: """

        if symbol['Type'] == 'Common':
            dividend = (symbol['Last_Dividend'])/price
        else:
            dividend = (symbol['Fixed_Dividend']*symbol['Par_Value'])/price

        return dividend

    def calculate_price_to_earning(self,price,symbol):
        """ Calculate price to earning ratio
        :param str symbol:
        :param float price:
        :return:"""

        dividend = self.calculate_dividend(price,symbol)
        p_e_ratio = price/dividend

        return p_e_ratio

    def add_trades(self,symbol,quantity,buy=False):
        """Record of trades
        :param str symbol:
        :param float quantity:
        :param bool buy:
        :return:"""

        timestamp = datetime.timestamp(datetime.now())
        self.trade_data[int(timestamp)] = {
            "symbol": symbol,
            "action": "buy" if buy else "sell",
            "quantity": quantity,
            "price": self.stock_data[symbol]["Par_Value"]
        }

        print("Saved Trade in Trades dictionary")

    def calculate_volume_weighted_stock_price(self,symbol):
        """Returns volume weighted stock price
        :param str symbol
        :returns"""
        sum_trade = 0
        sum_quantity = 0

        last_5_min = int(datetime.timestamp(datetime.now() - timedelta(minutes=5)))

        for trade in self.trade_data.keys():
            if trade >= last_5_min and self.trade_data[trade]["symbol"] == symbol:
                sum_trade = self.trade_data[trade]["quantity"] * self.trade_data[trade]["price"]
                sum_quantity += self.trade_data[trade]["quantity"]

        sum_quantity = 1 if sum_quantity == 0 else sum_quantity
        vol_weighted_stk_price = sum_trade/ sum_quantity

        return vol_weighted_stk_price

    def get_volume_weighted_stock_price(self):
        """ Returns list of prices for all symbols
        :returns
        """
        sum_trade_all = 0
        sum_quantity_all = 0
        lst_price = []
        for sym in self.stock_data.keys():
            for trade in self.trade_data.keys():
                if self.trade_data[trade]["symbol"] == sym:
                    sum_trade_all += self.trade_data[trade]["quantity"] * self.trade_data[trade]["price"]
                    sum_quantity_all += self.trade_data[trade]["quantity"]
                    sum_quantity_all = 1 if sum_quantity_all == 0 else sum_quantity_all
            if sum_trade_all != 0:
                vol_weighted_stk_price = sum_trade_all/ sum_quantity_all
                lst_price.append(vol_weighted_stk_price)
            sum_trade_all = 0
            sum_quantity_all = 0

        return lst_price

    def calculate_share_index(self):
        """calculate share index of all GBSE shares"""
        from functools import reduce
        price_all = reduce((lambda x,y:x*y), self.get_volume_weighted_stock_price())
        share_index = float(pow(price_all,1/len(self.trade_data.keys())))
        return share_index

def menus():
    """  List of Menus.
    """

    print("1 : Calculate Dividend \n")
    print("2 : Calculate P/E Ratio \n")
    print("3 : Add Trade \n")
    print("4 : List all Trades \n")
    print("5 : Calculate Volume Weighted Stock Price for the past 5 minutes \n")
    print("6 : Calculate GBCE Share Index of all shares \n")
    print("7 - Exit \n")



if __name__ == "__main__":
    wantToContinue = True
    stk_market = StockMarket()

    # Loop through the menu
    while wantToContinue:
        menus()
        option = input("Select option: \n")

        try:
            if option == "1" or option == "2" or option == "3" or option == "5":
                symbol = input("Select a symbol: ")
                dict_symbol = stk_market.get_symbol(symbol)

            if option == "1" or option == "2":
                price = input("Select a price: ")
                price = float(price) if price.isdigit() else 0

            if option == "1":
                print("Dividend : %s\n" % stk_market.calculate_dividend(price=price,symbol=dict_symbol))
            elif option == "2":
                print("P/E Ratio : %s\n" % stk_market.calculate_price_to_earning(price=price,symbol=dict_symbol))
            elif option == "3":
                quantity = input("Select a quantity: ")
                quantity = float(quantity) if quantity.isdigit() else 0
                buy = input("Is to buy? Yes(y) or No(n)").upper()
                buy = True if buy == "Y" else False
                stk_market.add_trades(symbol=symbol, quantity=quantity, buy=buy)
            elif option == "4":
                print("Trade List \n",stk_market.trade_data)
            elif option == "5":
                print("Volume Weighted Stock Price : %s\n" % stk_market.calculate_volume_weighted_stock_price(symbol=symbol))
            elif option == "6":
                trades = stk_market.trade_data.keys()
                if len(trades)>0:
                    print("GBCE Share Index of all shares : %s\n" % stk_market.calculate_share_index())
                else:
                    print("Please choose option 3 to add trades")
            elif option == "7":
                wantToContinue = False
                print("Exit\n")
            else:
                print("Invalid option\n")
        except (KeyError, ValueError, Exception) as error:
            print("Error: %s", error)