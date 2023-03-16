"""
@author: Pablo Sánchez Rico
"""

from multiprocessing import Process
from multiprocessing import Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
from random import random, randint

N = 10
NPROD = 5
NCONS = 1


def delay(f = 3):
    sleep(random()/f)
       
        
def producer(storage,last, empty_array, non_empty_array):
    for v in range(N):
        p=int(current_process().name.split('_')[1])
        empty_array[p].acquire()
        print (f"producer {current_process().name} produciendo")
        delay(6)
        storage[p] = last[p] + randint(0,5)
        last[p] = storage[p]
        delay(6)
        non_empty_array[p].release()
        print (f"producer {current_process().name} almacenado {storage[p]}")
    empty_array[p].acquire()
    storage[p] = -1
    non_empty_array[p].release()


def consumer(storage, empty_array, non_empty_array):
    for e in range(NPROD):# espera a que todos hayan producido
        non_empty_array[e].acquire()
    l = [] #lista con elementos consumidos
    while ([-1 for e in range (NPROD)])!= [storage[e] for e in range (NPROD)]:
        for e in range (NPROD):
            if storage[e] != -1:
                j = storage[e]
                p = e
                break
        for e in range(NPROD-1):
            if j > storage[e+1] and storage[e+1]!=-1:
                j = storage[e+1]
                p = e+1       
        print (f"consumer consumiendo {j}")
        l.append(j)
        empty_array[p].release()
        delay(6)
        non_empty_array[p].acquire()
    print ("elementos consumidos: "+str(l))

        

def main():
    storage = Array('i', NPROD)
    last = Array('i', NPROD)
    for e in range(NPROD):
        storage[e] = 0
        last[e] = 0
    print ("almacen inicial", storage[:])
    
    non_empty_array = [Semaphore(0) for j in range(NPROD)]
    empty_array = [Lock() for j in range(NPROD)]

    prodlst = [ Process(target=producer,
                        name=f"prod_{e}",
                        args=(storage,last, empty_array, non_empty_array))
                for e in range(NPROD) ]

    conslst = [Process(target=consumer,
                      name=f"cons",
                      args=(storage, empty_array, non_empty_array))]

    for e in prodlst + conslst:
        e.start()

    for e in prodlst + conslst:
        e.join()

if __name__ == '__main__':
    main()

