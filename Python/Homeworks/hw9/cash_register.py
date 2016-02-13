class Cash_Register:
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
        name = name.lower()
        if name in self.storage:
            self.storage[name][quantity] += quantity
        else:
            self.storage[name] = {'price': price, 'quantity': quantity}
            print('Added {} to storage'.format(name))

    def buy(self, name, quantity):
        """Main buying operation. Adds product to check, updates cash_check"""
        if name in self.storage:
            if self.storage[name]['quantity'] - quantity > 0:
                self.check.append((name, quantity, self.storage[name]['price'], self.storage[name]['price'] * quantity))
                self.check_total += self.storage[name]['price'] * quantity
                print('Added {} of {}'.format(quantity, name))
            else:
                print('Out of stock')
        else:
            print('Sorry, we don\'t sell this')

    def cancel(self, *indices):
        """Removes from check products at positions specified in arguments.
       If called without arguments removes all products"""
        if indices is not None:
            indices = sorted(indices, reverse=True)
            for i in indices:
                self.check_total -= self.check[i][3]
                del self.check[i]
        else:
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
        print("              {}".format(self.check_total))

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
        self.earned_total += self.check_total
        self.check_total = 0
        for i in self.check:
            self.storage[i[0]]['quantity'] -= i[1]
        self.check = []

    def print_storage(self):
        res = ''
        res += '=========Storage==========\n'
        for i in self.storage:
            res += '{}, {} units, {} $ \n'.format(str(i), str(self.storage[i]['quantity']), str(self.storage[i]['price']))
        return res

    def list_items(self):
        for i in self.storage:
            print(i)



c = Cash_Register()
print(c)
