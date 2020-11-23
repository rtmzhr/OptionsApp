import pandas as pd
from bs4 import BeautifulSoup
import requests

average_growth_per_year = 0.2


class OptionsManager:
    def __init__(self, answers=None):
        self.answers = answers
        self.options_list = []
        self.total_cost = 0

    def calc_total_cost(self):
        for option in self.options_list:
            self.total_cost += option.get_cost()
        return self.total_cost

    def calc_future_total_profit(self, future_strike):
        overall_profit = 0
        for option in self.options_list:
            overall_profit += option.get_profit(future_strike)
        return overall_profit

    def simulate_profit(self, strike_after_option_period):
        return self.calc_future_total_profit(strike_after_option_period) - self.total_cost


class OptionTrainingData:
    def __init__(self):
        self.data = pd.read_csv("Project/Data/4.csv")
        self.strikes_array = self.data["Strikes"].array.astype('float')
        self.strikes_array = self.strikes_array.reshape((1, len(self.data.index)))[0]
        self.current_stock_price = 290

    def set_options_date(self, date_index):
        return

    def get_option_index(self, strike, offset=0):
        length = len(self.strikes_array)
        strike -= strike % 5
        return offset + binary_search(self.strikes_array, 0, length, strike)

    def get_option_price(self, strike, offset=0):
        return self.data.iloc[self.get_option_index(strike, offset), :].astype('float')


class OptionData:
    def __init__(self):
        self.html = None
        self.soup = None
        self.option_date_value = None
        self.data = None
        self.strikes_array = None

        self.url = 'https://finance.yahoo.com/quote/FB/options?p=FB&straddle=true'
        self.init_page(self.url)
        self.current_stock_price = float(
            self.soup.find('span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text)
        self.dates_tags = [entry for entry in
                           self.soup.find('select', {'class': 'Fz(s) H(25px) Bd Bdc($seperatorColor)'})]

    def init_page(self, url):
        self.html = requests.get(url).text
        self.soup = BeautifulSoup(self.html, "html.parser")

    def get_dates_texts(self):
        dates = [month.text for month in self.dates_tags]
        return dates

    def set_options_date(self, date_text):
        dates = [month.text for month in self.dates_tags]
        self.option_date_value = self.dates_tags[dates.index(date_text)]['value']
        self.get_options_data()
        return dates.index(date_text)

    def get_options_data(self):
        url = 'https://finance.yahoo.com/quote/FB/options?p=FB&straddle=true&date={}'.format(self.option_date_value)
        self.init_page(url)
        calls = pd.DataFrame([entry.text for entry in self.soup.find_all('td', {
            'class': 'data-col0 Ta(end) Pstart(10px) call-in-the-money_Bgc($hoverBgColor)'
                     ' Bdstartw(8px) Bdstarts(s) Bdstartc(t) call-in-the-money_Bdstartc($linkColor)'})])
        strikes = [entry.text for entry in self.soup.find_all(
                'td', {'class': "data-col5 Ta(c) Px(10px) BdX Bdc($seperatorColor)"})]
        puts = pd.DataFrame([entry.text for entry in self.soup.find_all('td', {
            'class': "data-col6 Ta(end) Pstart(10px) put-in-the-money_Bgc($hoverBgColor)"})])
        data = pd.concat([calls, pd.DataFrame(strikes), puts], axis=1)
        data.columns = ["Calls", "Strikes", "Puts"]
        data = data.replace('-', 0)
        self.data = data
        self.strikes_array = [float(i) for i in strikes]

    def get_option_index(self, strike, offset=0):
        length = len(self.strikes_array)
        strike -= strike % 5
        return offset + binary_search(self.strikes_array, 0, length, strike)

    def get_option_price(self, strike, offset=0):
        return self.data.iloc[self.get_option_index(strike, offset), :].astype('float')


def binary_search(arr, low, high, x):
    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

            # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

            # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        return -1


option_data = OptionData()
current_stock_price = option_data.current_stock_price
