import datetime
from datetime import _days_before_year


class cash_register:
    def __init__(self):
        self.storage = {}
        self.check = []
        self.earned_total = 0
        self.check_total = 0
        self.add('eggs', 0.30, 1000)
        self.add('bread', 0.75, 180)
        self.add('milk', 3.5, 90)

    def add(self, name, price, quantity):
        """Main buying operation. Adds product to check, updates cash_check"""
        if name in self.storage:
            self.storage[name][quantity] += quantity
        else:
            self.storage[name] = {'price': price, 'quantity': quantity}

    def buy(self, name, quantity, price):
        """Main buying operation. Adds product to check, updates cash_check"""
        if self.storage[name][quantity] - quantity > 0:
            self.check.append((name, quantity, price, price * quantity))
        else:
            print('Out of stock')

    def cancel(self, *indices):
        """Removes from check products at positions specified in arguments.
       If called without arguments removes all products"""
        if len(indices) > 0:
            indices = sorted(indices, reverse=True)
            for i in indices:
                del self.check[i]
        else:
            self.check = []

    def change_product_price(self, product, new_price):
        """Changes price of specified product"""
        self.storage[product]['price'] = new_price

    def print_check(self):
        """Prints all items in check to screen"""
        print("=======Check=======")
        for i in self.check:
            print(*i)

    def print_storage(self):
        """Prints contents of storage"""
        for i in self.storage:
            print(*i)

    def print_total_cash(self):
        """Prints how many cash was made during session on this cash register"""
        print('today {} was made'.format(self.earned_total))

    def purchase(self):
        """To finish buying operation you should call this function.
       Removes products listed in check from storage, updates cash_register_total,
       refreshes the check and cash_check variables"""

