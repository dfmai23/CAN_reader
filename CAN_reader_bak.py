"""
2017 Formula Racing UC Davis
Dustin Mai


Quick little program to monitor the CAN bus wirelessly
Requires PySerial and Tkinter libraries installed

To add a new CAN message:					     ###search###
    - create the byte array ID				        #ADD1#
    - create the StringVar()				        #ADD2#
    - create CAN Decription, Message ID & DATA		#ADD3#
    - set() the StringVar() at the end		        #ADD4#
    - create the conditional				        #ADD5#

"""

import serial
import sys                              #for sys exit
import threading
#import tkFont
from tkinter import *
from time import sleep                  #for after()

#from CAN_recieve import CAN_recieve

COL0_W  = '22'
COL1_W  = '50'
srl = serial.Serial('COM4', 9600, timeout=None) #timeout=none, wiat until requested num of bytes are recieved


frame = Tk()                #main window frame
frame.geometry("740x540")   #4:3 ratio
f = 'Consolas 10'           #font type and sizw 

#anchor west, relief = solid oultine
Label(frame, text='CAN Bus Monitor',  font=f+' bold', anchor='w', width=COL0_W, relief='solid').grid(row=1, column=0)
Label(frame, text=('Port:', srl.port, 'Baud:', srl.baudrate), font=f, anchor='w', width=COL0_W, relief='solid').grid(row=2, column=0)
Label(frame, text='  ID               Data              Timestamp', font=f, anchor='w', width=COL1_W, relief='solid').grid(row=3, column=1)
Label(frame, text='CAN Decription', font=f, width=COL0_W, relief='solid').grid(row=4, column=0)
Label(frame, text='         [1, 2, 3, 4, 5, 6, 7, 8 ]    seconds', font=f, anchor='w', width=COL1_W, relief='solid').grid(row=4, column=1)


#ADD1#
LOGGER_TIME_ID      = bytearray([0x01, 0x23])       # time does not get sent out to the physical bus of the car
LOGGER_HEARTBEAT_ID = bytearray([0x02, 0x23])
DASH_ID             = bytearray([0x06, 0x26])
CURTIS_DEBUG_ID     = bytearray([0x04, 0x66])
CURTIS_STATUS_ID    = bytearray([0x05, 0x66])
CURTIS_RCVACK_ID    = bytearray([0x06, 0x66])
CURTIS_RCV_ID       = bytearray([0x07, 0x66])
CURTIS_VOLTAGE_ID   = bytearray([0x08, 0x66])
THROTTLE_ID         = bytearray([0x02, 0x00])
BRAKE_ID            = bytearray([0x02, 0x01])
BMS_STATUS_ID       = bytearray([0x01, 0x88])
BMS_VOLTAGE_ID      = bytearray([0x03, 0x88])
BMS_TEMP_ID         = bytearray([0x04, 0x88])


#ADD2#
LOGGER_TIME         = StringVar()
LOGGER_HEARTBEAT    = StringVar()
DASH                = StringVar()
CURTIS_DEBUG        = StringVar()
CURTIS_STATUS       = StringVar()
CURTIS_RCVACK       = StringVar()
CURTIS_RCV          = StringVar()
CURTIS_VOLTAGE      = StringVar()
THROTTLE            = StringVar()
BRAKE               = StringVar()
BMS_STATUS          = StringVar()
BMS_VOLTAGE         = StringVar()
BMS_TEMP            = StringVar()
UNKNOWN             = StringVar()


