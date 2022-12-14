from threading import Thread
import time
from string import Template

# https://www.geeksforgeeks.org/start-and-stop-a-thread-in-python/
class BackgroundThread:
	
    def __init__(self):
        self._running = True
	
    def terminate(self):
        self._running = False
        
    def run(self, sleep_time, run_function):
        while self._running:
            run_function()
            time.sleep(sleep_time)

def start_background_thread(sleep_time, run_function):
    background_thread = BackgroundThread()
    new_thread = Thread(target = background_thread.run, args =(sleep_time, run_function))
    new_thread.start()
    return background_thread
    # Usage:
    # import dnp_util as dnp_util
    # 1 = sleep 1 second between activations
    # broadcast_status = name of funtion to run every loop
    # background_thread = start_background_thread(1, broadcast_status)
    # Signal termination
    # background_thread.terminate()



# https://stackoverflow.com/a/30536361
class DeltaTemplate(Template):
    delimiter = '%'

# util to format a delta time object
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

