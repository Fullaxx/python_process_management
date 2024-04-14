#!/usr/bin/env python3
#
# https://docs.python.org/3/library/subprocess.html
# https://realpython.com/python-subprocess/
# https://techclaw.org/python-subprocess-run-a-comprehensive-guide/
# https://www.simplilearn.com/tutorials/python-tutorial/subprocess-in-python

#import os
#import sys
import time
import signal
import datetime
import subprocess

g_shutdown = False

def signal_handler(sig, frame):
	global g_shutdown
	g_shutdown = True

# https://stackoverflow.com/questions/2760652/how-to-kill-or-avoid-zombie-processes-with-subprocess-module#:~:text=The%20python%20runtime%20takes%20responsibility,poll%20or%20terminate%20on%20it.
# The python runtime takes responsibility for getting rid of zombie process once their process objects have been garbage collected.
# If you see the zombie lying around it means you have kept a process object and not called wait, poll or terminate on it

# using the watch_zombies.sh script, it would appear that this function will leave zombies... sometimes??
def launch_child_shell(l, d, s):
	p = subprocess.Popen(f'./sleep.sh {s}', shell=True, start_new_session=True, stdin=None, stdout=None, stderr=None, close_fds=True)
	if l is not None:
		l.append(p)
	if d is not None:
		t = datetime.datetime.utcnow().timestamp()
		d[t] = p

# using the watch_zombies.sh script, it would appear that this function will leave zombies... sometimes??
def launch_child_noshell(l, d, s):
	p = subprocess.Popen(['./sleep.sh', f'{s}'], shell=False, start_new_session=True, stdin=None, stdout=None, stderr=None, close_fds=True)
	if l is not None:
		l.append(p)
	if d is not None:
		t = datetime.datetime.utcnow().timestamp()
		d[t] = p

def launch_children(l, d, n, sleep_time):
	for i in range(0, n):
		launch_child_shell(l, d, sleep_time)
		launch_child_noshell(l, d, sleep_time)

def cleanup(l, d):
	if l:
		for i,p in enumerate(l):
			p.terminate()
#			print(i, p)

	if d:
		for k,p in d.items():
			p.terminate()
#			print(k, p)

if __name__ == "__main__":
#	l = []
	l = None
	d = None
#	d = {}

	signal.signal(signal.SIGINT,  signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)
	signal.signal(signal.SIGQUIT, signal_handler)

	while not g_shutdown:
		launch_children(l, d, 30, 4)
		time.sleep(5)

	cleanup(l, d)
