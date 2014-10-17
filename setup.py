import string
from setuptools import setup, find_packages

from datetime import datetime

version = datetime.now().strftime("0.1dev.%Y%m%d.%H%M")

setup(
    name='django-stashboard',
    version=version,
    packages=find_packages(exclude=["demo", "scripts", "tests"]),
    author='Gary Reynolds',
    author_email='gary.j.reynolds@det.nsw.edu.au',
    description='Fork of Stashboard (GAE) modified for pure-django.',
    url='https://github.com/goodtune/django-stashboard',
    install_requires=map(string.strip, open('requirements.txt').readlines()),
    include_package_data=True,
    zip_safe=False,
)
