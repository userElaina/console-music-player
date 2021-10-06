import os
import sys
import time
import random
import logging
import subprocess

from userelaina.th import throws
from userelaina.pthc import Ls,Archive,col2str

_debug=True
_white='\x1b[0m'

error_codes={
	403:'Forbidden',
	405:'Method Not Allowed',
	415:'Unsupported Media Type',
}
# https://http.cat/

def f_time(x:float)->str:
	x=float(x)
	m=int(x/60)-1
	x-=m*60
	while x>=60:
		x-=60
		m+=1
	return '%d:%.2f'%(m,x)

def f_size(x:int)->str:
	x=int(x)
	if x<=1024:
		return str(x)
	i=-1
	while x>=1000:
		x/=1024
		i+=1
	return '%.2f%s'%(x,'KMGTPEZY'[i])

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
	'h':['help','wtf'],
	'cd':[],
	'pwd':[],
	'w':['i','info','who','whoami'],
	'clear':['cls'],
	'explorer':['open'],
	'exit':['quit'],
	'exec':['eval'],

	'ls':['ll'],
	'la':['dir','lla'],
	'lst':['list'],
	'his':['history'],

	'l':['left'],
	're':['repeat'],
	'r':['right'],
	'm':['mode'],

	'u':['up','update'],
	'rm':['del','delete','remove'],
	'add':['append'],

	'p':['pause'],
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
		try:
			l,r=x.split(':')
			l=int(l) if l else 0
			r=int(r) if r else _max
		except:
			return (0,0)
	else:
		try:
			l=int(x)
		except:
			return (0,0)
		r=l+1
	return (l,r)

_max=1<<10
_badpth='\\/:*?"<>|'
# DEBUG INFO WARNING ERROR CRITICAL

show_name={
	'history':'Music Playback History',
	'chosen':'Music Playlist',
	'dir':'Directory',
	'file':'File',
	'ans':'Music',
}

