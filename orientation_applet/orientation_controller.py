import orientation_applet.resource as resource
import orientation_applet.ui as ui
import subprocess
import time
import os
import gi
import re
gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify
from threading import Thread

rotate = True
previous_state = 0
current_state = 0
command = "xsetwacom list"
drivers = subprocess.check_output(command.split())
#"'NTRG0001:01 1B96:1B05 touch'"
touch = re.findall(r'[0-9][0-9]',str(re.findall(r'id: [0-9][0-9]\\ttype: TOUCH', str(drivers))))
if touch == []:
	touch = re.findall(r'[0-9][0-9]',str(re.findall(r'id: [0-9][0-9]\ttype: TOUCH', str(drivers))))[0]
else:
	touch = touch[0]

#"'NTRG0001:01 1B96:1B05 Pen stylus'"
pen = re.findall(r'[0-9][0-9]',str(re.findall(r'id: [0-9][0-9]\\ttype: STYLUS', str(drivers))))
if pen == []:
	pen = re.findall(r'[0-9][0-9]',str(re.findall(r'id: [0-9][0-9]\ttype: STYLUS', str(drivers))))[0]
else:
	pen = pen[0] 
#"'NTRG0001:01 1B96:1B05 Pen eraser'"
eraser = re.findall(r'[0-9][0-9]',str(re.findall(r'id: [0-9][0-9]\\ttype: TOUCH', str(drivers))))
if eraser == []:
	eraser = re.findall(r'[0-9][0-9]',str(re.findall(r'id: [0-9][0-9]\ttype: ERASER', str(drivers))))[0]
else:
	eraser = eraser[0]
class OrientationManager(object):
	def __init__(self):
		self.path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
		self.iiopath = self.getsensor()
		
	def set_orientation(self, direction):
		#Commands for correct rotation
		if direction == 'normal':
			pen_rotate = 'none'
		elif direction == 'inverted':
			pen_rotate = 'half'
		elif direction == 'left':
			pen_rotate = 'ccw'
		elif direction == 'right':
			pen_rotate = 'cw'

		rotate_commands = ['xrandr -o ' + direction, 'xsetwacom set ' + touch + ' rotate ' + pen_rotate, 'xsetwacom set ' + pen + ' rotate ' + pen_rotate, 'xsetwacom set ' + eraser + ' rotate ' + pen_rotate]

		for command in rotate_commands: 
			subprocess.call(command.split(), shell=False)


	def enable_auto_rotate(self):
		global rotate
		rotate = True
		notify.init ("Rotation-ON")
		RotationON=notify.Notification.new ("Rotation","Screenrotation is now unlocked",resource.image_path("screen_auto_rotation", "dark"))
		RotationON.show ()

	def disable_auto_rotate(self):
		global rotate		
		rotate = False
		notify.init ("Rotation-Off")
		RotationOFF=notify.Notification.new ("Rotation","Screenrotation is now locked",resource.image_path("screen_lock_rotation", "dark"))
		RotationOFF.show ()

	def palm_detection(self, enable):
		status = enable
		stylusProximityCommand = 'xinput query-state ' + pen
		stylusProximityResult = subprocess.check_output(stylusProximityCommand.split(), shell=False)
		stylusProximityStatus = re.findall('In|Out', stylusProximityResult)[0]		
		if stylusProximityStatus == "out" and status == True:
			subprocess.call('xinput enable', touch)
		elif stylusProximityStatus == "in" and status == True:
			subprocess.call('xinput disable', touch)

	#def refreshtouch(self):
		#subprocess.call(['xinput disable', touch], shell=False)
		#subprocess.call(['xinput enable', touch], shell=False)

	def checkdisplays(self):
		check_displays = "xrandr | grep -w 'connected'"
		str_displays = str(subprocess.check_output(check_displays, shell=True).lower().rstrip())
		list_displays = str_displays.splitlines()
		int_displays = len(list_displays)
		return int_displays

	def initiate_fetcher(self, parent):		
		self._fetcher = StatusFetcher(parent)
		self._fetcher.start()
		


	def getsensor(self):
		count = 0
		while count <= 9:
			if os.path.exists('/sys/bus/iio/devices/iio:device' + str(count) +  '/in_accel_scale') == True:
				return '/sys/bus/iio/devices/iio:device' + str(count) + '/' # directory of accelerometer device (iio)
				break
			count = count + 1


	def get_orientation(self):
		global previous_state
		global current_state
		state_dict = {0: "normal", 1: "inverted", 2: "left", 3: "right"}
		iiopath = self.getsensor()
		multimonitor = False
		int_displays = self.checkdisplays()
		if int_displays > 1:
			multimonitor = True
		with open(self.iiopath + 'in_accel_scale') as f:
			scale = float(f.readline())
		if rotate == True and multimonitor == False:
			with open(self.iiopath + 'in_accel_x_raw', 'r') as fx:
				with open(self.iiopath + 'in_accel_y_raw', 'r') as fy:
					with open(self.iiopath + 'in_accel_z_raw', 'r') as fz:	
						xcoord = float(fx.readline())
						ycoord = float(fy.readline())
						zcoord = float(fz.readline())
						if self.checkdisplays() == 1:
							if (xcoord >= 65000 or xcoord <=650):
								if (ycoord <= 65000 and ycoord >= 64000):
									current_state = 0					
									if (ycoord >= 650 and ycoord <= 1100):
										current_state = 1
							if (xcoord <= 64999 and xcoord >= 650):
								if (xcoord >= 800 and xcoord <= 1000):
									current_state = 2
								if (xcoord >= 64500 and xcoord <=64700):
									current_state = 3	
			if current_state != previous_state:
				previous_state = current_state
				self.set_orientation(state_dict[current_state])
#				self.refreshtouch()

class StatusFetcher(Thread):
	def __init__(self, parent):
		Thread.__init__(self)
		self._parent = parent
		self.mgr = OrientationManager()
		self.freq = 5.0

	def fetch(self):
		return self.mgr.get_orientation()
		
	def run(self):
		"""It is the main loop."""
		while self._parent.alive.isSet():
			data = self.fetch()
			time.sleep(1.0/self.freq)

