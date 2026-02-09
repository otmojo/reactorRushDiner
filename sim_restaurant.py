import time
import threading
import queue
import asyncio
from visual import YangiConsole

IO_WAIT_TIME = 0.4
CPU_PROCESS_TIME = 0.07
CONTEXT_SWITCH_COST = 0.001 

def run_multi_thread_sim(num_customers=50, num_workers=10):
    q = queue.Queue()
    processed = 0
    lock = threading.Lock()
    start = time.time()

    def worker():
        nonlocal processed
        while True:
            item = q.get()
            if item is None:
                q.task_done()
                break
            time.sleep(CONTEXT_SWITCH_COST)
            time.sleep(IO_WAIT_TIME)
            time.sleep(CPU_PROCESS_TIME)
            with lock:
                processed += 1
                if processed % 5 == 0 or processed == num_customers:
                    YangiConsole.progress_bar(processed, num_customers, "THREAD_POOL")
            q.task_done()

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(num_workers)]
    for t in threads: t.start()
    
    for i in range(num_customers): q.put(i)
    for _ in range(num_workers): q.put(None)
    
    q.join()
    duration = time.time() - start
    throughput = processed / duration if duration > 0 else 0
    fake_cpu = ((CPU_PROCESS_TIME + CONTEXT_SWITCH_COST) * processed) / (duration * num_workers) * 100
    return throughput, min(fake_cpu, 100.0)

async def nio_customer_task(cid, progress_callback):
    await asyncio.sleep(IO_WAIT_TIME)
    await asyncio.sleep(CPU_PROCESS_TIME)
    progress_callback()

async def run_nio_sim(num_customers=50):
    start = time.time()
    processed = 0
    def update_progress():
        nonlocal processed
        processed += 1
        if processed % 5 == 0 or processed == num_customers:
             YangiConsole.progress_bar(processed, num_customers, "ASYNC_CORE")

    tasks = [asyncio.create_task(nio_customer_task(i, update_progress)) for i in range(num_customers)]
    await asyncio.gather(*tasks)
    duration = time.time() - start
    throughput = num_customers / duration if duration > 0 else 0
    fake_cpu = (CPU_PROCESS_TIME * num_customers) / duration * 100
    return throughput, min(fake_cpu, 100.0)