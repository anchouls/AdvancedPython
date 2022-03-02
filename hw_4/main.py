import time
import sys
from codecs import encode
from threading import Thread
from multiprocessing import Process, cpu_count, Queue, Pipe
import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import matplotlib.pyplot as plt


def fibonacci(n: int):
    if n == 1:
        return [1]
    answer = [1, 1]
    for _ in range(n - 2):
        answer.append(answer[-1] + answer[-2])
    return answer


def integrate(f, a, b, *, n_iter=100000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_thread(file, f, a, b, *, n_jobs, n_iter=100000):
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        step = (b - a) / n_jobs
        threads = []
        for i in range(n_jobs):
            file.write(f'In the interval [{a + i * step}, {a + (i + 1) * step} ] ' +
                       f'starts at: {time.time() - start_time} \n')
            threads.append(executor.submit(integrate, f, a + i * step, a + (i + 1) * step, n_iter=n_iter // n_jobs))
        return sum(t.result() for t in as_completed(threads))


def integrate_process(file, f, a, b, *, n_jobs, n_iter=100000):
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=n_jobs) as executor:
        step = (b - a) / n_jobs
        processes = []
        for i in range(n_jobs):
            file.write(f'In the interval [{a + i * step}, {a + (i + 1) * step} ] ' +
                       f'starts at: {time.time() - start_time} \n')
            processes.append(executor.submit(integrate, f, a + i * step, a + (i + 1) * step, n_iter=n_iter // n_jobs))
        return sum(p.result() for p in as_completed(processes))


def process_A(queue, conn_b):
    while True:
        s = queue.get()
        conn_b.send(s.lower())
        if s == '':
            return
        time.sleep(5)


def process_B(conn_a, conn_main):
    while True:
        s = conn_a.recv()
        conn_main.send(encode(s, 'rot_13'))
        if s == '':
            return


def take_and_print(conn_ans, f):
    while True:
        s = conn_ans.recv()
        if s == '':
            return
        f.write(f'{s}, end time: {time.time()}\n')


def easy():
    start_time = time.time()
    threads = [Thread(target=fibonacci, args=(int(1e5), )) for _ in range(10)]
    for tread in threads:
        tread.start()
    for tread in threads:
        tread.join()
    duration_threads = time.time() - start_time
    start_time = time.time()
    processes = [Process(target=fibonacci, args=(int(1e5), )) for _ in range(10)]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    duration_processes = time.time() - start_time
    with open('artifacts/easy.txt', 'w') as f:
        f.write(f'threads: {duration_threads}\n')
        f.write(f'processes: {duration_processes}\n')


def medium():
    cpu_num = cpu_count()
    time_threads = []
    time_process = []
    with open('artifacts/medium.txt', 'w') as f:
        f.write('Threads:\n')
        for n_jobs in range(1, cpu_num * 2 + 1):
            start_time = time.time()
            integrate_thread(f, math.cos, 0, math.pi / 2, n_jobs=n_jobs)
            time_threads.append(time.time() - start_time)
        f.write('Processes:\n')
        for n_jobs in range(1, cpu_num * 2 + 1):
            start_time = time.time()
            integrate_process(f, math.cos, 0, math.pi / 2, n_jobs=n_jobs)
            time_process.append(time.time() - start_time)
        plt.plot(list(range(1, cpu_num * 2 + 1)), time_threads)
        plt.savefig('artifacts/medium_compare_threads.png')
        plt.cla()
        plt.plot(list(range(1, cpu_num * 2 + 1)), time_process)
        plt.savefig('artifacts/medium_compare_processes.png')


def hard():
    queue = Queue()
    conn_a, conn_b = Pipe()
    conn_ans, conn_main = Pipe()
    A = Process(target=process_A, args=(queue, conn_b, ))
    B = Process(target=process_B, args=(conn_a, conn_main, ))
    A.start()
    B.start()
    s = None
    with open('artifacts/hard.txt', 'w') as f:
        output = Thread(target=take_and_print, args=(conn_ans, f, ))
        output.start()
        while s != '':
            s = input().strip()
            if s != '':
                f.write(f'{s}, start time: {time.time()}\n')
            queue.put(s)
        A.join()
        B.join()
        output.join()


def main():
    if sys.argv[1] == 'easy':
        easy()
    elif sys.argv[1] == 'medium':
        medium()
    elif sys.argv[1] == 'hard':
        hard()


if __name__ == "__main__":
    main()
