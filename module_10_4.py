import queue
import random
import time
from threading import Thread


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        time.sleep(random.randint(3,10))

class Cafe:
    def __init__(self, *tables):
        self.tables = list(tables)
        self.queue = queue.Queue()

    def guest_arrival(self, *guests:Guest):
        for g_ in guests:
            try:
                table = [t_ for t_ in self.tables if t_.guest is None][0]
            except IndexError:
                table = None
            if table is None:
                self.queue.put(g_)
                print(f'{g_.name} в очереди')
            else:
                table.guest = g_
                g_.start()
                print(f'{g_.name} сел(-а) за столик {table.number}')

    def discuss_guests(self):
        while (len([t_ for t_ in self.tables if t_.guest is not None]) > 0) or not self.queue.empty():
            for table in [t_ for t_ in self.tables if t_.guest is not None]:
                if table is not None and not table.guest.is_alive():
                    print(f'{table.guest.name} поел(-а) и ушёл(-ла).')
                    print(f'Столик {table.number} свободен.')
                    table.guest = None
                if not self.queue.empty():
                    try:
                        table = [t_ for t_ in self.tables if t_.guest is None][0]
                    except IndexError:
                        table = None
                    if table is not None:
                        guest = self.queue.get()
                        table.guest = guest
                        print(f'{guest.name} вышел(-ла) из очереди и сел(-а) за столик {table.number}')
                        guest.start()

if __name__ == '__main__':
    # Создание столов
    tables = [Table(number) for number in range(1, 6)]
    # Имена гостей
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
        ]
    # Создание гостей
    guests = [Guest(name) for name in guests_names]
    # Заполнение кафе столами
    cafe = Cafe(*tables)
    # Приём гостей
    cafe.guest_arrival(*guests)
    # Обслуживание гостей
    cafe.discuss_guests()



