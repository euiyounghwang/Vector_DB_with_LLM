import time
import multiprocessing
from multiprocessing import Process, Queue

def square(number):
    return number ** 2


def square_numbers(numbers, result_queue):
    squared_numbers = [x ** 2 for x in numbers]
    result_queue.put(squared_numbers)

def cube_numbers(numbers, result_queue):
    cubed_numbers = [x ** 3 for x in numbers]
    result_queue.put(cubed_numbers)


def work1():
    numbers = range(1000000)
    
    # Single-core processing
    start_time = time.time()
    results_single = []
    for number in numbers:
        result = square(number)
        # results_single.append(result)
    end_time = time.time()
    single_time = end_time - start_time
    
    # Multi-core processing
    start_time = time.time()
    pool = multiprocessing.Pool()
    results_multi = pool.map(square, numbers)
    pool.close()
    pool.join()
    end_time = time.time()
    multi_time = end_time - start_time
    
    # Print results
    print(f"Single core time: {single_time:.4f} seconds")
    print(f"Multi-core time: {multi_time:.4f} seconds")
    print(f"Speedup: {single_time/multi_time:.2f}x")


def work2():
    data = [1, 2, 3, 4, 5]
    result_queue = Queue()

    # 각 프로세스에 다른 함수 할당
    process1 = Process(target=square_numbers, args=(data, result_queue))
    process2 = Process(target=cube_numbers, args=(data, result_queue))

    # 프로세스 시작
    process1.start()
    process2.start()

    # 프로세스 종료 대기
    process1.join()
    process2.join()

    # 결과를 큐에서 수집
    results = [result_queue.get(), result_queue.get()]

    print("Squared Results:", results[0])
    print("Cubed Results:", results[1])


def worker(num):
    print('Worker', num)

def work():
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()


if __name__ == '__main__':
#    work1()
#    work2()
    work()
