from setuptools import setup

setup(
  name='snapcastr',
  packages=['snapcastr'],
  include_package_data=True,
  install_requires=[ 'flask', 'flask_bootstrap', 'flask_nav', 'flask-wtf', 'snapcast', 'wtforms']
)
