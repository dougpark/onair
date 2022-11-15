from threading import Thread
import time
from string import Template

# https://www.geeksforgeeks.org/start-and-stop-a-thread-in-python/
class RunThread:
	
    def __init__(self):
        self._running = True
	
    def terminate(self):
        self._running = False
        
    def run(self, sleep_time, run_function):
        while self._running:
            run_function()
            time.sleep(sleep_time)

def start_run_thread(run_function):
    run_thread = RunThread()
    new_thread = Thread(target = run_thread.run, args =(1, run_function))
    new_thread.start()
    return run_thread
    # ...
    # Signal termination
    # run_thread.terminate()



    # https://stackoverflow.com/a/30536361
class DeltaTemplate(Template):
    delimiter = '%'

# https://stackoverflow.com/a/30536361
def strfdelta(td, fmt):

    # Get the timedelta’s sign and absolute number of seconds.
    sign = "+" if td.days < 0 else "-"
    secs = abs(td).total_seconds()

    # Break the seconds into more readable quantities.
    days, rem = divmod(secs, 86400)  # Seconds per day: 24 * 60 * 60
    hours, rem = divmod(rem, 3600)  # Seconds per hour: 60 * 60
    mins, secs = divmod(rem, 60)

    # Format (as per above answers) and return the result string.
    t = DeltaTemplate(fmt)
    return t.substitute(
        s=sign,
        D="{:d}".format(int(days)),
        H="{:02d}".format(int(hours)),
        M="{:02d}".format(int(mins)),
        S="{:02d}".format(int(secs)),
        )

