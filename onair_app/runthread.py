from threading import Thread
import time

# https://www.geeksforgeeks.org/start-and-stop-a-thread-in-python/
class RunThread:
	
    def __init__(self):
        self._running = True
	
    def terminate(self):
        self._running = False
        
    def run(self, sleepTime, runMeth):
        while self._running:
            runMeth()
            time.sleep(sleepTime)

def startRunThread(runMeth):
    runThread = RunThread()
    newThread = Thread(target = runThread.run, args =(1, runMeth))
    newThread.start()
    return runThread
    # ...
    # Signal termination
    # runThread.terminate()