from options.Models.managers import option_data


class Option:
    def __init__(self, strike_index, amount):
        self.amount = amount
        self.strike = option_data.strikes_array[strike_index]

    def get_cost(self):
        return self.price * self.amount

    def get_profit_after_costs(self, future_strike):
        return self.get_profit(future_strike) - self.get_cost()

    def __str__(self):
        x = 1
        if self.option_execution == "buy":
            x = -1
        return f'{self.option_execution} {self.option_type} option | strike = {self.strike}'


class PutOption(Option):
    def __init__(self, strike_index, amount):
        self.option_type = "put"
        Option.__init__(self, strike_index, amount)
        self.price = option_data.get_option_price(self.strike)["Puts"]


class BuyPutOption(PutOption):
    def __init__(self, strike_index, amount=1):
        self.option_execution = "buy"
        PutOption.__init__(self, strike_index, amount)

    def get_profit(self, future_strike):
        profit = 0
        if future_strike < self.strike:
            profit = (self.strike - future_strike) * self.amount
        return profit


class SellPutOption(PutOption):
    def __init__(self, strike_index, amount=1):
        self.option_execution = "sell"
        PutOption.__init__(self, strike_index, amount)

    def get_profit(self, future_strike):
        profit = 0
        if future_strike < self.strike:
            profit = (future_strike - self.strike) * self.amount
        return profit

    def get_cost(self):
        return -1 * Option.get_cost(self)


class CallOption(Option):
    def __init__(self, strike_index, amount):
        self.option_type = "call"
        Option.__init__(self, strike_index, amount)
        self.price = option_data.get_option_price(self.strike)["Calls"]



class BuyCallOption(CallOption):
    def __init__(self,  strike_index, amount=1):
        self.option_execution = "buy"
        CallOption.__init__(self, strike_index, amount)

    def get_profit(self, future_strike):
        profit = 0
        if future_strike > self.strike:
            profit = (future_strike - self.strike) * self.amount
        return profit


class SellCallOption(CallOption):
    def __init__(self, strike_index, amount=1):
        self.option_execution = "sell"
        CallOption.__init__(self, strike_index, amount)

    def get_profit(self, future_strike):
        profit = 0
        if future_strike > self.strike:
            profit = (self.strike - future_strike) * self.amount
        return profit

    def get_cost(self):
        return -1 * Option.get_cost(self)

