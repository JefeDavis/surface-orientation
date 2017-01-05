import json
import pkg_resources

try:
	from urllib2 import urlopen
except ImportError:
	from urllib.request import urlopen


def is_update_available():
	current_version = _current_version()
	latest_version = _latest_version()
	return current_version is not None \
		and latest_version is not None \
		and current_version != latest_version


def _current_version():
	try:
		version = u'v%s' % pkg_resources.get_distribution("Orientation").version
	except pkg_resources.DistributionNotFound:
		version = None
	return version


def _latest_version():
	try:
		response = urlopen('https://api.github.com/repos/virtualguywithabowtie/surface-orientation/tags')
		raw_json = response.read().decode('ascii')
		tags = json.loads(raw_json)
		latest_version = [tag['name'] for tag in tags][0]
	except:
		latest_version = None
	return latest_version
