"""

import threading
import time

lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1():
    with lock_a:
        print("Thread 1: tengo A")
        time.sleep(0.1)
        print("Thread 1: pidiendo B...")
        with lock_b:  # Espera B
            print("Thread 1: tengo A y B")

def thread_2():
    with lock_b:
        print("Thread 2: tengo B")
        time.sleep(0.1)
        print("Thread 2: pidiendo A...")
        with lock_a:  # Espera A: DEADLOCK
            print("Thread 2: tengo B y A")

t1 = threading.Thread(target=thread_1)
t2 = threading.Thread(target=thread_2)
t1.start(); t2.start()
# El programa se cuelga: ninguno termina porque cada uno espera al otro.
# Matar con Ctrl+C después de verlo colgado.
"""
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1():
    with lock_a:
        with lock_b:
            print("Thread 1: tengo A y B")

def thread_2():
    with lock_a:    # Mismo orden que thread_1
        with lock_b:
            print("Thread 2: tengo A y B")

t1 = threading.Thread(target=thread_1)
t2 = threading.Thread(target=thread_2)
t1.start(); t2.start()
t1.join(); t2.join()
