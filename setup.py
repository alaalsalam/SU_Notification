from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in sunotification/__init__.py
from sunotification import __version__ as version

setup(
	name="sunotification",
	version=version,
	description="sunotification",
	author="sunotify",
	author_email="sunotify@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
