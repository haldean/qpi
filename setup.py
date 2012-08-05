from setuptools import setup, find_packages

setup(
    name='qpi',
    version='0.1',
    license='MIT License',
    url='https://github.com/haldean/qpi',
    long_description=open('README.md').read(),

    author='Will Haldean Brown',
    author_email='will.h.brown@gmail.com',

    packages = find_packages(),
    scripts = ['qpi/qpi.py'],

    install_requires = [
      'argparse',
      'flask',
      'gdata',
      ],

    package_data = {
      '': ['README.md',],
      'qpi': ['static', 'templates'],
      }
    )
