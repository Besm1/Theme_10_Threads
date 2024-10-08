from threading import Thread, Lock
from random import randint
from time import sleep

class Bank:
    def __init__(self, balance):
        self.balance = balance
        self.lock = Lock()

    def deposit(self):
        for i in range(100):
            income = randint(50, 500)
            locked_by_funds_shortage = self.lock.locked()
            if not locked_by_funds_shortage:
                # print(f'@1({i}): Закрываем замок для фиксации прихода')
                self.lock.acquire()
            self.balance += income
            print(f'@1({i}): Пополнение {income}. Баланс {self.balance}')
            if  locked_by_funds_shortage:
                if self.balance > 500:
                    # print(f'@1({i}): Приход зафиксирован, средств стало много! Открываем замок')
                    self.lock.release()
                else:
                    # print(f'@1({i}): Приход зафиксирован, но средств мало. Замок НЕ открываем.')
                    pass
            else:
                # print(f'@1({i}): Приход зафиксирован, открываем замок')
                self.lock.release()
            sleep(0.01)     # Транзакция занимает время...

    def take(self):
        for i in range(100):
            expense = randint(50,500)
            print(f'@2({i}): Запрос на {expense}.')
            if self.balance >= expense:
                # print(f'@2({i}): Закрываем замок...')
                self.lock.acquire()
                # print(f'@2({i}): ...замок закрыт!')
                self.balance -= expense
                print(f'@2({i}): Снятие {expense}. Баланс {self.balance}. Открываем замок.')
                self.lock.release()
            else:
                print(f'@2({i}): Запрос отклонён, недостаточно средств. Пытаемся закрыть замок')
                self.lock.acquire()
                # print(f'@2({i}): Замок закрыт!')

if __name__ == '__main__':
    bank = Bank(0)
    t1 = Thread(target=bank.deposit)
    t2 = Thread(target=bank.take)

    t1.start()
    t2.start()

    t2.join()
    print('@2(--): Поток два стрельбу закончил!')
    t1.join()

    print(f'\nИтоговый баланс: {bank.balance}')