from setuptools import setup

# setup.py file for the package
setup(
  name='churchtools-song-checker',
  version='1.0.0',
  packages=['ct-song-checker'],
  python_requires='>3.9.1',
  install_requires=[
    'requests',
    'datetime',
    'os',
    'dotenv'
  ],
  entry_points={
    'console_scripts': [
      'ct-song-checker = songchecker.py.__main__:main'
    ]
  },
  author='Gifhorner Friedenskirche'
)

