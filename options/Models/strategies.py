from options.Models.managers import option_data, current_stock_price
from options.Models.options import BuyCallOption, BuyPutOption, SellCallOption, SellPutOption


class Strategy:

    def __init__(self, option_manager):
        self.option_manager = option_manager
        option_period = option_manager.answers["Option Period"]
        likelihood = option_manager.answers["Estimation Likelihood"]
        increase_prob = option_manager.answers["Stock Increase Likelihood"]
        decrease_prob = option_manager.answers["Stock Decrease Likelihood"]
        risk_appetite = option_manager.answers["Risk Appetite"]
        estimated_price_by_user = option_manager.answers['Price Estimation']

        self.estimated_price = likelihood * estimated_price_by_user + (1 - likelihood) * current_stock_price ** (option_period / 12)
        self.strike_offset = 3 + 10 - risk_appetite + option_period
        self.strike_offset = [increase_prob * self.strike_offset, decrease_prob * self.strike_offset]

        self.lower_bound_index = option_data.get_option_index(estimated_price_by_user, -1 * int(self.strike_offset[1]))
        self.upper_bound_index = option_data.get_option_index(estimated_price_by_user, int(self.strike_offset[0]))

    def buy_call(self, strike_index):
        self.option_manager.options_list.append(BuyCallOption(strike_index))

    def sell_call(self, strike_index):
        self.option_manager.options_list.append(SellCallOption(strike_index))

    def buy_put(self, strike_index):
        self.option_manager.options_list.append(BuyPutOption(strike_index))

    def sell_put(self, strike_index):
        self.option_manager.options_list.append(SellPutOption(strike_index))


def get_option_choice(question):
    opt = input(question)
    while opt.isdigit() and 1 <= int(opt) <= 4:
        opt = input("Invalid Input! {}".format(question))
    return int(opt)

    # class Manually(Strategy):
    #     choose_opt_type_question = Question("option type", "Please Choose which open do you want\n"
    #                                                        "1 for Buy-Put    2 for Sell-Put\n"
    #                                                        "3 for Buy-Call   4 for Sell-Call\n", 1, 4, validate_int_range)
    #     choose_opt_strike_question = Question("option strike", "what's the option's strike?\n"
    #                                                            " Please write an Integer\n", 100, 400, validate_int_range)
    #
    #     def __init__(self, option_manager):
    #         Strategy.__init__(self, option_manager)
    #         self.strategy_question_manager = QuestionManger([self.choose_opt_type_question,
    #                                                          self.choose_opt_strike_question])
    #
    # def execute(self):
    #     self.strategy_question_manager.start()
    #     if self.strategy_question_manager.answers["option type"] == 1:
    #         self.buy_put(self.strategy_question_manager.answers["option strike"])
    #     elif self.strategy_question_manager.answers["option type"] == 2:
    #         self.sell_put(self.strategy_question_manager.answers["option strike"])
    #     elif self.strategy_question_manager.answers["option type"] == 3:
    #         self.sell_call(self.strategy_question_manager.answers["option strike"])
    #     else:
    #         self.buy_call(self.strategy_question_manager.answers["option strike"])
    #     self.strategy_question_manager.reset_answers()
    #     if input("Do you want to choose another option?\n Press Y/N\n") == "Y":
    #         self.execute()


class IronCodorStrategy(Strategy):
    def __init__(self, option_manager):
        Strategy.__init__(self, option_manager)

    def execute(self):
        self.buy_put(self.lower_bound_index - 1)
        self.sell_put(self.lower_bound_index)
        self.sell_call(self.upper_bound_index)
        self.buy_call(self.upper_bound_index + 1)
        self.option_manager.calc_total_cost()
