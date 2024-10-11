import datetime
import multiprocessing


def read_info(name):
    all_data = []
    with open(file=name, mode='r') as file:
        line = file.readline()
        while line:
            all_data.append(line)
            line = file.readline()


if __name__ == '__main__':
    files = [f'./files_10_5/file {i}.txt' for i in range(1,5)]

    start = datetime.datetime.now()
    for f_ in files:
        read_info(f_)
    finish = datetime.datetime.now()
    print(finish - start)

    with multiprocessing.Pool(processes=4) as pool:
        start = datetime.datetime.now()
        pool.map(read_info, files )
    finish = datetime.datetime.now()
    print(finish - start)
