# Console Music Player

播放器为 [ffplay](https://ffmpeg.org/).
如果你没有安装它,可以从[这里](https://github.com/BtbN/FFmpeg-Builds/releases)下载(二进制文件).

## Help

### 基本命令

#### cd

`cd %s` *path*

将当前路径改变为 *path*.

*path* 可以是相对路径或绝对路径,甚至可以是数字.

当其是数字时,意味着(上一个**输出文件列表的命令**中输出的)文件列表的第 *path* 个文件夹.

#### pwd

`pwd`

输出当前路径.

#### `w`

`w` `i` `info`

输出当前状态.

```py
str(播放模式) int(总共播放了几首) str(当前播放状态)
str(当前播放的音乐文件名称)
```

#### clear

`clear` `cls`

清空 **console**.

#### exit

`exit`

退出.

### 输出文件列表的命令

音乐文件默认高亮色为黄色,当前播放音乐文件默认高亮色为青色.

#### his

`his` `history`

输出已播放音乐文件.

其中,当前正在播放音乐文件高亮.

#### lst

`lst` `list`

输出当前音乐文件列表.

其中,当前正在播放音乐文件高亮.

#### la

`la` `ls all` `ll all`

输出当前路径所有文件和文件夹.

其中,音乐文件高亮.

#### lf

`lf` `ls file` `ll file`

输出当前路径所有文件.

其中,音乐文件高亮.

#### ld

`ld` `ls dir` `ll dir`

输出当前路径所有文件夹.

#### ls

`ls` `ll` 

输出当前路径所有音乐文件.

其中,当前正在播放音乐文件高亮.

### 修改播放队列的命令

以三种形式播放:
顺序播放 `cycle`;
单曲循环 `loop`;
随机播放 `random`.

#### l

`l` `left`

当前播放结束时,播放上一首.

#### re

`re` `repeat`

当前播放结束时,再次播放(重复一次).

#### r

`r` `right`

当前播放结束时,播放下一首.

#### rm

`rm` `remove` `del` `delete`

`rm %d` *n*

从播放队列中删除(播放队列的)第 *n* 首.

`rm %d:%d` *l*,*r*

从播放队列中删除(播放队列的) `[l:r]` 首.

*l*,*r* 均可缺省,语义如 **Python**.

#### add

`add` `append`

`add %d` *n*

从(上一个**输出文件列表的命令**中输出的)文件列表中添加第 *n* 首到播放队列.

`add %d:%d` *l*,*r*

从(上一个**输出文件列表的命令**中输出的)文件列表中添加 `[l:r]` 首到播放队列.

*l*,*r* 均可缺省,语义如 **Python**.

#### u

`u` `up` `update`

(删除原播放队列,并)将播放队列更新为当前目录下所有音乐文件.

### 修改播放状态的命令

#### p

`p` `pause`

暂停/开始.

#### m

`m` `mode`

`m %s` *mode*

切换播放模式为 *mode*.

### 其它

当在任何命令中加入字符 `+` ,(若正在播放,)将会在命令执行结束时结束当前的播放.

## To Do

Embedded `help` documents.

`pause` in one music (depend on **ffprobe**).

`explorer`.

打包:普通,少依赖,打进 **ffplay**.

增加指令别名.

调整指令代码顺序.

显示歌名和进度.

显示歌词及其指定语言翻译 (depend on **Google Translate**).

显示字符画:声音波形.

## Won't Do

联网搜索音乐.

对本地音乐文件的非只读操作.

GUI.
