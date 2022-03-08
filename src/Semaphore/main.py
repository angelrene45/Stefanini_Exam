"""
    Login queue

    Consider a system that can only support two users (S=2). 

    -Create 4 user ( 1 thread peer user )
"""

import threading
import time 

MAX_THREADS_SEMAPHORE = 2 # only 2 user is allowed 
sema = threading.Semaphore( MAX_THREADS_SEMAPHORE ) # by default is 1 ( it means can be accessed 1 thread at a time ) 

def login( name, time_session ):
    sema.acquire()
    print (f"{name} is logged")
    time.sleep(time_session) # simulate user is in system for time_session
    print (f"{name} is logout")
    sema.release() # logout

if __name__ == "__main__":  
    # create users with name of user and time session  
    user1 = threading.Thread(target=login, args=('Juan',4))
    user2 = threading.Thread(target=login, args=('René',10))
    user3 = threading.Thread(target=login, args=('Monse',15))
    user4 = threading.Thread(target=login, args=('Leonel',20))

    # simulate user login
    user1.start()
    user2.start()
    user3.start()
    user4.start()