
from tkinter.filedialog import askopenfilename

"""
#process a log file to match BMS voltage to throttle/brake input
class data_process(threading.Thread):
  def __init__(self):                         #constructor
    super(data_process, self).__init__()     #self init
    self.alive = True
  #end fn init

  def run(self):
  	filename = askopenfilename() # show an "Open" dialog box and returns path of selected file
	#end fn
#end class
"""


def data_process():
	prev_voltage	= '388,999,F,D6,10,3A,00,01,C3,E3\n'
	prev_throttle = '200,1000,0,0,0,0,0,0,0,0\n'
	prev_brake 		= '201,1001,0,0,0,0,0,0,0,0\n'
	timestamp = 0

	filename  = askopenfilename() # show an "Open" dialog box and returns path of selected file
	filename2 = filename[:-4]+'_processed'+'.csv' 	#[:-4] removes ".csv"
	file  = open(filename,  'r')
	file2 = open(filename2, 'w')	
	#print(filename2)

	for line in file:		#read file line by line and process
		#print(line, end='')

		#only writes if new throttle/brake message
		if line[:3] == '200' or line[:3] == '201':	#throttle/brake
			if line[:3] == '200':			 #throttle
				prev_throttle = line
			else:	# line[:3] == '201': #brake
				prev_brake = line

			timestamp = line.split(',')[1]
			line_processed = prev_throttle[:-1]+',,'+prev_brake[:-1]+',,'+prev_voltage[:-1]+',,'+timestamp+'\n'	#[:-1] removes '\n'
			file2.write(line_processed)
			#print(line+' '+timestamp)
			#print(line_processed)
		elif line[:3] == '388':
			prev_voltage = line
	#end for

	file.close()
#end fn
