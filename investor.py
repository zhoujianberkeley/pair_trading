class invest:

    ts_cost = 35/1000
    long = None

    def __init__(self, balance):
        self.balance = balance
        self.porfo = {}

    def buy(self, id, price):
        self.porfo[id] = self.balance/(price*(1 + invest.ts_cost))
        self.balance = 0

    def sell(self, id, price):

        self.balance += self.porfo.__getitem__(id)*price* \
                       (1 - invest.ts_cost)
        self.porfo.__delitem__(id)

    def short(self, id, price):
        self.porfo[id] = self.balance/ price
        self.balance += self.porfo[id] * price* \
                       (1 - invest.ts_cost)

    def clo_short(self, id, price):
        self.balance -= self.porfo.__getitem__(id) * price * \
                        (1 + invest.ts_cost)
        self.porfo.__delitem__(id)

