from threading import Thread
from time import sleep

class Knight(Thread):
    def __init__(self, name:str, power:int):
        super().__init__()
        self.name = name
        self.power = power

    def run(self):
        print(f'{self.name}, на нас напали!')
        days = 0
        enemies_qty = 100
        while enemies_qty > 0:
            enemies_qty -= self.power
            sleep(1)
            days += 1
            print(f'{self.name} сражается {days} дней..., осталось {enemies_qty} воинов.\n', end='')
        print(f'{self.name}одержал победу спустя {days} дней(дня)!')

first_knight = Knight('Sir Lancelot', 10)
second_knight = Knight("Sir Galahad", 20)

first_knight.start()
second_knight.start()

first_knight.join()
second_knight.join()

print('Все битвы закончились!')