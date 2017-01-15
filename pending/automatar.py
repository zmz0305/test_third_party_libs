import os
import logging
import fileinput
import fnmatch

script_dir_path = os.path.dirname(os.path.realpath(__file__))
LOCAL_PYTHON = 'basepython=/Users/zmz0305/workspace/OneDrive/workplace/research/install-python/bin/python3'

class cd:
	def __init__(self, path):
		self.new_path = os.path.expanduser(path)

	def __enter__(self):
		self.saved_path = os.getcwd()
		os.chdir(self.new_path)

	def __exit__(self, etype, value, traceback):
		os.chdir(self.saved_path)

def download(path):
	os.system("git clone " + path)

def init_repos():
	with open("repos.txt") as lines:
		for line in lines:
			download(line)


def add_local_python_path(file):
	has_basepython = False
	with open(file) as f:
		for line in f:
			if 'basepython' in line:
				has_basepython = True
				break
	# with fileinput.input(file) as lines:
	with fileinput.input(file, inplace=True, backup='.bak') as lines:
		for line in lines:
			if not has_basepython:
				print(line.replace('[testenv]', '[testenv]\n'+LOCAL_PYTHON), end='')
			elif 'basepython' in line:
				print(line.replace(line, LOCAL_PYTHON))
			else:
				print(line)

def find_files(path, filter):
	for root, dirs, files in os.walk(path):
		for file in fnmatch.filter(files, filter):
			yield os.path.join(root, file)

def find_dirs(path, depth):
	startinglevel = path.count(os.sep)
	for root, dirs, files in os.walk(path):
		level = root.count(os.sep) - startinglevel
		for dir in dirs:
			if level < 1:
				yield os.path.join(root, dir)

def run_tox_tests():
	print(script_dir_path)
	for file in find_files(script_dir_path, 'tox.ini'):
		print(file)
		add_local_python_path(file)
	for dir in find_dirs(script_dir_path, ''):
		print(dir)
		with cd(dir):
			os.system('tox -e py3.6 > test_res_mod.txt')


def runner():
	init_repos()
	run_tox_tests()

runner()



