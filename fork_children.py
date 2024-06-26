#!/usr/bin/env python3
#
# https://docs.python.org/3/library/os.html
# https://sigterm.sh/2012/08/22/forking-background-processes-in-python/

# python exit vs sys.exit
# https://stackoverflow.com/questions/6501121/difference-between-exit-and-sys-exit-in-python

import os
import sys
import time
import signal
import subprocess

g_shutdown = False

#def child_reaper(sig, frame):
#	os.waitpid(-1, os.WNOHANG)

def quit_handler(sig, frame):
	global g_shutdown
	g_shutdown = True

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def bailmsg(*args, **kwargs):
	eprint(*args, **kwargs)
	sys.exit(1)

def child_activity_popen(s):
#	Configure the child processes environment
#	os.chdir("/")
	os.setsid()
	os.umask(0)

	p = subprocess.Popen(f'./sleep.sh {s}', shell=True, start_new_session=True, stdin=None, stdout=None, stderr=None, close_fds=True)
	p.wait()

def child_activity_system(s):
#	Configure the child processes environment
#	os.chdir("/")
	os.setsid()
	os.umask(0)

#	Execute something in the background
	try:
		os.system(f'./sleep.sh {s}')
	except (OSError, e):
		bailmsg(f'system failed: {e.errno} ({e.strerror})')

def fork_child(s):
	try:
		pid = os.fork()
#		Parent Check
		if pid > 0: return
	except (OSError, e):
#		print >> sys.stderr, "fork failed: %d (%s)" % (e.errno, e.strerror)
		bailmsg(f'fork failed: {e.errno} ({e.strerror})')

	child_activity_system(s)
#	child_activity_popen(s)
	sys.exit(0)

def fork_children(n, s):
	for i in range(0, n):
		fork_child(s)

if __name__ == "__main__":
	signal.signal(signal.SIGINT,  quit_handler)
	signal.signal(signal.SIGTERM, quit_handler)
	signal.signal(signal.SIGQUIT, quit_handler)

#	https://stackoverflow.com/questions/38775178/how-to-avoid-defunct-processes-with-python-fork
#	https://mail.python.org/pipermail/tutor/2003-December/026748.html
#	signal.signal(signal.SIGCHLD, child_reaper)
	signal.signal(signal.SIGCHLD, signal.SIG_IGN)

	while not g_shutdown:
		fork_children(30, 4)
		time.sleep(5)
