import os
import re
import time
import random

from userelaina.cls import *
from userelaina.th import throws

d_mode={
	'rd':['ra','random'],
	'cy':['cycle'],
	'lp':['loop','lo'],
}
for i in d_mode:
	d_mode[i].append(i)

def f_mode(x:str,dft:str='rd')->str:
	for i in d_mode:
		if x in d_mode[i]:
			return i
	return dft

d_order={
	'r':['right'],
	'l':['left'],
	're':[],
	'up':['u','update'],
	
	'p':['pause'],
	'm':['mode'],
	'exit':[],

	'll':['ls'],
	'cd':[],
	'list':['lst'],
	'i':['info'],
	'his':['history'],

	'rm':['del','delete','remove'],
	'add':['append'],
}
for i in d_order:
	d_order[i].append(i)

def f_order(x:str)->str:
	for i in d_order:
		if x in d_order[i]:
			return i
	return str(x)

'DEBUG INFO WARNING ERROR CRITICAL'

class nMuz:
	def __init__(
		self,
		clk:float=1,
		mode:str='rd',
		color:str='y',
	):
		_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'logs')
		if not os.path.exists(_dir):
			os.mkdir(_dir)
		self.__logpth=os.path.join(_dir,'muz.log')
		self.__regpth=os.path.join(_dir,'muz-register.txt')
		self.__errpth=os.path.join(_dir,'muz-errs.txt')
		self.__warnpth=os.path.join(_dir,'muz-warn.txt')
		self.__log=Log(self.__logpth)

		self.__clk=clk
		self.__mode=f_mode(mode)

		self.__ls=Ls()
		self.__ls.paint('muz',color)

		self.__q=list()
		self.__nwn=-1

		self.__his=list()
		self.__pause=False
		self.__ed=False

	def lg(self,s:str,hd:str='log',):
		hd=str(hd)
		hd+=' '*(8-len(hd))
		s=re.sub('[\r]*\033\\[[0-9]+m','',str(s))
		self.__log.lg(hd+str(s))

	def pt(self,s:str=None):
		if s:
			s=str(s)
			print('\r'+s)
		else:
			s='None...'
		print('\r\033[32m'+self.__ls.get_pth()+'#\033[0m ',end='')
		self.lg(s,'INFO')

	def __play(self):
		while not len(self.__l):
			time.sleep(self.__clk)
		pth=self.__get1()
		self.__his.append(pth)
		self.pt('\033[36m'+pth+'\033[0m')
		# od='ffplay -nodisp -autoexit -hide_banner -loglevel quiet "'+pth+'" > 1.txt'
		od='ffplay -nodisp -autoexit -hide_banner -loglevel warning "'+pth+'" > "'+self.__warnpth+'"'
		self.lg(od,'WARNING')
		open(self.__warnpth,'wb')
		os.system(od)
		s=open(self.__warnpth,'r').read().strip()
		if len(s):
			self.lg(s,'ERROR')

	def __kill(self):
		od='taskkill -f -im ffplay.exe 2>"'+self.__errpth+'" > "'+self.__regpth+'"'
		self.lg(od,'WARNING')
		open(self.__regpth,'wb')
		open(self.__errpth,'wb')
		os.system(od)
		s=open(self.__regpth,'r').read().strip()
		if len(s):
			self.lg(s,'ERROR')
		s=open(self.__errpth,'r').read().strip()
		if len(s):
			self.lg(s,'ERROR')

	def __always(self):
		while True:
			time.sleep(self.__clk)

			if not len(self.__l):
				continue

			if self.__pause:
				continue

			if not self.__t.is_alive():
				if self.__ed:
					exit()
				self.__t=throws(self.__play)

	def __get1(self)->str:
		if len(self.__q):
			return self.__q.pop(0)
		if self.__mode=='rd':
			self.__nwn=random.randint(0,len(self.__l)-1)
		elif self.__mode=='cy':
			self.__nwn=(self.__nwn+1)%len(self.__l)
		else:
			self.__nwn%=len(self.__l)
		return self.__l[self.__nwn]

	def __up_l(self):
		self.__l=self.__ls.get_clip(0,9999,'ans_full')

	def join(self):
		_s=lambda x:str(x)+(' '*(3-len(str(x))))
		self.pt('console-music-player muz start!')
		self.__up_l()
		self.__t=throws(self.__play)
		self.__mian=throws(self.__always)
		while True:
			a=input()
			self.lg(a,'DEBUG')
			taskkill='+' not in a
			_a=a.strip()
			a=_a.replace('+','').split(' ',1)+['',]
			a2=a[1].strip()
			a=a[0]
			a=f_order(a)
			if _a=='':
				self.pt()
			elif a=='r':
				if self.__mode=='lp':
					self.__nwn+=1
				self.pt()
			elif a=='l':
				self.__q=self.__his[-2:999]+self.__q
				self.pt()
			elif a=='re':
				self.__q=self.__his[-1:999]+self.__q
				self.pt()
			elif a=='up':
				self.__up_l()
				self.pt()
			elif a=='p':
				self.__pause=~self.__pause
				self.pt('pause...' if self.__pause else 'restart')
			elif a=='m':
				_a3=f_mode(a2)
				if _a3!=self.__mode:
					self.__mode=_a3
					self.__up_l()
				self.pt()
			elif a=='exit':
				self.pt('exit!')
				exit()

			elif a=='ll':
				if 'all' in a2:
					self.__ls.show(fullpath='full' in a2,no=True)
				elif a2=='dir':
					self.__ls.showdir(fullpath='full' in a2,no=True)
				elif a2=='file':
					self.__ls.showfile(fullpath='full' in a2,no=True)
				else:
					self.__ls.showfile(fullpath='full' in a2,no=True,onlyans=True,name='music')
				self.pt()
			elif a=='cd':
				try:
					_a3=int(a2)
				except:
					_a3=a2
				self.__ls.cd(_a3)
				self.pt()
			elif a=='list':
				_rn=0
				self.pt('list('+str(len(self.__l))+'):')
				for i in self.__l:
					self.pt(_s(_rn)+(' \033[34m' if i==self.__his[-1] else ' \033[33m')+i+'\033[0m')
					_rn+=1
			elif a=='his':
				self.pt('history('+str(len(self.__his))+'):')
				_rn=0
				for i in self.__his:
					self.pt(_s(_rn)+(' \033[34m' if i==self.__his[-1] else ' \033[33m')+i+'\033[0m')
					_rn+=1
			elif a=='i':
				self.pt(self.__mode+' '+str(len(self.__his)))

			elif a=='rm':
				a2=a2.replace(':',' ')
				if ' ' in a2:
					l,r=a2.split(' ')
					l=int(l)
					r=int(r)
				else:
					l=int(a2)
					r=int(l+1)
				_l=self.__l[l:r]
				for i in _l.copy():
					self.__l.remove(i)
				self.pt('remove '+str(len(_l))+' music')
			elif a=='add':
				a2=a2.replace(':',' ')
				if ' ' in a2:
					l,r=a2.split(' ')
					l=int(l)
					r=int(r)
				else:
					l=int(a2)
					r=int(l+1)
				_l=[i for i in self.__ls.get_clip(l,r,'ans_full') if i not in self.__l]
				self.__l+=_l
				self.pt('add '+str(len(_l))+' music')
			else:
				_flg=True
				if os.path.exists(_a):
					if os.path.isfile(_a):
						_flg=False
						self.__q.append(os.path.abspath(_a))
				_a=os.path.join(self.__ls.get_pth(),_a)
				if os.path.exists(_a):
					if os.path.isfile(_a):
						_flg=False
						self.__q.append(os.path.abspath(_a))
				if _flg:
					self.pt('OrderNotFoundError: '+a)
				else:
					self.pt('append 1 music')

			if a in list('rlpm')+['exit','re']:
				if taskkill:
					self.__kill()


nMuz().join()

