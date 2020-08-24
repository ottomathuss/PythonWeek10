"""
    Author:          Hartmut Mathussek
    Date Created:    07/26/2020
    Functionality:
                     This file contains the investor, stock and bond classes
                     including methods to calculate earnings/loss and yearly yield.
                     
"""

from datetime import datetime

# Create Investor class
class Investor:
    def __init__(self, investor_id, investor_name, investor_address, investor_phone, investor_stocks = [], investor_bonds = []):
        self.investor_id = investor_id
        self.investor_name = investor_name
        self.investor_address = investor_address
        self.investor_phone = investor_phone
        self.investor_stocks = investor_stocks
        self.investor_bonds = investor_bonds

    # Getters and setters
    def get_investor_id(self):
        return self.investor_id

    def set_investor_id(self, investor_id):
        self.investor_id = investor_id

    def get_investor_name(self):
        return self.investor_name

    def set_investor_name(self, investor_name):
        self.investor_name = investor_name

    def get_investor_address(self):
        return self.investor_address

    def set_investor_address(self, investor_address):
        self.investor_address = investor_address

    def get_investor_phone(self):
        return self.investor_phone

    def set_investor_phone(self, investor_phone):
        self.investor_phone = investor_phone

    def get_investor_stocks(self):
        return self.investor_stocks

    def set_investor_stocks(self, investor_stocks):
        self.investor_stocks = investor_stocks

    def get_investor_bonds(self):
        return self.investor_bonds

    def set_investor_bonds(self, investor_bonds):
        self.investor_bonds = investor_bonds

# Create Stock class
class Stock:
    def __init__(self, purchase_id, symbol, number_shares, purchase_price, current_value, purchase_date):
        self.symbol = symbol
        self.purchase_id = purchase_id
        self.number_shares = number_shares
        self.purchase_price = purchase_price
        self.current_value = current_value
        self.purchase_date = purchase_date

    def print_symbol(self):
        symbol = self.symbol
        return symbol

    # Getters and setters
    def get_purchase_id(self):
        return self.purchase_id

    def set_purchase_id(self, purchase_id):
        self.purchase_id = purchase_id

    def get_symbol(self):
        return self.symbol

    def set_symbol(self, symbol):
        self.symbol = symbol

    def get_number_shares(self):
        return self.number_shares

    def set_number_shares(self, number_shares):
        self.number_shares = number_shares

    def get_purchase_price(self):
        return self.purchase_price

    def set_purchase_price(self, purchase_price):
        self.purchase_price = purchase_price

    def get_current_value(self):
        return self.current_value

    def set_current_price(self, current_value):
        self.current_value = current_value

    def get_purchase_date(self):
        return self.purchase_date

    def set_purchased_date(self, purchase_date):
        self.purchase_date = purchase_date

    def f_earnings(self):
        # Function that calculates the earnings/losses for each stock
        try:
            earnings = (self.current_value - self.purchase_price) * self.number_shares
            return ("$"+format(earnings, ",.2f"))
        except:
            return ("Error!")

    def f_yearly_yield(self):
        # Function that calculates the average percentage yield/loss per stock per year
        try:
            today = datetime.today()
            datemask = "%m/%d/%Y"
            purch_date = datetime.strptime(self.purchase_date, datemask)
            days_owned_year = (today - purch_date).days
            result = (self.current_value - self.purchase_price) / self.purchase_price / days_owned_year * 365 * 100
            return (format(result, ",.2f"))
        except:
            return("Error!")
        
# Create Bond class to inherit from the Stock class
class Bond(Stock):
    def __init__(self, purchase_id, symbol, number_shares, purchase_price, current_value, purchase_date, coupon, yield_percent):
        super().__init__(purchase_id, symbol, number_shares, purchase_price, current_value, purchase_date)
        self.coupon = coupon
        self.yield_percent = yield_percent

    def get_yield_percent(self):
        return self.yield_percent

    def get_coupon(self):
        return self.coupon

    def set_yield_percent(self, yield_percent):
        self.yield_percent = yield_percent

    def set_coupon(self, coupon):
        self.coupon = coupon
        

