# Orientation Controller & Indicator for Ubuntu Unity / Gnome on Microsoft Surface Pro 3

Application and indicator to allow automatic screen rotation and locking for ubuntu
on a Microsoft Surface Pro 3.

Main features:

- auto rotates screen based on accelerometer data.
- optionally, locks orientation to current configuration.
- theming support for icons

# Usage

**Install**:

	please note: this program requires the use of the wacom driver for inputs. 
	On install this program will replace your 10-evdev.conf and 50-wacom.conf files
	located at `/usr/share/X11/xorg-conf.d/`.
	Your old files will be saved in .bak format within the same direcotry 

To install Orientation run
	
	$ sudo pip install git+https://github.com/virtualguywithabowtie/surface-orientation.git

If you do not have `pip` you may install it by running

	$ sudo apt-get install python-pip python-dev build-essential 

	$ sudo pip install --upgrade pip 

	$ sudo pip install --upgrade virtualenv

**Update**

Orientation will notify you automatically if a newer version is available (provided that there is an access to
the internet). To update, run again same command as for install.

**Run**

To run Orientation, start it from Unity Dash or Gnome Desktop Menu (whichever
desktop you use).

**Few more details, if you want**

Install process will install the indicator directly from the source code on GitHub.
`pip` basically clones the repo and builds and installs everything locally.

Just in case, you can as well run Orientation from command line: use `orientation`.

To uninstall Orientation and all files accompanying it, run
`sudo pip uninstall Orientation`.


# Development

## Project directory layout

- `bin/` - entry point scripts
- `icons/` - icons files used in runtime
- `drivers/` - .conf files for touch,pen,eraser,pad to force use of wacom driver
- `orientation_applet/` - root application package (all source code)
- `setup.py` - python packaging script
- `README.md` - this file

## Python 2 and Python 3

Current implementation runs on both Python 2.7 and Python 3. All
tests are as well executed on "both pythons".

**Reminder - release process**

1. Make changes, update and run tests, ensure good coverage
2. Update setup.py and change the version according to [semantic versioning](http://semver.org/)
3. Tag new version; tag format is 'vX.Y.Z'; e.g.: v1.2.1
4. Push changes and a new tag
