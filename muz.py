import os
import re
import sys
import time
import copy
import random
import logging
import threading


'''
_th
'''

def throws(f,args:tuple=tuple())->None:
	if not f:
		f=args

	if isinstance(f,(list,tuple)):
		if len(f)==1:
			args=tuple()
		elif len(f)==2:
			args=f[1]
		else:
			args=f[1:]
		f=f[0]

	if not isinstance(args,tuple):
		args=(args,)
		
	_t=threading.Thread(target=f,args=args,daemon=True)
	_t.start()
	return _t


'''
_pth
'''

exts={
	'':[''],
	'qwq':['qwq','qwq1','qwq2','qwq3','qwq4','bmp'],
	'pic':['png','jpg','jpeg','gif','bmp','tif','tiff'],
	'tar':['rar','zip','7z','tar','gz','xz','z','bz2'],
	'music':['mp3','wav','flac'],
	'movie':['mp4','mkv','mov','ts'],
	'office':['csv','doc','docx','ppt','pptx','xls','xlsx','pdf'],
	'danger':['vbs','sh','cmd','exe'],
	'html':['html'],
	'txt':['txt','in','out','log'],
	'data':['xml','json','svg','csv','md','rst'],
	'c':['c','cpp','h','hpp'],
	'java':['java'],
	'py':['pyi','py'],
	'othercodes':['cs','go','js','lua','pas','php','r','rb','swift','ts','vb','sh','vbs'],
}
exts['muz']=exts['music']
exts['vid']=exts['movie']
exts['cpp']=exts['c']
exts['python']=exts['py']
exts['codes']=exts['c']+exts['java']+exts['py']+exts['othercodes']+exts['data']
exts['text']=exts['codes']+exts['txt']+exts['html']

colors={
	'default':'\033[0m',
	'red':'\033[31m',
	'green':'\033[32m',
	'yellow':'\033[33m',
	'blue':'\033[34m',
	'purple':'\033[35m',
	'cyan':'\033[36m',
}

color_name={
	'dft':'default',
	'rd':'red',
	'yl':'yellow',
	'pp':'purple',
	'ppl':'purple'
}

for i in colors:
	color_name[i]=i
	color_name[i[0]]=i
	color_name[i[:2]]=i


class Pth:
	def __init__(
		self,
		old:str='.old',
	):
		self.old=old

	def ck(
		self,
		pth:str,
		l:int=5,
	)->str:
		pth=os.path.abspath(pth)
		if not os.path.exists(pth):
			return
		i=1
		pth2=pth+'.'+str(i).zfill(l)+self.old
		while os.path.exists(pth2):
			i+=1
			pth2=pth+'.'+str(i).zfill(l)+self.old
		os.rename(pth,pth2)
		return pth2

def get_ext(s:str)->str:
	_base=os.path.basename(s)
	return _base.rsplit('.',1)[-1].lower() if '.' in _base else ''
_s=lambda x:str(x)+(' '*(3-len(str(x))))

