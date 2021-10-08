# Console Music Player

播放器为 [ffplay](https://ffmpeg.org/).
如果你没有安装它,可以从[这里](https://github.com/BtbN/FFmpeg-Builds/releases)下载(二进制文件).

[英文 (English)](README.md)

## Version

`0.0.4`

Early access 版本,初步测试可正常使用,但不保证后续更新的兼容性.

## Help

### 基本命令

#### help

`h` `help` `?`

Show help.

#### pwd

`pwd`

打印当前路径.

#### w

`w` `i` `info` `who` `whoami`

Show status.

```py
str(play_mode),int(total_number_played),str(player_status)
str(name_of_the_music_file_currently_playing)
str(play_time),str(playback_progress_percentage)
str(music_format),str(bit_rate),str(size),str(probe_score)
```

#### cd

`cd %s` *path*

将当前路径改变为 *path*.

*path* 可以是相对路径或绝对路径,甚至可以是数字.

当其是数字时,意味着(上一个**打印文件列表的命令**中打印的)文件列表的第 *path* 个文件夹.

#### clear

`clear` `cls`

Clear **console**.

#### explorer

`explorer` `open`

打开当前路径文件夹.

For windows only.

#### m

`m` `mode`

`m %s` *mode*

切换播放模式为 *mode*.

可以以三种形式播放:

顺序播放 `cycle`;

单曲循环 `loop`;

随机播放 `random`.

#### exit

`exit` `quit`

Exit.

#### exec

`exec` `eval`

`exec %s` *code*

Run *code*.

For developer debugging only.

This is the only command that causes an error that makes the program exit abnormally, I think.

### 改变播放状态的命令

有三种播放状态:

**playing**,

**paused**,

**stopped**.

#### p

`p` `pause`

Pause or restart.

#### stop

`stop`

Stop (not exit).

当前状态为**playing**时,该命令等效于 `p+`;

当前状态为**paused**时,该命令等效于 `+`.

#### restart

`restart` `start`

Restart.

当前状态为**playing**时,该命令无效.

### 打印文件列表的命令

音乐文件默认高亮色为黄色,当前播放音乐文件默认高亮色为青色.

#### his

`his` `history`

打印已播放音乐文件.

其中,当前正在播放音乐文件高亮.

#### lst

`lst` `list`

打印当前音乐文件列表.

其中,当前正在播放音乐文件高亮.

#### la

`la` `ls all` `ll all`

打印当前路径所有文件和文件夹.

其中,音乐文件高亮.

#### lf

`lf` `ls file` `ll file`

打印当前路径所有文件.

其中,音乐文件高亮.

#### ld

`ld` `ls dir` `ll dir`

打印当前路径所有文件夹.

#### ls

`ls` `ll` 

打印当前路径所有音乐文件.

其中,当前正在播放音乐文件高亮.

### 改变播放队列的命令

#### l

`l` `left`

当前播放结束时,播放上一首.

#### re

`re` `repeat`

当前播放结束时,再次播放(重复一次).

#### r

`r` `right`

当前播放结束时,播放下一首.

#### rd

`rd` `random`

在当前播放结束时,随机播放一首.

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

从(上一个**打印文件列表的命令**中打印的)文件列表中添加第 *n* 首到播放队列.

`add %d:%d` *l*,*r*

从(上一个**打印文件列表的命令**中打印的)文件列表中添加 `[l:r]` 首到播放队列.

*l*,*r* 均可缺省,语义如 **Python**.

#### u

`u` `up` `update`

(删除原播放队列,并)将播放队列更新为当前目录下所有音乐文件.

### 其它

当命令一个文件的路径,下一首将会播放输入对应的文件.

当命令一个数字,下一首将会播放输入的数字在播放列表中对应位置的音乐.

当命令中含有字符 `+` 时,(若正在播放,)将会在命令执行结束时结束当前的播放,并删除存在的断点.

## To Do

Embedded `help` documents (not url).

Pack (Virtual Machines).

Linux version.

Switches whether to display information in real time and dynamically.

## Won't Do

联网搜索音乐.

对本地音乐文件的非只读操作.

GUI.
