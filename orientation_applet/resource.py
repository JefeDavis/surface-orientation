from os.path import join, dirname, isfile

RESOURCES_DIRECTORY_PATH = "/usr/share/orientation"

__RELATIVE_RESOURCE_PATH = join(dirname(dirname(__file__)))
__CURRENT_RESOURCES_PATH = \
	__RELATIVE_RESOURCE_PATH \
	if isfile(join(__RELATIVE_RESOURCE_PATH, "bin", "orientation_applet")) else \
		RESOURCES_DIRECTORY_PATH


def image_path(name, theme):
	"""Returns path to the image file by its name, in given theme library"""
	return join(__CURRENT_RESOURCES_PATH, "icons", theme, "%s.svg" % name)
