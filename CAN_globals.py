from tkinter import *

#ADD1#
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

#ADD2#	#dictionary	#ID's as string
CAN_map = { '123': LOGGER_TIME,
						'223': LOGGER_HEARTBEAT,
						'626': DASH,
						'466': CURTIS_DEBUG,
						'566': CURTIS_STATUS,
						'666': CURTIS_RCVACK,
						'766': CURTIS_RCV,
						'866': CURTIS_VOLTAGE,
						'200': THROTTLE,
						'201': BRAKE,
						'188': BMS_STATUS,
						'388': BMS_VOLTAGE,
						'488': BMS_TEMP}



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
