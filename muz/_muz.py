import os
import sys
import time
import random
import logging

from userelaina.th import throws
from userelaina.pthc import Ls,Archive,col2str

_debug=True
_white='\x1b[0m'

d_mode={
	'random':['rd'],
	'cycle':[],
	'loop':['lp'],
}
for i in d_mode:
	d_mode[i]+=[i,i[0],i[:2]]

def f_mode(x:str,dft:str='random')->str:
	for i in d_mode:
		if x in d_mode[i]:
			return i
	return dft

d_command={
	'pwd':[],
	'w':['info','i'],
	'clear':['cls'],

	'ls':['ll'],
	'la':['dir','lla'],
	'lst':['list'],
	'his':['history'],

	'cd':[],

	'l':['left'],
	're':[],
	'r':['right'],
	'm':['mode'],

	'u':['up','update'],
	'rm':['del','delete','remove'],
	'add':['append'],

	'p':['pause'],
	'exit':[],
	'exec':[],
}
for i in d_command:
	d_command[i].append(i)

def _splitcmd(x:str)->tuple:
	x=x.replace('+','').strip().split(' ',1)+['',]
	x1=x[0].strip().lower()
	x2=x[1].strip()
	for i in d_command:
		if x1 in d_command[i]:
			return (i,x2)
	return (x1,x2)

def _splitlr(x:str)->tuple:
	if not x:
		return (0,_max)
	x=x.replace(' ',':')
	if ':' in x:
		l,r=x.split(':')
		l=int(l) if l else 0
		r=int(r) if r else _max
	else:
		l=int(x)
		r=l+1
	return (l,r)

_max=1<<10
_badpth='\\/:*?"<>|'
# DEBUG INFO WARNING ERROR CRITICAL