#ADD3#
Label(frame, text=' LOGGER_TIME      ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=5, column=0)
Label(frame, text=' LOGGER_HEARTBEAT ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=6, column=0)
Label(frame, text=' DASH             ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=7, column=0)
Label(frame, text=' CURTIS_DEBUG     ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=8, column=0)
Label(frame, text=' CURTIS_STATUS    ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=9, column=0)
Label(frame, text=' CURTIS_RCVACK    ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=10, column=0)
Label(frame, text=' CURTIS_RCV       ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=11, column=0)
Label(frame, text=' CURTIS_VOLTAGE   ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=12, column=0)
Label(frame, text=' THROTTLE         ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=13, column=0)
Label(frame, text=' BRAKE            ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=14, column=0)
Label(frame, text=' BMS_STATUS       ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=15, column=0)
Label(frame, text=' BMS_VOLTAGE      ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=16, column=0)
Label(frame, text=' BMS_TEMP         ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=17, column=0)
Label(frame, text='                  ', font=f, anchor='w', width=COL0_W, relief='groove').grid(row=99, column=0)

can1 = Label(frame, textvariable=LOGGER_TIME    , font=f, anchor='w', width=COL1_W, relief='groove')
can2 = Label(frame, textvariable=LOGGER_HEARTBEAT, font=f, anchor='w', width=COL1_W, relief='groove')
can3 = Label(frame, textvariable=DASH           , font=f, anchor='w', width=COL1_W, relief='groove')
can4 = Label(frame, textvariable=CURTIS_DEBUG   , font=f, anchor='w', width=COL1_W, relief='groove')
can5 = Label(frame, textvariable=CURTIS_STATUS  , font=f, anchor='w', width=COL1_W, relief='groove')
can6 = Label(frame, textvariable=CURTIS_RCVACK  , font=f, anchor='w', width=COL1_W, relief='groove')
can7 = Label(frame, textvariable=CURTIS_RCV     , font=f, anchor='w', width=COL1_W, relief='groove')
can8 = Label(frame, textvariable=CURTIS_VOLTAGE , font=f, anchor='w', width=COL1_W, relief='groove')
can9 = Label(frame, textvariable=THROTTLE       , font=f, anchor='w', width=COL1_W, relief='groove')
can10 = Label(frame, textvariable=BRAKE         , font=f, anchor='w', width=COL1_W, relief='groove')
can11 = Label(frame, textvariable=BMS_STATUS    , font=f, anchor='w', width=COL1_W, relief='groove')
can12 = Label(frame, textvariable=BMS_VOLTAGE   , font=f, anchor='w', width=COL1_W, relief='groove')
can13 = Label(frame, textvariable=BMS_TEMP      , font=f, anchor='w', width=COL1_W, relief='groove')
can14 = Label(frame, textvariable=UNKNOWN       , font=f, anchor='w', width=COL1_W, relief='groove')

can1.grid(row=5, column=1)
can2.grid(row=6, column=1)
can3.grid(row=7, column=1)
can4.grid(row=8, column=1)
can5.grid(row=9, column=1)
can6.grid(row=10, column=1)
can7.grid(row=11, column=1)
can8.grid(row=12, column=1)
can9.grid(row=13, column=1)
can10.grid(row=14, column=1)
can11.grid(row=15, column=1)
can12.grid(row=16, column=1)
can13.grid(row=17, column=1)
can14.grid(row=99, column=1)


#is a byte array but each element is an int
#msg is temp var to hold received messages
#new_msg replace the test_msgs
#test_msg used to initialized can messages
msg = bytearray()
new_msg = bytearray([0x09,0x99,
0x00,0x00,0x00,0x00,
0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
0xFF,0x0A])
test_msg=('0x%01X%02X     %02X %02X %02X %02X %02X %02X %02X %02X     %d.%03d' %
(9, 153,
255, 255, 255, 255, 255, 255, 255, 255,
0, 000))


class CAN_recieve(threading.Thread):
    def __init__(self):                         #constructor
        super(CAN_recieve, self).__init__()     #self init
        self.alive = True
    #end fn init

    def run(self):
        global msg         #declare globals inside fn that calls it
        global new_msg

        global LOGGER_TIME
        global LOGGER_HEARTBEAT
        global DASH
        global CURTIS_DEBUG
        global CURTIS_STATUS
        global CURTIS_RCVACK
        global CURTIS_RCV
        global CURTIS_VOLTAGE
        global THROTTLE
        global BRAKE
        global BMS_STATUS
        global BMS_VOLTAGE
        global BMS_TEMP

        global can1
        global can2	
        global can3
        global can4
        global can5
        global can6
        global can7
        global can8
        global can9
        global can10
        global can11
        global can12
        global can13

        mask1 = 0
        mask2 = 0
        mask3 = 0
        mask4 = 0

        while self.alive:
            try:
                #msg = srl.read(16) #acquire the wireless CAN message r
                msg = srl.readline()		#'\n' delimiter
               	size = len(msg)

               	if size >= 16 :
	                mask1 = msg[size-14] << 24
	                mask2 = msg[size-13] << 16
	                mask4 = msg[size-12] << 8
	                mark4 = msg[size-11]
	                timestamp = mask1 | mask2 | mask3 | mask4

	                #print(msg)
	                new_msg=('0x%01X%02X     %02X %02X %02X %02X %02X %02X %02X %02X     %d.%03d' %
	                (msg[size-16], msg[size-15],
	                msg[size-10], msg[size-9], msg[size-8], msg[size-7], msg[size-6], msg[size-5], msg[size-4], msg[size-3],
	                timestamp // 1000, timestamp % 1000))
	                print(new_msg)
	                
	                #log to file

	                #ADD5#
	                if msg[0:2] == LOGGER_TIME_ID:
	                    LOGGER_TIME.set(new_msg)    #draw to window

	                elif msg[0:2] == LOGGER_HEARTBEAT_ID:	                
	                    LOGGER_HEARTBEAT.set(new_msg)

	                elif msg[0:2] == DASH_ID:
	                   	DASH.set(new_msg)

	                elif msg[0:2] == CURTIS_DEBUG_ID:
	                    CURTIS_DEBUG.set(new_msg)

	                elif msg[0:2] == CURTIS_STATUS_ID:
	                    CURTIS_STATUS.set(new_msg)

	                elif msg[0:2] == CURTIS_RCVACK_ID:
	                    CURTIS_RCVACK.set(new_msg)

	                elif msg[0:2] == CURTIS_RCV_ID:
	                    CURTIS_RCV.set(new_msg)

	                elif msg[0:2] == CURTIS_VOLTAGE_ID:
	                    CURTIS_VOLTAGE.set(new_msg)

	                elif msg[0:2] == THROTTLE_ID:
	                    THROTTLE.set(new_msg)

	                elif msg[0:2] == BRAKE_ID:
	                    BRAKE.set(new_msg)

	                elif msg[0:2] == BMS_STATUS_ID:
	                    BMS_STATUS.set(new_msg)

	                elif msg[0:2] == BMS_VOLTAGE_ID:
	                    BMS_VOLTAGE.set(new_msg)

	                elif msg[0:2] == BMS_TEMP_ID:
	                    BMS_TEMP.set(new_msg)
	                else:
	                  	UNKNOWN.set(new_msg)
                else:
                	pass
            #end try
            except KeyboardInterrupt:
                self.alive = False                 #close this thread
            #end except
        #end while
    #end run(self)
#end class


can_reader = CAN_recieve()
can_reader.daemon = True        #let gui run in background of main process
def CAN_update():
    can_reader.start()
#end fn

def sysexit():
    sys.exit()
#end fn


#ADD4#
LOGGER_TIME.set(test_msg)
LOGGER_HEARTBEAT.set(test_msg)
DASH.set(test_msg)
CURTIS_DEBUG.set(test_msg)
CURTIS_STATUS.set(test_msg)
CURTIS_RCVACK.set(test_msg)
CURTIS_RCV.set(test_msg)
CURTIS_VOLTAGE.set(test_msg)
THROTTLE.set(test_msg)
BRAKE.set(test_msg)
BMS_STATUS.set(test_msg)
BMS_VOLTAGE.set(test_msg)
BMS_TEMP.set(test_msg)

Label(frame, text='', width=COL0_W).grid(row=100, column=0)		#row=100 end of rows
Button(frame, text="Exit", command=lambda: sysexit(), width='8', relief='raised').grid(row=101)

try:
	frame.after(100, CAN_update)
	frame.mainloop()
except:
	sysexit()
