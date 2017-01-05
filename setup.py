#!/usr/bin/python3

import os
from distutils.core import setup

from orientation_applet.resource import RESOURCES_DIRECTORY_PATH


def find_resources(resource_dir):
    target_path = os.path.join(RESOURCES_DIRECTORY_PATH, resource_dir)
    resource_names = os.listdir(resource_dir)
    resource_list = [os.path.join(resource_dir, file_name) for file_name in resource_names]
    return (target_path, resource_list)


setup(name="Orientation",
      version="1.0.0",
      description="Auto Orientation Indicator for Ubuntu on Surface",
      url='https://github.com/vguywithabowtie/orientation',
      author='VirtualGuywithaBowTie',
      author_email='mr.jefedavis@gmail.com',
      license='GNU',
      packages=["orientation_applet"],
      data_files=[
          ('/usr/share/applications', ['orientation.desktop']),
          find_resources("icons/light"),
          find_resources("icons/dark")],
      scripts=["bin/orientation"]
)