class Ls:
	def __init__(
		self,
		pth:str='./',
		l:list=list(),
	):
		self.__pth=os.path.abspath('./')
		self.cd(pth)
		self.__col=dict()
		self.__cols={'red','green','yellow','blue','purple','cyan'}

		for i in l:
			if isinstance(i,str):
				self.paint(i)
			else:
				self.paint(i[0],i[1])

	def __get_col(self)->str:
		ans=random.choice(list(self.__cols))
		if len(self.__cols)>1:
			self.__cols.discard(ans)
		return ans

	def cd(self,pth:str):
		if isinstance(pth,int):
			pth=self.get_clip(pth+2)
		_ans=os.path.abspath(os.path.join(self.__pth,pth))
		self.__pth=_ans if os.path.isdir(_ans) else os.path.dirname(_ans)
		self.__d=['.','..',]
		self.__f=list()
		self.__ext=list()
		for i in os.listdir(self.__pth):
			_full=os.path.join(self.__pth,i)
			if os.path.isdir(_full):
				self.__d.append(i)
			elif os.path.isfile(_full):
				self.__f.append(i)
		self.__up_flg=True

	def paint(self,x:str,y:str=None)->bool:
		if x not in exts:
			return False
		y=color_name[y] if y in color_name else self.__get_col()
		_d={i:y for i in exts[x]}
		self.__col.update(_d)
		self.__up_flg=True
		return True

	def get_pth(self)->str:
		return self.__pth

	def up(self)->dict:
		if not self.__up_flg:
			return copy.deepcopy(self.__d)
		_col=[self.__col.get(get_ext(i),'default') for i in self.__f]
		_ans=[i for i in self.__f if self.__col.get(get_ext(i),'default')!='default']
		self.__d={
			'pth':self.__pth,
			'dir':self.__d,
			'file':self.__f,
			'ans':_ans,
			'dir_full':[os.path.join(self.__pth,i) for i in self.__d],
			'file_full':[os.path.join(self.__pth,i) for i in self.__f],
			'ans_full':[os.path.join(self.__pth,i) for i in _ans],
			'file_color':_col,
			'ans_color':[i for i in _col if i!='default'],
			'len_dir':len(self.__d)-2,
			'len_file':len(self.__f),
			'len_ans':len(_ans),
		}
		self.__up_flg=False
		return copy.deepcopy(self.__d)

	def get_clip(self,l:int,r:int=None,k:str='dir')->list:
		_d=self.up()
		if k not in {'dir','file','ans','dir_full','file_full','ans_full'}:
			return list()
		return _d[k][l:r] if r else _d[k][l]

	def showdir(self,fullpath:bool=False,no:bool=False):
		_d=self.up()
		print('dir('+str(_d['len_dir'])+'):')
		_dir=_d['dir_full' if fullpath else 'dir']
		for i in range(_d['len_dir']+2):
			if no:
				print(_s(i-2),end=' ')
			print(os.path.join(_dir[i],''))
		
	def showfile(self,fullpath:bool=False,no:bool=False,onlyans:bool=False,name:str='file'):
		_d=self.up()
		_hd='ans' if onlyans else 'file'
		_file=_d[_hd+('_full' if fullpath else '')]
		print(colors['default']+name+'('+str(_d['len_ans'])+'/'+str(_d['len_file'])+'):')
		for i in range(_d['len_'+_hd]):
			if no:
				print(_s(i),end=' ')
			print(colors[_d[_hd+'_color'][i]]+_file[i]+'\n'+colors['default'],end='')

	def show(self,fullpath:bool=False,no:bool=False):
		print(colors['default'])
		print(colors['green']+self.get_pth()+'# '+colors['default'])
		print(colors['default'])
		self.showdir(fullpath,no)
		print(colors['default'])
		self.showfile(fullpath,no)
		print(colors['default'])


'''
_log
'''

class Log:
	def __init__(
		self,
		pth:str='py.log',
		erpth:str=None,
	):
		bg=list()

		
		self.__pth=os.path.abspath(pth)
		s=Pth('.log').ck(self.__pth)
		open(self.__pth,'wb')
		if s:
			bg.append(self.__pth+' already exists, and then it is moved '+s)

		if erpth:
			self.__err=os.path.abspath(erpth)
			s=Pth('.log').ck(self.__err)
			open(self.__err,'wb')
			if s:
				bg.append(self.__err+' already exists, and then it is moved '+s)

		bg.append('Log start!')
		
		'DEBUG INFO WARNING ERROR CRITICAL'
		self.__logger=logging.getLogger('Log')
		self.__logger.setLevel(logging.DEBUG)
		formatter=logging.Formatter("%(asctime)s %(message)s")

		handler_lg=logging.FileHandler(filename=self.__pth,encoding='utf-8')
		handler_lg.setLevel(logging.DEBUG)
		handler_lg.setFormatter(formatter)
		self.__logger.addHandler(handler_lg)

		handler_pt=logging.StreamHandler()
		handler_pt.setLevel(logging.INFO)
		handler_pt.setFormatter(logging.Formatter("%(message)s"))
		self.__logger.addHandler(handler_pt)

		if erpth:
			handler_er=logging.FileHandler(filename=self.__err,encoding='utf-8')
			handler_er.setLevel(logging.ERROR)
			handler_er.setFormatter(formatter)
			self.__logger.addHandler(handler_er)

		# for i in bg:
		# 	self.er(i)

	def lg(self,s:str):
		s=str(s)
		self.__logger.debug(s)

	def pt(self,s:str):
		s=str(s)
		self.__logger.info(s)

	def er(self,s:str):
		s=str(s)
		self.__logger.error(s)

	def ptr(self,s:str):
		pt(repr(s))


