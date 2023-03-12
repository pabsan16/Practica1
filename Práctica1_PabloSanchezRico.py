# -*- coding: utf-8 -*-
"""
@author: Pablo Sánchez Rico
"""


from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore
from multiprocessing import current_process
from multiprocessing import Array
from time import sleep
from random import random, randint


N=10
NPROD=5
NCONS=1
k=5 


def delay(f=3):
    sleep(random()/f)
       
        
def producer(storage,last, empty_array, non_empty_array,index):
    for v in range(N):
        p=int(current_process().name.split('_')[1])
        empty_array[p].acquire()
        print (f"producer {current_process().name} produciendo")
        delay(6)
        storage[index[p]]=last[p]+randint(0,5)
        last[p]=storage[index[p]]
        index[p]+= 1
        delay(6)
        non_empty_array[p].release()
        print (f"producer {current_process().name} almacenado {storage[index[p]-1]}") 
    empty_array[p].acquire()
    storage[k*p+k-1]=-1
    non_empty_array[p].release()
    

def consumer(storage, empty_array, non_empty_array,index):
    for e in range(NPROD): 
        non_empty_array[e].acquire()
    l=[] 
    while ([-1 for e in range (NPROD*k)])!=[storage[e] for e in range (NPROD*k)]:
        lista_minimos=[storage[i*k] for i in range(NPROD)]
        for e in range (NPROD):
            if lista_minimos[e]!=-1:
                j=lista_minimos[e]
                p=e
                break
        for n in range(NPROD-1):
            if j>lista_minimos[n+1] and lista_minimos[n+1]!=-1:
                j=lista_minimos[n+1]
                p=n+1    
        index[p]=index[p]-1
        for h in range(p*k,p*k+k-1):
            storage[h]=storage[h+1]
        if storage[p*k+k-1]==-1:
            storage[p*k+k-1]=-1
        else:
            storage[p*k+k-1]=0
        print (f"consumer consumiendo {j}")
        l.append(j)
        empty_array[p].release()
        delay(6)
        non_empty_array[p].acquire()
    print ("elementos consumidos: " + str(l))
        

def main():
    storage=Array('i', NPROD*k)
    last=Array('i', NPROD)
    index=Array('i',NPROD)
    for e in range (NPROD):
        index[e]=e*k
        last[e]=0
    for e in range(NPROD*k):
        storage[e]=0
    print ("almacen inicial", storage[:])    
    non_empty_array=[Semaphore(0) for e in range(NPROD)]
    empty_array=[BoundedSemaphore(k) for e in range(NPROD)]
    prodlst=[Process(target=producer,
                        name=f'prod_{i}',
                        args=(storage,last, empty_array, non_empty_array, index))
                for i in range(NPROD)]
    conslst=[Process(target=consumer,
                      name=f"cons",
                      args=(storage, empty_array, non_empty_array,index))]
    for e in prodlst + conslst:
        e.start()
    for e in prodlst + conslst:
        e.join()
        
        
if __name__ == '__main__':
    main()




















