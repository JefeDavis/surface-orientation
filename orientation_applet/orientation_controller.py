import orientation_applet.resource as resource
import orientation_applet.ui as ui
import subprocess
import time
import os
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify
from threading import Thread

rotate = True
quit = False
class OrientationManager(object):
	def __init__(self):
		self.path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
		self.touch = '17' #"'NTRG0001:01 1B96:1B05 touch'"
		self.pen = '16' #"'NTRG0001:01 1B96:1B05 Pen stylus'"
		self.eraser = '18' #"'NTRG0001:01 1B96:1B05 Pen eraser'"
		self.iiopath = self.getsensor()
		
	def set_orientation(self, x, y, z):
		#Commands for correct rotation
		normals = ['xrandr -o normal', 'xsetwacom set ' + self.touch + ' rotate none', 'xsetwacom set ' + self.pen + ' rotate none', 'xsetwacom set ' + self.eraser + ' rotate none']

		inverteds = ['xrandr -o inverted', 'xsetwacom set ' + self.touch + ' rotate half', 'xsetwacom set ' + self.pen + ' rotate half', 'xsetwacom set ' + self.eraser + ' rotate half']

		lefts = ['xrandr -o left', 'xsetwacom set ' + self.touch + ' rotate ccw', 'xsetwacom set ' + self.pen + ' rotate ccw', 'xsetwacom set ' + self.eraser + ' rotate ccw']

		rights = ['xrandr -o right', 'xsetwacom set ' + self.touch + ' rotate cw', 'xsetwacom set ' + self.pen + ' rotate cw', 'xsetwacom set ' + self.eraser + ' rotate cw']

		if self.checkdisplays() == 1:
			if (x >= 65000 or x <=650):
				if (y <= 65000 and y >= 64000):
					for normal in normals: 
						subprocess.call(normal.split(), shell=False)
					self.current_state = 0
				if (y >= 650 and y <= 1100):
					for inverted in inverteds:
						subprocess.call(inverted.split(), shell=False)
					self.current_state = 1
			if (x <= 64999 and x >= 650):
				if (x >= 800 and x <= 1000):
					for left in lefts:
						subprocess.call(left.split(), shell=False)
					self.current_state = 2
				if (x >= 64500 and x <=64700):
					for right in rights:					
						subprocess.call(right.split(), shell=False)
					self.current_state = 3

	def enable_auto_rotate(self):
		global rotate
		rotate = True
		notify.init ("Rotation-OFF")
		RotationON=notify.Notification.new ("Rotation","Screenrotation is now unlocked",resource.image_path("screen_auto_rotation", "dark"))
		RotationON.show ()

	def disable_auto_rotate(self):
		global rotate		
		rotate = False
		notify.init ("Rotation-ON")
		RotationOFF=notify.Notification.new ("Rotation","Screenrotation is now locked",resource.image_path("screen_lock_rotation", "dark"))
		RotationOFF.show ()

	def refreshtouch(self):
		subprocess.call('xinput disable',self.touch)
		subprocess.call('xinput enable',self.touch)

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
		current_state = 0
		iiopath = self.getsensor()
		multimonitor = False
		int_displays = self.checkdisplays()
		if int_displays > 1:
			multimonitor = True
		previous_state = current_state
		with open(self.iiopath + 'in_accel_scale') as f:
			scale = float(f.readline())
		if rotate == True and multimonitor == False:
			with open(self.iiopath + 'in_accel_x_raw', 'r') as fx:
				with open(self.iiopath + 'in_accel_y_raw', 'r') as fy:
					with open(self.iiopath + 'in_accel_z_raw', 'r') as fz:	
						xcoord = float(fx.readline())
						ycoord = float(fy.readline())
						zcoord = float(fz.readline())
						self.set_orientation(xcoord,ycoord,zcoord)
		if current_state != previous_state:
			self.refreshtouch()

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

