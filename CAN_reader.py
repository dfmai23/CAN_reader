"""
2017 Formula Racing UC Davis FE4
Dustin Mai

Program to monitor the CAN bus wirelessly
Requires PySerial and Tkinter libraries

To add a new CAN message:					     ###search###
    - create the StringVar()				       	#ADD1#
    - add ID and StringVar() to map				    #ADD2#
    - create CAN Decription, Message ID & DATA		#ADD3#
    - set() the StringVar() at the end		        #ADD4#

"""

import serial
import sys                              #for sys exit
import threading
from tkinter import *
from time import sleep                  #for after()


COL0_W  = '22'
COL1_W  = '50'
srl = serial.Serial(port='COM8', baudrate=9600, timeout=None) #timeout=none, wiat until requested num of bytes are recieved


frame = Tk()                #main window frame
frame.geometry("740x540")   #4:3 ratio
f = 'Consolas 10'           #font type and size


from CAN_globals import *		#has to be after root window is created
from CAN_recieve import CAN_recieve
from data_process import *

#anchor west, relief = solid oultine
Label(frame, text='CAN Bus Monitor',  font=f+' bold', anchor='w', width=COL0_W, relief='solid').grid(row=1, column=0)
Label(frame, text=('Port:', srl.port, 'Baud:', srl.baudrate), font=f, anchor='w', width=COL0_W, relief='solid').grid(row=2, column=0)
Label(frame, text='  ID               Data              Timestamp', font=f, anchor='w', width=COL1_W, relief='solid').grid(row=3, column=1)
Label(frame, text='CAN Decription', font=f, width=COL0_W, relief='solid').grid(row=4, column=0)
Label(frame, text='         [1, 2, 3, 4, 5, 6, 7, 8 ]    seconds', font=f, anchor='w', width=COL1_W, relief='solid').grid(row=4, column=1)


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



can_reader = CAN_recieve(srl)
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
Button(frame, text="Exit", command=lambda: sysexit(), width='8', relief='raised').grid(row=101, column=0)
Button(frame, text="Process file", command=lambda: data_process(), width='8', relief='raised').grid(row=101, column=1)

try:
	frame.after(100, CAN_update)
	frame.mainloop()
except:
	sysexit()
