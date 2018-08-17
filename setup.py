from setuptools import setup

import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('barracks/barracks.py', 'rb') as f:
	version = str(ast.literal_eval(_version_re.search(
		f.read().decode('utf-8')).group(1)))


setup(
	name='barracks',
	packages=['barracks'],
	version=version,
	description='Simple file storing util for reading & writing series of data for data mining',
	license='MIT',

	author='Youngsoo Lee',
	author_email='0soo.2@prev.kr',
	
	url='https://github.com/Prev/barracks',
	keywords=['barracks', 'file-storage', 'data-mining'],

	install_requires=[
		'lz4>=2.1.0',
	],

	classifiers=(
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	),

)
