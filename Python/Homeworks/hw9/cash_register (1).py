import storage

class Cash_Register:
    def __init__(self):
        self.storage = storage.storage
        self.check = []
        self.earned_total = 0
        self.check_total = 0
        self.locked = {}

    def add_product(self, name, price, quantity):
        """Main buying operation. Adds product to check, updates cash_check"""
        name = name.lower()
        if name in self.storage:
            self.storage[name]['quantity'] += quantity
            self.storage[name]['price'] = price
        else:
            self.storage[name] = {'price': price, 'quantity': quantity}
            print('Added {} to storage'.format(name))

    def buy(self, name, quantity):
        """Main buying operation. Adds product to check, updates cash_check"""
        if name in self.storage:
            if self.storage[name]['quantity'] - quantity >= 0:
                #if item exists in check, just increase quantity
                for i in range(len(self.check)):
                    if self.check[i][0] == name:
                        old_q = self.check[i][1]
                        new_q = old_q + quantity
                        self.check[i] = (name, new_q, self.storage[name]['price'], self.storage[name]['price'] * new_q)
                        self.check_total += self.storage[name]['price'] * quantity
                        self.locked[name] += quantity
                        self.storage[name]['quantity'] -= quantity
                        self.print_check()
                        print('Added {} of {}'.format(quantity, name))
                        return
                self.check.append((name, quantity, self.storage[name]['price'], self.storage[name]['price'] * quantity))
                self.check_total += self.storage[name]['price'] * quantity
                self.locked[name] = quantity
                self.storage[name]['quantity'] -= quantity
                print('Added {} of {}'.format(quantity, name))
                self.print_check()
            else:
                print('Out of stock')
        else:
            print('Sorry, we don\'t sell this. Here is what we offer')
            self.print_storage()
            

    def cancel(self, *indices):
        """Removes from check products at positions specified in arguments.
       If called without arguments removes all products"""
        if len(indices) > 0:
            indices = sorted(indices, reverse=True)
            for i in indices:
                self.check_total -= self.check[i][3]
                self.add_product(self.check[i][0], self.check[i][2], self.check[i][1])
                self.locked[self.check[i][0]] -= self.check[i][1]
                del self.check[i]
        else:
            for i in self.check:
                self.add_product(i[0], i[2], i[1])
                self.locked[i[0]] -= i[1]
            self.check = []
            self.check_total = 0
        self.print_check()

    def change_product_price(self, product, new_price):
        """Changes price of specified product"""
        self.storage[product]['price'] = new_price

    def print_check(self):
        """Prints all items in check to screen"""
        print("=======Check=======")
        for i in self.check:
            print(*i)
        print("====================")
        print("       Total   {}".format(self.check_total))

    def print_storage(self):
        """Prints contents of storage"""
        print('========Storage=======')
        for i in self.storage:
            print('{} {} {}'.format(i, self.storage[i]['price'], self.storage[i]['quantity']))

    def print_total_cash(self):
        """Prints how many cash was made during session on this cash register"""
        print('today {} was made'.format(self.earned_total))

    def purchase(self):
        """To finish buying operation you should call this function.
       Removes products listed in check from storage, updates cash_register_total,
       refreshes the check and cash_check variables"""
        self.earned_total += self.check_total
        self.check_total = 0
        self.check = []
        print('Thank you, have a nice day :)')

    def list_items(self):
        for i in self.storage:
            print(i)


c1 = Cash_Register()
c2 = Cash_Register()

