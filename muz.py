import os
import sys
from random import choice
from time import sleep as slp
from os import system as sh
import downs
import threading

_ext=['mp3','wav','flac']

_f=[i for i in os.listdir() if os.path.isfile(i) and [None for j in _ext if i.lower().endswith('.'+j)]]

bg=choice(_f)
loop1=False
random1=True

for i in sys.argv[1:]:
	try:
		bg=os.path.basename(i)
		# print(i)
	except:
		if i=='loop':
			loop1=True
		elif i=='seq' or i=='norandom':
			random1=False

if loop1:
	_l=[bg,]
	random1=True
else:
	_l=_f.copy()
	_l.remove(bg)
	_l=_l+[bg,]

g_reg=None
g_rn=0
def g1():
	global g_reg,g_rn
	ans=g_reg if g_reg else (choice(_l) if random1 else _l[g_rn])
	g_reg=None
	g_rn=(g_rn+1)%len(_l)
	return ans

def play(pth:str):
	print('\033[1;33m'+os.path.abspath(pth)+'\033[0m')
	od='ffplay -nodisp -autoexit -hide_banner -loglevel quiet "'+pth+'"'
	sh(od)

t=downs.throws(play,g1())
def mian():
	global t
	while True:
		if not t.is_alive():
			t=downs.throws(play,g1())
		slp(1)
downs.throws(mian)

while True:
	ipt=input()
	taskkill='+' not in ipt
	ipt=ipt.replace('+','')

	if ipt in {'nx','r','next'}:
		if loop1:
			_l=[choice(_f),]
	elif os.path.isfile(ipt):
		g_reg=ipt
	else:
		taskkill=False

	if ipt=='?':
		ans='one' if loop1 else (
			'random' if random1 else 'seq'
		)
		print(ans)

	if taskkill:
		sh('taskkill -f -im ffplay.exe')
