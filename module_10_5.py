import datetime
import multiprocessing


def read_info(name):
    all_data = []
    with open(file=name, mode='r') as file:
        line = file.readline()
        while line:
            all_data.append(line)
            line = file.readline()

def time_dec(proc):
    def kostyl(*args, **kwargs):
        start = datetime.datetime.now()
        result = proc(*args, **kwargs)
        time = (datetime.datetime.now() - start)
        print(time)
        return result
    return kostyl

@time_dec
def classic(*files):
    for f_ in files[0]:
        read_info(f_)

@time_dec
def multy(*files):
    with multiprocessing.Pool(processes=4) as pool:
        pool.map(read_info, files[0] )

@time_dec
def main():
    files = [f'./files_10_5/file {i}.txt' for i in range(1,5)]
    classic(files)
    multy(files)

if __name__ == '__main__':
    main()

