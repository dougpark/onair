#!/usr/bin/python
# https://www.tutorialspoint.com/python/python_multithreading.htm

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, delay):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.delay = delay
   def run(self):
      print("Starting " + self.name)
      print_time(self.name, 5, self.delay)
      print("Exiting " + self.name)

def print_time(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print ("%s: %s, %s" % (threadName, counter, time.ctime(time.time())))
      counter -= 1

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

print ("Exiting Main Thread")