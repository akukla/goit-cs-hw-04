import os
import threading
import multiprocessing
from queue import Queue
import time

def process_file_thread(filename, keyword, results_queue):
    try:
        with open(os.path.join('data', filename), 'r') as file:
            content = file.read()
            if keyword in content:
                results_queue.put(f'Keyword "{keyword}" found in file {filename}')
            else:
                results_queue.put(f'Keyword "{keyword}" NOT found in file {filename}')
    except FileNotFoundError as e:
        results_queue.put(f'File {filename} not found!')

def process_file_process(filename, keyword, results_list):
    try:
        with open(os.path.join('data', filename), 'r') as file:
            content = file.read()
            if keyword in content:
                results_list.append(f'Keyword "{keyword}" found in file {filename}')
            else:
                results_list.append(f'Keyword "{keyword}" NOT found in file {filename}')
    except FileNotFoundError as e:
        results_list.append(f'File {filename} not found!')

def main():
    files = ['file1.txt', 'file2.txt', 'file3.txt', 'file4.txt', 'file5.txt']
    keyword = 'sometimes'

    results_queue = Queue()

    start_time = time.time()
    threads = []
    for file in files:
        thread = threading.Thread(target=process_file_thread, args=(file, keyword, results_queue))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("\nThreading result:\n")
    while not results_queue.empty():
        print(results_queue.get())
    print(f'\nTime taken with threads: {time.time() - start_time} seconds')

    # ------------------------------

    start_time = time.time()
    multiprocessing.set_start_method('spawn')
    with multiprocessing.Manager() as manager:
        results_list = manager.list()

        processes = []
        for file in files:
            process = multiprocessing.Process(target=process_file_process, args=(file, keyword, results_list))
            process.start()
            processes.append(process)

        for process in processes:
            process.join()
        print("\nProcess result:\n")
        for result in results_list:
            print(result)
    print(f'\nTime taken with processes: {time.time() - start_time} seconds')

if __name__ == '__main__':
    main()