'''
muz
'''

__denug=True

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

d_command={
	'l':['left'],
	're':['repeat'],
	'r':['right'],
	'up':['u','update'],
	
	'p':['pause'],
	'm':['mode'],

	'll':['ls'],
	'lst':['list'],
	'w':['info','i'],
	'his':['history'],

	'rm':['del','delete','remove'],
	'add':['append'],
}
for i in d_command:
	d_command[i].append(i)

def f_command(x:str)->str:
	for i in d_command:
		if x in d_command[i]:
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
		print('\r\033[32mMUZ '+self.__ls.get_pth()+'#\033[0m ',end='')
		self.lg(s,'INFO')

	def __play(self):
		while not len(self.__l):
			time.sleep(self.__clk)
		pth=self.__get1()
		self.__his.append(pth)
		self.pt('\033[36m'+pth+'\033[0m')
		od='ffplay -nodisp -autoexit -hide_banner -loglevel quiet "'+pth+'" > "'+self.__warnpth+'"'
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
			taskkill='+' in a
			_a=a.strip()
			a=_a.replace('+','').split(' ',1)+['',]
			a2=a[1].strip()
			a=a[0].lower()
			a=f_command(a)

			if _a=='':
				self.pt()

			elif a=='qwq':
				self.pt('QwQ')

			elif a=='w':
				self.pt(self.__mode+' '+str(len(self.__his)))
			elif a=='his':
				self.pt('history('+str(len(self.__his))+'):')
				_rn=0
				for i in self.__his:
					self.pt(_s(_rn)+(' \033[34m' if i==self.__his[-1] else ' \033[33m')+i+'\033[0m')
					_rn+=1
			elif a=='lst':
				_rn=0
				self.pt('list('+str(len(self.__l))+'):')
				for i in self.__l:
					self.pt(_s(_rn)+(' \033[34m' if i==self.__his[-1] else ' \033[33m')+i+'\033[0m')
					_rn+=1
			elif a=='ll' or a=='ls' or a=='la':
				if a=='la' or 'all' in a2:
					self.__ls.show(fullpath='full' in a2,no=True)
				elif a2=='dir':
					self.__ls.showdir(fullpath='full' in a2,no=True)
				elif a2=='file':
					self.__ls.showfile(fullpath='full' in a2,no=True)
				else:
					self.__ls.showfile(fullpath='full' in a2,no=True,onlyans=True,name='music')
				self.pt()

			elif a=='l':
				self.__q=self.__his[-2:999]+self.__q
				self.pt()
			elif a=='re':
				self.__q=self.__his[-1:999]+self.__q
				self.pt()
			elif a=='r':
				if self.__mode=='lp':
					self.__nwn+=1
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

			elif a=='cd':
				try:
					_a3=int(a2)
				except:
					_a3=a2
				self.__ls.cd(_a3)
				self.pt()

			elif a=='exit':
				# self.pt('exit!')
				self.__kill()
				sys.exit()

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
					self.pt('MuzCommandNotFound: '+a)
				else:
					self.pt('append 1 music')

			if taskkill:
				self.__kill()

nMuz().join()
