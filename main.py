import os
import threading
import multiprocessing
from queue import Queue
import time

def process_file_thread(filename, keywords, results_queue):
    result = {}
    try:
        with open(os.path.join('data', filename), 'r') as file:
            content = file.read()
            
            for keyword in keywords:
                if keyword in content:
                    result[keyword] = filename
    except FileNotFoundError as e:
        pass
    results_queue.put(result)

def process_file_process(filename, keywords, results_list):
    result = {}
    try:
        with open(os.path.join('data', filename), 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    result[keyword] = filename

    except FileNotFoundError as e:
       pass
    results_list.append(result)

def threading_tasks(files, keywords):
    results_queue = Queue()

    start_time = time.time()
    threads = []
    for file in files:
        thread = threading.Thread(target=process_file_thread, args=(file, keywords, results_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    result = {}
    for keyword in keywords:
        result[keyword] = []

    while not results_queue.empty():
        res_th = results_queue.get()
        for key in res_th:
            result[key].append(res_th[key])

    print(f'\nTime taken with threads: {time.time() - start_time} seconds')

    return result

def process_tasks(files, keywords):
    start_time = time.time()
    multiprocessing.set_start_method('spawn')
    result = {}
    for keyword in keywords:
        result[keyword] = []
    with multiprocessing.Manager() as manager:
        results_list = manager.list()

        processes = []
        for file in files:
            process = multiprocessing.Process(target=process_file_process, args=(file, keywords, results_list))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()

        for result_p in results_list:
            for key in result_p:
                result[key].append(result_p[key])
                
    print(f'\nTime taken with processes: {time.time() - start_time} seconds')
    return result


if __name__ == '__main__':
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt', 'file5.txt']
    keywords = ['sometimes', 'ipsum']

    res_th = threading_tasks(files, keywords)
    print("\nThreading result:\n")
    print(res_th)
    # ------------------------------
    res_p = process_tasks(files, keywords)
    print("\nProcess result:\n")
    print(res_p)