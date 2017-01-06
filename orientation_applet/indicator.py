#!/usr/bin/env python3
import orientation_applet.resource as resource
import orientation_applet.ui as ui
import orientation_applet.autoupdate as autoupdate
import signal
import sys
import os
import gi
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')
from orientation_applet.orientation_controller import OrientationManager
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import Gtk as gtk
from threading import Event as event

#PARAMETERS
appindicator_ID = 'screen_orientation_indicator'
path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
doquit = False
class OrientationIndicator(object):
	def __init__(self):
		self.setup_indicator()
		self.check_for_updates()
		self.alive = event()
		self.alive.set()
		self.rotate_mgr = OrientationManager()
		self.rotate_mgr.initiate_fetcher(self)
		
	def toggle(item, self, indicator):
		rotate_toggle_mgr = OrientationManager()
		if self.get_active():
			indicator.set_status(appindicator.IndicatorStatus.ATTENTION)
			rotate_toggle_mgr.disable_auto_rotate()
		else:
			indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
			rotate_toggle_mgr.enable_auto_rotate()
	
	def _shutdown(self):
		self.alive.clear()
		try:
			gtk.main_quit()
		except RuntimeError:
			pass

	def quit(self, item):
		self._shutdown()

	def open_about_page(self, item):
		import webbrowser
		webbrowser.open('https://github.com/virtualguywithabowtie/surface-orientation')
	
	def check_for_updates(self):
		if autoupdate.is_update_available():
			notify.init("Update-Available")
			UpdateAvailable=notify.Notification.new ("Orientation Update","A newer version of Orientation is available on GitHub. "+\
				"Open 'About' to navigate to the project page.")
			UpdateAvailable.show()
		
	def run(self):
		gtk.main()

	def setup_menu(self,indicator):
		def add_item(item):
			item.show()
			menu.append(item)
			return item
		menu = gtk.Menu()
		toggle_button = add_item(gtk.CheckMenuItem("Lock Orentation"))
		toggle_button.connect("toggled", self.toggle, indicator)
		indicator.set_secondary_activate_target(toggle_button)
		add_item(gtk.SeparatorMenuItem())
		add_item(gtk.MenuItem('About')).connect("activate", self.open_about_page)
		add_item(gtk.MenuItem("Exit")).connect("activate", self.quit)
		return menu

	def setup_indicator(self):
		indicator = appindicator.Indicator.new(appindicator_ID,resource.image_path("screen_auto_rotation", ui.THEME),appindicator.IndicatorCategory.APPLICATION_STATUS)
		indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
		indicator.set_attention_icon(resource.image_path("screen_lock_rotation", ui.THEME))
		indicator.set_menu(self.setup_menu(indicator))
		return indicator

def main():
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	OrientationIndicator().run()

if __name__ == "__main__":
	main()


