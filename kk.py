#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
kill me baby - karuta
"""

import sys,os
import time
import random
from multiprocessing import Process,Pipe

def timeup(conn,fileno):
	for i in range(11):
		sys.stdout.write("\rtime:"+str(10-i).zfill(2)+" ans: ")
		sys.stdout.flush()
		time.sleep(1)

	if i==10:
		print ""
		conn.send("t")

def getans(conn,fileno):
	sys.stdin=os.fdopen(fileno)
	ans=raw_input()
	conn.send(ans)

def makeq():
	titles=[]
	for i in open('title.txt','r'):
		titles.append(i.strip().split(','))
	qr=[-1]*3
	i=0
	while(i<3):
		tmp=random.randint(0,12)
		if not(tmp in qr):
			qr[i]=tmp
			i+=1
	a=random.randint(0,2)

	print titles[qr[a]][0]
	print "0)%s 1)%s  2)%s" % (titles[qr[0]][1],titles[qr[1]][1],titles[qr[2]][1])
	print ""
	print "enter 0-2 (or q to quit)"
	print ""

	return [a,titles[qr[a]][1]]


def kk(combo):
	cor=makeq()
	p_c,c_c=Pipe()
	p={}
	ans=''
	p[0] = Process(target=timeup,args=(c_c,sys.stdin.fileno()))
	p[1] = Process(target=getans,args=(c_c,sys.stdin.fileno()))
	for i in range(len(p)):
		p[i].start()
	while not(ans=='0' or ans=='1' or ans=='2' or ans=='q' or ans=='t'):
		ans=p_c.recv()
	for i in range(len(p)):
		p[i].terminate()

	if ans=='t':
		print "time up! Answer is "+cor[1]
		print "-----------------"
		return 0
	elif ans=='q':
		print "Bye!"
		quit()
	else:
		if int(ans) == cor[0]:
			combo+=1
			print "Right!   "+str(combo)+" combo!"
			print "-----------------"
			return combo
		else:
			print "No! Answer is "+cor[1]
			print "-----------------"
			return 0

if __name__=='__main__':
	print "\nKill me Karuta\n"
	time.sleep(1)
	combo=0
	while(True):
		combo=kk(combo)
		time.sleep(1.5)