class Muz:
	def __init__(
		self,
		mode:str='rd',
		color_muz:str='y',
		color_highlight:str='c',
		color_pwd:str='g',
		log:str='muz.log',
	):
		Archive().new(log)
		self.__log=logging.getLogger('muz')
		self.__log.setLevel(logging.DEBUG)
		handler_lg=logging.FileHandler(filename=log,encoding='utf8')
		handler_lg.setLevel(logging.DEBUG)
		handler_lg.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
		self.__log.addHandler(handler_lg)

		self.__clk=1

		self.__mode=f_mode(mode)

		self.__ls=Ls()
		self.__ls.setcolor('muz',color_muz)
		self.__col_muz=col2str(color_muz)
		self.__col_highlight=col2str(color_highlight)
		self.__col_pwd=col2str(color_pwd)

		self.__q=list() # wait list
		self.__n=-1 # No. __n music in __l is Playing
		self.__his=list()

		self.__pause=False

	def sh(self,s:str)->int:
		self.__log.warning(s)
		s='('+s+') 1>nul 2>nul'
		return os.system(s)

	def pt(self,s:str=None):
		if s:
			s=str(s)
			print('\r'+s+' '*(len(self.__ls.pwd())+2-len(s)))
		else:
			s='None...'
		self.__log.info(s)
		print('\r'+self.__col_pwd+self.__ls.pwd()+'#'+_white+' ',end='')

	def __play(self):
		pth=self.__get1()
		self.__his.append(pth)
		self.pt(self.__col_highlight+pth+_white)
		od='ffplay -nodisp -autoexit -hide_banner -loglevel quiet "'+pth+'"'
		self.sh(od)

	def __kill(self):
		od='taskkill -f -im ffplay.exe'
		self.sh(od)

	def __always(self):
		while True:
			while self.__pause or not self.__ls.lencho() or self.__t.is_alive():
				time.sleep(self.__clk)

			self.__t=throws(self.__play)


	def __get1(self)->str:
		if self.__q:
			return self.__q.pop(0)

		while not self.__ls.lencho():
			time.sleep(self.__clk)
		if self.__mode=='loop':
			self.__n%=self.__ls.lencho()
		elif self.__mode=='cycle':
			self.__n=(self.__n+1)%self.__ls.lencho()
		else:
			self.__n=random.randint(0,self.__ls.lencho()-1)
		return self.__ls.getcho(self.__n)


	def cmd_qwq(self,s:str):
		if s=='qwq':
			s='QwQ'
		elif s=='owo':
			s='OwO'
		elif s=='qaq':
			s='QAQ'
		elif s=='quq':
			s='QuQ'
		elif s=='qvq':
			s='QvQ'
		elif s=='tat':
			s='TAT'
		elif s=='0w0':
			s='0w0'
		else:
			s='QωQ'
		self.pt(s)

	def cmd_pwd(self):
		self.pt(self.__ls.pwd())

	def cmd_w(self):
		s=self.__mode+' '
		if self.__his:
			s+=str(len(self.__his))
			s+=' paused' if self.__pause else ' playing'
			self.pt(s)
			self.pt('\x1b[36m'+self.__his[-1]+'\x1b[0m')
		else:
			s+='0 waiting'
			self.pt(s)

	def cmd_clear(self):
		print('\x1b[256F\x1b[0J',end='')
		self.pt()

	def cmd_ls(self,k:str='ans',fullpath:bool=False):
		if k=='all':
			self.__ls.show(fullpath=fullpath)
			self.pt()
			return
		if k=='history':
			k='Music Playback History '
			self.__ls.fxxkreg(self.__his,k)
		if k=='chosen':
			self.__ls.setreg(k=k)
			k='Music Playlist '
			self.__ls.fxxkreg(reg=None,regtag=k)
		s=self.__ls.showreg(k=k,fullpath=fullpath)
		if self.__his:
			s=s.replace(self.__col_muz+self.__his[-1],self.__col_highlight+self.__his[-1])
		print(s,end='')
		self.pt()

	def cmd_cd(self,s:str):
		if self.__ls.cd(s):
			self.pt('ParametersError: The system cannot find the path "'+str(s)+'" specified.')
		else:
			self.pt()

	def cmd_l(self):
		self.__q=self.__his[-2:_max]+self.__q
		self.pt()

	def cmd_re(self):
		self.__q=self.__his[-1:_max]+self.__q
		self.pt()

	def cmd_r(self):
		if self.__mode=='loop':
			self.__n+=1
		self.pt()

	def cmd_m(self,mode:str):
		if mode!=self.__mode:
			self.__mode=mode
		self.pt()	

	def cmd_u(self):
		_l=self.__ls.setcho('ans')
		if self.__his:
			self.pt('updated to '+str(_l)+' music')
		else:
			self.pt()

	def cmd_rm(self,l:int,r:int):
		_l=self.__ls.uncho(l,r)
		self.pt('remove '+str(_l)+' music')

	def cmd_add(self,l:int,r:int):
		_l=self.__ls.addcho('ans',l,r)
		self.pt('append '+str(_l)+' music')


	def cmd_p(self,taskkill:bool):
		self.__pause=~self.__pause
		if taskkill:
			self.cmd_re()
		self.pt('pause...' if self.__pause else 'restart')

	def cmd_exit(self):
		self.__kill()
		sys.exit(0)

	def cmd_exec(self,s:str):
		if _debug:
			self.pt(repr(eval(s)))
		else:
			self.pt('PermissionDenied: exec')


	def cmd(self,command:str):
		self.__log.debug(command)
		taskkill='+' in command
		x=_splitcmd(command)
		self.__log.debug(str(x))

		if x[0]=='':
			self.pt()
		elif x[0].startswith('qwq') or x[0] in ('owo','qaq','quq','qvq','tat','0w0'):
			self.cmd_qwq(x[0])

		elif x[0]=='pwd':
			self.cmd_pwd()
		elif x[0]=='w':
			self.cmd_w()
		elif x[0]=='clear':
			self.cmd_clear()

		elif x[0] in ('ls','la','lst','his','ld','lf'):
			full='full' in x[1]
			if x[0]=='lst':
				k='chosen'
			elif x[0]=='his':
				k='history'
			elif x[0]=='lf' or 'file' in x[1]:
				k='file'
			elif x[0]=='ld' or 'dir' in x[1]:
				k='dir'
			elif x[0]=='la' or 'al' in x[1]:
				k='all'
			else:
				k='music'
			self.cmd_ls(k,full)

		elif x[0]=='cd':
			try:
				k=int(x[1])
			except:
				k=x[1]
			self.cmd_cd(k)

		elif x[0]=='l':
			self.cmd_l()
		elif x[0]=='re':
			self.cmd_re()
		elif x[0]=='r':
			self.cmd_r()
		elif x[0]=='m':
			self.cmd_m(f_mode(x[1]))

		elif x[0]=='u':
			self.cmd_u()
		elif x[0] in ('rm','add'):
			l,r=_splitlr(x[1])
			if x[0]=='rm':
				self.cmd_rm(l,r)
			else:
				self.cmd_add(l,r)

		elif x[0]=='p':
			self.cmd_p(taskkill=taskkill)
		elif x[0]=='exit':
			self.cmd_exit()
		elif x[0]=='exec':
			self.cmd_exec(x[1])
			

		else:
			_flg=command
			command=os.path.join(self.__ls.pwd(),command)
			if os.path.exists(command):
				if os.path.isfile(command):
					_flg=None
					self.__q.append(os.path.abspath(command))
			if _flg:
				command=_flg
				if os.path.exists(command):
					if os.path.isfile(command):
						_flg=None
						self.__q.append(os.path.abspath(command))
			if _flg:
				self.pt('MuzCommandNotFound: '+x[0])
			else:
				self.pt('append 1 music')

		if taskkill:
			self.__kill()

	def join(self):
		_s=lambda x:str(x)+(' '*(3-len(str(x))))
		if self.sh('where ffplay'):
			self.pt('Please add ffplay to the PATH or where you want to run this program.')
			self.cmd_exit()
		self.cmd_clear()
		self.pt('Windows Muz')
		self.pt('Copyright (C) userElaina. All rights reserved.')
		self.pt(' ')
		self.pt('Try the new Muz  https://github.com/userElaina/console-music-player')
		self.pt(' ')
		self.cmd_u()
		self.__t=throws(self.__play)
		self.__mian=throws(self.__always)
		while True:
			command=input().strip()
			self.cmd(command=command)
