#!/usr/bin/env python
import subprocess
import multiprocessing
from multiprocessing import *
import os
import sys
import re
import reconf
from reconf import *
import time
from functools import wraps
import argparse
import ipaddr
import nmapxml
from nmapxml import *
from threading import Thread
import functools

parser = argparse.ArgumentParser(description='Run a short or verbose dirb scan')
parser.add_argument('-ip', action='store', required=True, help='IP Address to be assessed')
parser.add_argument('-s', action='store', required=True, help='Service')
parser.add_argument('-a', action='store_true', required=False, help='ALL')
parser.add_argument('-hy', action='store_true', required=False, help='hydra')
parser.add_argument('-n', action='store_true', required=False, help='ncrack')
parser.add_argument('-m', action='store_true', required=False, help='medusa')

args = parser.parse_args()
try:
        ip_address = ipaddr.IPAddress(args.ip)
except:
        print "Try again..."
        sys.exit()

stype = args.s

def timeout(timeout):
	def deco(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, timeout))]
			def newFunc():
				try:
					res[0] = func(*args, **kwargs)
				except Exception, e:
					res[0] = e
			t = Thread(target=newFunc)
			t.daemon = True
			try:
				t.start()
				t.join(timeout)
			except Exception, je:
				print 'error starting thread'
				raise je
			ret = res[0]
			if isinstance(ret, BaseException):
				raise ret
			return ret
		return wrapper
	return deco	

@timeout(60)
def chkcreds(EXECMD):
    	subprocess.call(EXECMD, shell=True)

if args.a is True or args.m is True and args.hy is False and args.n is False:
	medusasrv = ['csv','ftp','http','imap','mssql','mysql','nntp','pcanywhere','pop3','postgres','rexec','rlogin','rsh','smb','smtp','snmp','ssh','svn','telnet','vmauthd','vnc','web']
	if stype in medusasrv:
	        outfile = "%s/%s_%s_medusa.txt" % (reconf.rsltpth, ip_address, stype)
		MEDUSA = "medusa -h %s -U %s -P %s -O %s -e ns -v 4 -M %s" % (ip_address, reconf.usrlst, reconf.pwdlst, outfile, stype)
		print "\033[1;31m[>]\033[0;m Executing %s" % MEDUSA
		chkcreds(MEDUSA)
		sys.exit(0)

if args.a is True or args.n is True and args.hy is False and args.m is False:
	ncracksrv = ['ftp', 'ssh', 'telnet', 'http', 'pop3', 'smb', 'rdp', 'vnc']
	if stype in ncracksrv:
	        outfile = "%s/%s_%s_ncrack.txt" % (reconf.rsltpth, ip_address, stype)
		NCRACK = "ncrack -p %s -u %s -p %s -T4 -oA %s %s" % (stype, reconf.usrlst, reconf.pwdlst, outfile, ip_address)
		print "\033[1;31m[>]\033[0;m Executing %s" % NCRACK 
		chkcreds(NCRACK)
		sys.exit(0)

if args.a is True or args.hy is True and args.n is False and args.m is False:
	hydrasrv = ['cisco', 'cisco-enable', 'cvs', 'firebird', 'ftp', 'ftps', 'http', 'icq', 'imap', 'irc', 'ldap2', 'ldap3', 'mssql', 'mysql', 'nntp', 'oracle-listener', 'oracle-sid', 'pcanywhere', 'pcnfs', 'pop3', 'postgres', 'rdp', 'redis', 'rexec', 'rlogin', 'rsh', 's7', 'sip', 'smb', 'smtp', 'smtp-enum', 'snmp', 'socks5', 'ssh', 'sshkey', 'svn', 'teamspeak', 'telnet', 'vmauthd', 'vnc', 'xmpp']
	if stype in hydrasrv:
	        outfile = "%s/%s_%s_hydra.txt" % (reconf.rsltpth, ip_address, stype)
		HYDRA = "hydra -L %s -P %s -q -e ns -o %s %s %s" % (reconf.usrlst, reconf.pwdlst, outfile, ip_address, stype)
		chkcreds(HYDRA)
