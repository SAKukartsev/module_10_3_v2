import threading
from random import randint
from time import sleep


class Bank:
    lock = threading.Lock()
    take_work = 0
    deposit_work = 0

    def __init__(self, balance):
        self.balance = balance

    def deposit(self):
        for i in range(10):
            rand_deposit = randint(50, 500)
            while self.deposit_work == 1 and self.take_work == 0:
                pass
            if self.balance <= 500:
                with self.lock:
                    self.balance += rand_deposit
                    print(f'Пополнение: {rand_deposit}. Баланс: {self.balance}')
                    self.deposit_work = 1
                    sleep(0.001)
            else:
                while self.balance > 500 and self.take_work == 0:
                    with self.lock:
                        self.deposit_work = 1
                    pass
        self.deposit_work = 1

    def take(self):
        for i in range(10):
            rand_take = randint(50, 500)
            while self.deposit_work == 0:
                pass
            with self.lock:
                print(f'Запрос на {rand_take}')
            if rand_take <= self.balance:
                with self.lock:
                    self.balance -= rand_take
                    print(f'Снятие: {rand_take}. Баланс: {self.balance}')
                    self.deposit_work = 0
                    sleep(0.001)
            else:
                with self.lock:
                    print('Запрос отклонён, недостаточно средств')
                    self.deposit_work = 0
                    sleep(0.001)

        self.take_work = 1


bk = Bank(0)

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