class Muz:
	def __init__(
		self,
		mode:str='rd',
		color_muz:str='y',
		color_highlight:str='c',
		color_pwd:str='g',
		color_err:str='r',
		log:str='muz.log',
		clk:float=0.1,
	):
		Archive().new(log)
		self.__log=logging.getLogger('muz')
		self.__log.setLevel(logging.DEBUG)
		handler_lg=logging.FileHandler(filename=log,encoding='utf8')
		handler_lg.setLevel(logging.DEBUG)
		handler_lg.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
		self.__log.addHandler(handler_lg)

		self.__ls=Ls()
		self.__ls.setcolor('muz',color_muz)
		self.__col_muz=col2str(color_muz)
		self.__col_highlight=col2str(color_highlight)
		self.__col_pwd=col2str(color_pwd)
		self.__col_err=col2str(color_err)

		self.__mode=f_mode(mode)
		self.__clk=clk

		self.__q=list() # wait list
		self.__n=-1 # No. __n music in __l is Playing
		self.__ss=0 # Next ffmpeg command -ss
		self.__now=dict()
		self.__his=list()

		self.__pause=False

	def sh(self,s:str)->str:
		self.__log.warning(s)
		s=subprocess.Popen(
			s,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT,
			encoding='utf8',
			errors='replace',
		)
		return s.stdout.read()

	def pt(self,s:str=None):
		if s:
			s=str(s)
			print('\r'+s+' '*(len(self.__ls.pwd())+2-len(s)))
		else:
			s='None...'
		self.__log.info(s)
		print('\r'+self.__col_pwd+self.__ls.pwd()+'#'+_white+' ',end='')
	
	def er(self,s:str,code:int)->str:
		s=str(s)
		_s=error_codes[code]+': '+s
		_ws=' '*(len(self.__ls.pwd())+2-len(_s))
		print('\r'+self.__col_err+error_codes[code]+_white+': '+s+_ws)
		self.__log.error(s)
		print('\r'+self.__col_pwd+self.__ls.pwd()+'#'+_white+' ',end='')


	def __pop(self)->str:
		while True:
			time.sleep(self.__clk)
			if self.__q:
				return self.__q.pop(0)

	def __play(self):
		pth=self.__pop()
		od='ffprobe -show_format "'+pth+'"'
		l=self.sh(od).split('\n')
		_flg=True

		while _flg:
			try:
				self.__now={
					'pth':pth,
					'format':l[5].split('=',1)[-1],
					'duration':float(l[7].split('=',1)[-1]),
					'size':f_size(l[8].split('=',1)[-1])+'B',
					'bit_rate':f_size(l[9].split('=',1)[-1])+'bps',
					'probe_score':l[10].split('=',1)[-1]+'pts',
					'start':time.time()-self.__ss,
				}
				_flg=False
			except:
				self.er(pth,415)
				self.__ls.delcho(pth)
				
				pth=self.__pop()
				od='ffprobe -show_format "'+pth+'"'
				l=self.sh(od).split('\n')
				_flg=True

		self.__his.append(pth)
		self.pt(self.__col_highlight+pth+_white)

		od='ffplay -nodisp -autoexit -hide_banner -loglevel quiet '
		if self.__ss:
			od+='-ss '+str(self.__ss)+' '
			self.__ss=0
		od+='"'+pth+'"'
		self.sh(od)


	def __always_q(self):
		while True:
			time.sleep(self.__clk)
			if self.__q or not self.__ls.lencho():
				continue
			if self.__mode=='loop':
				self.__n%=self.__ls.lencho()
			elif self.__mode=='cycle':
				self.__n=(self.__n+1)%self.__ls.lencho()
			else:
				self.__n=random.randint(0,self.__ls.lencho()-1)
			self.__q.append(self.__ls.getcho(self.__n))

	def __always_play(self):
		while True:
			time.sleep(self.__clk)
			if self.__pause or not self.__ls.lencho() or self.__t.is_alive():
				continue
			self.__t=throws(self.__play)


	def __kill(self):
		od='taskkill -f -im ffplay.exe'
		self.sh(od)


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

	def cmd_h(self):
		self.pt('https://github.com/userElaina/console-music-player/blob/main/README.md')

	def cmd_cd(self,s:str):
		if self.__ls.cd(s):
			self.pt('ParametersError: The system cannot find the path "'+str(s)+'" specified.')
		else:
			self.pt()

	def cmd_pwd(self):
		self.pt(self.__ls.pwd())

	def cmd_w(self):
		s=self.__mode+' '
		if not self.__now:
			s+='0 waiting'
			self.pt(s)
			return
		s+=str(len(self.__his))
		s+=' paused' if self.__pause else ' playing'
		self.pt(s)
		self.pt('\x1b[36m'+self.__now['pth']+'\x1b[0m')
		if self.__pause:
			_nw=self.__ss
		else:
			_nw=time.time()-self.__now['start']
		s=f_time(_nw)+'/'+f_time(self.__now['duration'])+' '
		s+=str(round(100*_nw/self.__now['duration'],2))+'%'
		self.pt(s)
		s=[self.__now['format'],self.__now['bit_rate'],self.__now['size'],self.__now['probe_score'],]
		s=' '.join(s)
		self.pt(s)


	def cmd_clear(self):
		print('\x1b[256F\x1b[0J',end='')
		self.pt()

	def cmd_explorer(self):
		self.sh('explorer "'+self.__ls.pth+'"')
		self.pt()

	def cmd_exit(self):
		self.__kill()
		sys.exit(0)

	def cmd_exec(self,s:str):
		if _debug:
			self.pt(repr(eval(s)))
		else:
			self.er('For developer debugging only.',403)

	def cmd_ls(self,k:str='ans',fullpath:bool=False):
		if k=='all':
			self.__ls.show(fullpath=fullpath)
			self.pt()
			return
		if k=='history':
			self.__ls.fxxkreg(reg=self.__his,regtag=show_name[k])
		else:
			self.__ls.setreg(k=k)
			self.__ls.fxxkreg(reg=None,regtag=show_name[k])
		s=self.__ls.showreg(k=show_name[k],fullpath=fullpath)
		if self.__now:
			s=s.replace(self.__col_muz+self.__now['pth'],self.__col_highlight+self.__now['pth'])
		print(s,end='')
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
		if self.__now:
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
		if self.__pause:
			if taskkill:
				self.__ss=0
			self.__pause=False
			self.pt('restart')
		else:
			self.cmd_re()
			if self.__now and not taskkill:
				self.__ss=max(0,time.time()-self.__now['start']-self.__clk)
			else:
				self.__ss=0
			self.__pause=True
			self.pt('pause')

	def cmd_jmp_str(self,command:str)->str:
		pth=os.path.join(self.__ls.pwd(),command)
		if os.path.exists(pth):
			if os.path.isfile(pth):
				return pth
		if os.path.exists(command):
			if os.path.isfile(command):
				return command
		return None

	def cmd_jmp_int(self,x:int)->str:
		try:
			x=int(x)
			return self.__ls.getcho(x)
		except:
			return None

	def cmd_jmp(self,command:str):
		pth=self.cmd_jmp_int(command)
		if pth is None:
			pth=self.cmd_jmp_str(command)
		if pth is not None:
			self.__q=[pth,]+self.__q
			return 1
		else:
			return None


	def cmd(self,command:str):
		self.__log.debug(command)
		taskkill='+' in command
		x=_splitcmd(command)
		self.__log.debug(str(x))

		if x[0]=='':
			self.pt()
		elif x[0].startswith('qwq') or x[0] in ('owo','qaq','quq','qvq','tat','0w0'):
			self.cmd_qwq(x[0])

		elif x[0]=='h':
			self.cmd_h()

		elif x[0]=='cd':
			try:
				k=int(x[1])
			except:
				k=x[1]
			self.cmd_cd(k)

		elif x[0]=='pwd':
			self.cmd_pwd()
		elif x[0]=='w':
			self.cmd_w()
		elif x[0]=='clear':
			self.cmd_clear()
		elif x[0]=='explorer':
			self.cmd_explorer()

		elif x[0]=='exit':
			self.cmd_exit()
		elif x[0]=='exec':
			self.cmd_exec(x[1])

		elif x[0] in ('ls','la','lst','his','ld','lf'):
			full='full' in x[1]
			if x[0]=='lst' or 'lst' in x[1] or 'list' in x[1]:
				k='chosen'
			elif x[0]=='his' or 'his' in x[1]:
				k='history'
			elif x[0]=='lf' or 'file' in x[1]:
				k='file'
			elif x[0]=='ld' or 'dir' in x[1]:
				k='dir'
			elif x[0]=='la' or 'al' in x[1]:
				k='all'
			else:
				k='ans'
			self.cmd_ls(k,full)

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
			elif x[0]=='add':
				self.cmd_add(l,r)

		elif x[0]=='p':
			self.cmd_p(taskkill=taskkill)
			taskkill=self.__pause

		else:
			if self.cmd_jmp(command):
				taskkill=True
			else:
				self.er(command,405)

		if taskkill:
			self.__kill()

	def join(self):
		_s=lambda x:str(x)+(' '*(3-len(str(x))))
		if not self.sh('where ffplay'):
			self.pt('Please add ffplay to the PATH or where you want to run this program.')
			self.cmd_exit()
		self.cmd_clear()
		self.pt('Windows Muz')
		self.pt('Copyright (C) userElaina. All rights reserved.')
		self.pt(' ')
		self.pt('Get the source  https://github.com/userElaina/console-music-player')
		self.pt(' ')
		self.cmd_u()
		self.__t=throws(self.__play)
		self.__mian=[throws(self.__always_q),throws(self.__always_play)]
		while True:
			command=input().strip()
			self.cmd(command=command)
