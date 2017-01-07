#!/usr/bin/python3

import os
import shutil
from setuptools import setup

from orientation_applet.resource import RESOURCES_DIRECTORY_PATH


def find_resources(resource_dir):
    target_path = os.path.join(RESOURCES_DIRECTORY_PATH, resource_dir)
    resource_names = os.listdir(resource_dir)
    resource_list = [os.path.join(resource_dir, file_name) for file_name in resource_names]
    return (target_path, resource_list)

def install_driver():
	path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
	FILE_DIR = '/etc/X11/xorg.conf.d/'
	FILE_WACOM = FILE_DIR + '52-wacom.conf'
	#if os.path.isfile(FILE_EVDEV):
	#	os.rename(FILE_EVDEV,FILE_EVDEV + '.bak')
	if not os.path.exists(FILE_DIR):
        	os.makedirs(FILE_DIR)
	if os.path.isfile(FILE_WACOM):
		os.rename(FILE_WACOM,FILE_WACOM + '.bak')
	shutil.copy(os.path.join(path, 'drivers/52-wacom.conf'),FILE_WACOM)

install_driver()
setup(name="Orientation",
      version="2.0.2",
      description="Auto Orientation Indicator for Ubuntu on Surface",
      url='https://github.com/vguywithabowtie/orientation',
      author='VirtualGuywithaBowTie',
      author_email='virtualguywithabowtie@users.noreply.github.com',
      license='GNU',
      packages=["orientation_applet"],
      data_files=[
          ('/usr/share/applications', ['orientation.desktop']),
          find_resources("icons/light"),
          find_resources("icons/dark")],
      scripts=["bin/orientation"]
)

print("Please restart computer after installation!!!!!!!")
