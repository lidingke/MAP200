import threading
import time
class Pyr(threading.Thread):
    """docstring for Pyr"""
    def __init__(self,):
        super(Pyr, self).__init__()
        # self.arg = arg

    def run(self):
        # while :
        #     pass
        for _ in range(1,10):
            a = '11'
            print '_',_
            time.sleep(1)

