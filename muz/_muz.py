import os
import re
import sys
import time
import shlex
import random
import logging
import subprocess

from userelaina.th import throws
from userelaina.pthc import Ls,Archive,col2str,fastlog

_debug=True
_white='\x1b[0m'

error_codes={
    403:'Forbidden',
    404:'Not_Found',
    405:'Method_Not_Allowed',
    415:'Unsupported_Media_Type',
}
# https://http.cat/

state_codes={
    0:'playing',
    1:'paused',
    2:'stopped',
}

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
    'h':['help','?','wtf'],
    'pwd':[],
    'w':['i','info','who','whoami'],
    'cd':[],
    'clear':['cls'],
    'explorer':['open'],
    'm':['mode'],
    'reboot':[],
    'exit':['quit','halt','poweroff'],
    'exec':['eval'],

    'p':['pause'],
    'start':['restart'],
    'stop':[],

    'his':['history'],
    'lst':['list'],
    'la':['dir','lla'],
    'lf':[],
    'ld':[],
    'ls':['ll'],

    'l':['left'],
    're':['repeat'],
    'r':['right'],
    'rd':['random'],

    'rm':['del','delete','remove'],
    'add':['append'],
    'u':['up','update'],
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
        pth:str='./',
        mode:str='random',
        color_muz:str='yellow',
        color_now:str='cyan',
        color_pwd:str='green',
        color_err:str='red',
        log:str='muz.log',
        clk:float=0.1,
    ):
        self.__log=fastlog('muz','quiet',log)
        # DEBUG INFO WARNING ERROR CRITICAL

        self.__ls=Ls(pth)
        self.__ls.setcolor('muz',color_muz)
        self.__col_muz=col2str(color_muz)
        self.__col_now=col2str(color_now)
        self.__col_pwd=col2str(color_pwd)
        self.__col_err=col2str(color_err)

        self.__mode=f_mode(mode)
        self.__clk=clk

        self.__mian=None # play subprocess (of __always_play)
        self.__sub=None # ffplay subprocess (of __t)
    
    def lg(self,s:all):
        s=repr(s)
        self.__log.debug(s)

    def pt(self,s:str=None):
        res='None...'
        if s:
            s=str(s)
            res=re.sub('\x1b\[[0-9]+m','',s)
            print('\r'+s+' '*(len(self.__ls.pwd())+2-len(res)))
        self.__log.info(res)
        print('\r'+self.__col_pwd+self.__ls.pwd()+'#'+_white+' ',end='')

    def sh(self,s:str)->str:
        self.__log.warning(s)
        sub=subprocess.Popen(
            shlex.split(s),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            encoding='utf8',
            errors='replace',
        )
        if s.startswith('ffplay'):
            self.__sub=sub
        return sub.stdout.read()

    def er(self,s:str,code:int)->str:
        s=str(s)
        _s=error_codes[code]+': '+s
        _ws=' '*(len(self.__ls.pwd())+2-len(_s))
        print('\r'+self.__col_err+error_codes[code]+_white+': '+s+_ws)
        self.__log.error(s)
        print('\r'+self.__col_pwd+self.__ls.pwd()+'#'+_white+' ',end='')

    def rd(self)->int:
        if self.__ls.lencho()<=1:
            return 0
        _l=random.randint(0,self.__ls.lencho()-2)
        if _l>=self.__n:
            _l+=1
        return _l

    def __reset_nx(self):
        if self.__mode=='loop':
            self.__nx=self.__n
        elif self.__mode=='cycle':
            self.__nx=self.__n+1
        else:
            self.__nx=self.rd()

    def __pop(self)->str:
        while True:
            time.sleep(self.__clk)
            while not self.__ls.lencho():
                time.sleep(self.__clk)
            reg_state=self.__state
            while self.__state:
                time.sleep(self.__clk)
                _reg_state=self.__state
                if _reg_state:
                    reg_state=_reg_state

            if reg_state==1 and self.__now:
                return self.__now['pth']
            self.__n=self.__nx%self.__ls.lencho()
            self.__reset_nx()
            return self.__ls.getcho(self.__n)

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
                _d=self.__ls.delcho(pth)
                print(_d,self.__ls.cho)
                
                self.__nx=self.__n
                pth=self.__pop()
                od='ffprobe -show_format "'+pth+'"'
                l=self.sh(od).split('\n')
                _flg=True

        self.__his.append(pth)
        self.pt(self.__col_now+os.path.basename(pth)+_white)

        od='ffplay -nodisp -autoexit -hide_banner -loglevel quiet '
        if self.__ss:
            od+='-ss '+str(self.__ss)+' '
            self.__ss=0
        od+='"'+pth+'"'
        self.sh(od)
        self.__mian=throws(self.__play)

    def __kill(self):
        if self.__sub is not None:
            self.__sub.terminate()
            self.__sub=None

    def cmd_none(self):
        self.pt()

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

    def cmd_pwd(self):
        self.pt(self.__ls.pwd())

    def cmd_w(self):
        s=self.__mode+' '+str(len(self.__his))+' '
        if self.__state==0 and not self.__ls.lencho():
            s+='waiting'
        else:
            s+=state_codes[self.__state]
        if _debug:
            s+=' ['+self.__col_err+'debug'+_white+']'
        self.pt(s)

        if self.__now:
            self.pt(self.__col_now+self.__now['pth']+_white)
            if self.__state:
                _nw=self.__ss
            else:
                _nw=time.time()-self.__now['start']
            s=f_time(_nw)+'/'+f_time(self.__now['duration'])+' '
            s+=str(round(100*_nw/self.__now['duration'],2))+'%'
            self.pt(s)
            s=[self.__now['format'],self.__now['bit_rate'],self.__now['size'],self.__now['probe_score'],]
            s=' '.join(s)
            self.pt(s)

        if self.__ls.lencho():
            self.pt('Next: '+self.__col_muz+self.__ls.getcho(self.__nx)+_white)


    def cmd_cd(self,s:str):
        if self.__ls.cd(s):
            self.er('The system cannot find the path "'+str(s)+'" specified.',404)
        else:
            self.pt()

    def cmd_clear(self):
        print('\x1b[256F\x1b[0J',end='')
        self.pt()

    def cmd_explorer(self):
        if os.name=='nt':
            self.sh('explorer "'+self.__ls.pth+'"')
            self.pt()
        else:
            self.er('For Windows NT only.',403)

    def cmd_m(self,mode:str):
        if mode==self.__mode:
            self.pt()
        else:
            self.__mode=mode
            self.__reset_nx()
            self.pt('The playback mode is changed to "'+mode+'".')


    def cmd_reboot(self):
        self.__ss=0 # Next ffmpeg command -ss
        self.__state=2
        self.__kill()

        self.__n=0 # No. __n music in __l is playing.
        self.__nx=0 # No. __nx music in __l will play next.
        self.__now=dict()
        self.__his=list()
        self.__start_str='Start!'

        self.cmd_clear()
        self.pt('Windows Muz')
        self.pt('Copyright (C) userElaina. All rights reserved.')
        self.pt(' ')
        self.pt('Get the source  https://github.com/userElaina/console-music-player')
        self.pt(' ')
        if self.__ls.setcho('ans'):
            self.pt(self.__start_str)
            self.__start_str='Restart!'
        self.__state=0

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
            s=s.replace(self.__col_muz+os.path.basename(self.__now['pth']),self.__col_now+os.path.basename(self.__now['pth']))
        print(s,end='')
        self.pt()


    def cmd_nx(self,delta:int,to0:bool):
        if not self.__ls.lencho():
            self.pt()
            return
        if self.__state==1:
            self.__state=2
            self.__ss=0
            self.__nx=self.__n
        if delta==8:
            self.__nx=self.rd()
        elif delta:
            self.__nx+=delta
        else:
            self.__nx=self.__n
        if self.__state:
            self.ss=0
            to0=False
        if to0:
            self.pt()
        else:
            self.pt('Next: '+self.__col_muz+os.path.basename(self.__ls.getcho(self.__nx%self.__ls.lencho()))+_white)


    def cmd_rm(self,l:int,r:int):
        _l=self.__ls.uncho(l,r)
        self.pt('Removed '+str(_l)+' music.')

    def cmd_add(self,l:int,r:int):
        if not self.__ls.lencho():
            self.__n=0
            self.__nx=0
        _l=self.__ls.addcho('ans',l,r)
        self.pt('Added '+str(_l)+' music.')

    def cmd_u(self):
        self.__n=0
        self.__nx=0
        _l=self.__ls.setcho('ans')
        self.pt('Updated to have '+str(_l)+' music.')


    def cmd_jmp_int(self,x:int)->str:
        try:
            x=int(x)
            return x%self.__ls.lencho()
        except:
            return None

    def cmd_jmp_str(self,command:str)->str:
        pth=os.path.join(self.__ls.pwd(),command)
        if os.path.exists(pth):
            if os.path.isfile(pth):
                return pth
        if os.path.exists(command):
            if os.path.isfile(command):
                return command
        return None

    def cmd_jmp(self,command:str):
        pth=self.cmd_jmp_int(command)
        if pth is not None:
            self.__nx=pth
            return 1
        pth=self.cmd_jmp_str(command)
        if pth is None:
            return None
        self.__nx=self.__ls.findcho(pth)
        _l=self.__ls.addcho([pth,])
        self.__nx%=self.__ls.lencho()
        self.pt('Appended '+str(_l)+' music.')
        return 1


    def cmd_state(self,to0,top,tor):
        _s=None
        if self.__state==0 and (to0|top):
            if not self.__now:
                to0=True
            if top:
                _s='Stop!' if to0 else 'Pause!'
                self.__state=2 if to0 else 1
            if self.__now:
                if to0:
                    self.__ss=0
                    self.__now=dict()
                else:
                    self.__ss=max(0,time.time()-self.__now['start']-self.__clk)
                self.__kill()
        elif self.__state and (to0|tor):
            if self.__state==1 and to0:
                _s='Stop!'
                self.__state=2
                self.__ss=0
                self.__now=dict()
            if tor:
                if self.__ls.lencho():
                    self.__start_str='Restart!'
                    _s='Continue!' if self.__state==1 else self.__start_str
                    self.__state=0
                else:
                    _s='No music in the playlist!'
                    self.__state=2
        if _s:
            self.pt(_s)
        else:
            if top or tor:
                self.pt()



    def cmd(self,command:str):
        self.lg(command)
        x=_splitcmd(command)
        self.lg(str(x))
        to0='+' in command
        top=False
        tor=False
        
        if x[0]=='':
            self.cmd_none()
        elif x[0].startswith('qwq') or x[0] in ('owo','qaq','quq','qvq','tat','0w0'):
            self.cmd_qwq(x[0])

        elif x[0]=='h':
            self.cmd_h()
        elif x[0]=='pwd':
            self.cmd_pwd()
        elif x[0]=='w':
            self.cmd_w()

        elif x[0]=='cd':
            try:
                k=int(x[1])
            except:
                k=x[1]
            self.cmd_cd(k)

        elif x[0]=='clear':
            self.cmd_clear()
        elif x[0]=='explorer':
            self.cmd_explorer()
        elif x[0]=='m':
            self.cmd_m(f_mode(x[1]))

        elif x[0]=='reboot':
            self.cmd_reboot()
        elif x[0]=='exit':
            self.cmd_exit()
        elif x[0]=='exec':
            self.cmd_exec(x[1])

        elif x[0]=='p':
            top=True
            tor=True
        elif x[0]=='stop':
            top=True
            to0=True
        elif x[0]=='start':
            tor=True

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

        elif x[0] in ('l','re','r','rd'):
            if x[0]=='l':
                delta=-1
            elif x[0]=='re':
                delta=0
            elif x[0]=='r':
                delta=1
            else:
                delta=8
            self.cmd_nx(delta=delta,to0=to0)

        elif x[0] in ('rm','add'):
            l,r=_splitlr(x[1])
            if x[0]=='rm':
                self.cmd_rm(l,r)
            elif x[0]=='add':
                self.cmd_add(l,r)
        elif x[0]=='u':
            self.cmd_u()

        else:
            if self.cmd_jmp(command) is None:
                self.er(command,405)

        self.cmd_state(to0,top,tor)

    def join(self):
        _check=['ffplay','ffprobe',]
        if os.name=='nt':
            _whereis='where '
            for i in _check:
                _s=self.sh(_whereis+i)
                if _s.strip()=='':
                    print('Please add '+i+' to the PATH or where you want to run this program.')
                    self.cmd_exit()
        else:
            _whereis='whereis '
            for i in _check:
                _s=self.sh(_whereis+i)
                if _s.strip().endswith(':'):
                    print('Please add '+i+' to the PATH or where you want to run this program.')
                    self.cmd_exit()

        self.cmd_reboot()
        self.__mian=throws(self.__play)
        while True:
            command=input().strip()
            self.cmd(command=command)
