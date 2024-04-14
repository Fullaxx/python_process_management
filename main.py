#!/usr/bin/env python3
#
# https://docs.python.org/3/library/subprocess.html
# https://realpython.com/python-subprocess/
# https://techclaw.org/python-subprocess-run-a-comprehensive-guide/
# https://www.simplilearn.com/tutorials/python-tutorial/subprocess-in-python

#import os
#import sys
import time
import subprocess

def launch_child_shell():
	p = subprocess.Popen('./sleep.sh 4', shell=True, start_new_session=True, stdin=None, stdout=None, stderr=None, close_fds=True)

def launch_child_noshell():
	p = subprocess.Popen(['./sleep.sh', '4'], shell=False, start_new_session=True, stdin=None, stdout=None, stderr=None, close_fds=True)

def launch_children(children):
	for i in range(0, children):
		launch_child_shell()
		launch_child_noshell()

if __name__ == "__main__":
	while True:
		launch_children(20)
		time.sleep(5)
