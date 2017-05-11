import serial
import threading
import os
from tkinter import *
from datetime import datetime as dt

from CAN_globals import CAN_map, msg, new_msg, UNKNOWN

logs_path = os.getcwd() + '\\logs\\'

class CAN_recieve(threading.Thread):
    def __init__(self, srl):                         #constructor
        super(CAN_recieve, self).__init__()     #self init
        self.alive = True
        self.srl = srl
    #end fn init

    def run(self):
        global msg         #declare globals inside fn that calls it
        global new_msg
        global CAN_map

        size = 0

        if not os.path.exists(logs_path):           #make logs folder
            os.makedirs(logs_path)
        datetime = dt.now().strftime('(%Y-%m-%d)_%H.%M.%S')   
        #log = open(logs_path+datetime+'.txt', 'w')
        log = 0
        #print(logs_path+datetime)
    
        while self.alive:
            try:
                #msg = srl.read(16) #acquire the wireless CAN message r
                msg = self.srl.readline()        #'\n' delimiter
                size = len(msg)

                if size >= 16 and msg[size-2] == 255:   #0xFF0A delimiter
                    self.CAN_process(msg, size, log)
                #if size >=16 and msg[size-2] == 255:
                else:   #get rest of message
                    msg += self.srl.readline()  
                    size = len(msg)
                    if size >= 16 and msg[size-2] == 255:   #0xFF0A delimiter
                        self.CAN_process(msg, size, log)
                #else
            #try
            except KeyboardInterrupt:
                self.alive = False                 #close this thread
            #except
        #while
        #file.close() 
    #run(self)

    def CAN_process(self, msg, size, log):
        mask1 = 0
        mask2 = 0
        mask3 = 0
        mask4 = 0

        mask1 = msg[size-14] << 24
        mask2 = msg[size-13] << 16
        mask4 = msg[size-12] << 8
        mark4 = msg[size-11]
        timestamp = mask1 | mask2 | mask3 | mask4

        #print('%u %s' % (size, msg))
        new_msg=('0x%01X%02X     %02X %02X %02X %02X %02X %02X %02X %02X     %d.%03d' %
        (msg[size-16], msg[size-15],
        msg[size-10], msg[size-9], msg[size-8], msg[size-7], msg[size-6], msg[size-5], msg[size-4], msg[size-3],
        timestamp // 1000, timestamp % 1000))
        #print(new_msg)
       
        CAN_ID = ('%1X%02X' % (msg[size-16], msg[size-15]))
        CAN_msg = CAN_map.get(CAN_ID)
        if CAN_msg != None:
            CAN_msg.set(new_msg)
        else:
            UNKNOWN.set(new_msg)

        #log to file
        #log.write('%s,%u,%X,%X,%X,%X,%X,%X,%X,%X\n' % 
        #(CAN_ID, timestamp, msg[size-10], msg[size-9], msg[size-8], msg[size-7], msg[size-6], msg[size-5], msg[size-4], msg[size-3]))
    #CAN_process()
#end class