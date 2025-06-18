# shop_app/task_queue.py
import threading
import queue
import logging
import time
import signal
import sys

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s', handlers=[
        logging.FileHandler("shop_app_worker.log"),  # Log file path
        logging.StreamHandler()  # Also output to console
    ])

task_queue = queue.Queue()
shutdown_event = threading.Event()
workers = []

def process_task(task):
    # Simulate task logic (e.g., update DB, send email)
    logging.info(f"Processing task: {task}")
    time.sleep(2)
    logging.info(f"Finished task: {task}")

def worker():
    while not shutdown_event.is_set():
        try:
            task = task_queue.get(timeout=1)
            process_task(task)
            task_queue.task_done()
        except queue.Empty:
            continue

def start_worker_pool(num_workers=2):
    logging.info(f"Starting {num_workers} worker threads...")
    for _ in range(num_workers):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        workers.append(t)

def graceful_shutdown(*args):
    logging.info("Graceful shutdown initiated...")
    shutdown_event.set()

    # Wait for worker threads to finish
    for t in workers:
        t.join(timeout=5)

    logging.info("All workers shut down cleanly.")
    sys.exit(0)  # Ensure Django exits cleanly

def setup_signal_handlers():
    signal.signal(signal.SIGINT, graceful_shutdown)
    signal.signal(signal.SIGTERM, graceful_shutdown)
    
    
"""How It Works
start_worker_pool() creates daemon threads for concurrent processing.

graceful_shutdown() sets a shutdown flag and joins threads cleanly.

signal.signal() registers system signals like SIGINT (Ctrl+C) or SIGTERM (Docker stop)."""
