from threading import Thread, Lock
from random import randint
from time import sleep

class Bank:
    def __init__(self, balance):
        self.balance = balance
        self.change_lock = Lock()
        self.take_lock = Lock()

    def deposit(self):
        for i in range(100):
            income = randint(50, 500)
            print(f'@1({i}): Запрос на пополнение {income}. Пытаемся закрыть замок change_lock...')
            self.change_lock.acquire()
            print(f'@1({i}): ... замок change_lock закрыт')
            self.balance += income
            print(f'@1({i}): Пополнение {income}. Баланс {self.balance}')
            sleep(0.001)     # Транзакция занимает время...
            print(f'@1({i}): Приход зафиксирован, открываем замок change_lock')
            self.change_lock.release()
            if self.take_lock.locked() and self.balance > 500:
                self.take_lock.release()
                print(f'@1({i}): Средств стало достаточно, открываем замок take_lock')
            # sleep(0.001)     # А это не время на транзакцию, а время между транзакциями... Непонятно, зачем.

    def take(self):
        for i in range(100):
            expense = randint(50,500)
            print(f'    @2({i}): Запрос на снятие {expense}.')
            if self.take_lock.locked() and not t1.is_alive():  # Если снятие залочено, а поступлений больше не будет
                self.take_lock.release()
            if self.balance >= expense:
                print(f'    @2({i}): Закрываем замок take_lock. Если не получилось - значит заблокировано по недостаче...')
                self.take_lock.acquire(timeout=0.000000001)
                # if not t1.is_alive():
                print(f'    @2({i}): ...замок take_lock закрыт!')
                print(f'    @2({i}): Закрываем замок change_lock. Если не получилось - значит сейчас происходит пополнение...')
                self.change_lock.acquire()
                print(f'    @2({i}): ...замок change_lock закрыт!')
                self.balance -= expense
                print(f'    @2({i}): Снятие {expense}. Баланс {self.balance}. Открываем замок change_lock.')
                self.change_lock.release()
                print(f'    @2({i}): Открываем замок замок take_lock!')
                if self.take_lock.locked():
                    self.take_lock.release()
            else:
                print(f'    @2({i}): Запрос отклонён, недостаточно средств (баланс {self.balance}).', end='')
                if t1.is_alive():
                    print(f'    @2({i}): Закрываем замок take_lock')
                    self.take_lock.acquire()
                    print(f'    @2({i}): замок take_lock закрыт!')
                else:
                    print(f'    @2({i}): Счёт арестован за недостачу!')
                    break

if __name__ == '__main__':
    bank = Bank(0)
    t1 = Thread(target=bank.deposit)
    t2 = Thread(target=bank.take)

    t1.start()
    t2.start()

    t2.join()
    print('    @2(--): Поток два стрельбу закончил!')
    t1.join()

    print(f'\nИтоговый баланс: {bank.balance}')