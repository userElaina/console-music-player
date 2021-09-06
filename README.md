# console-music-player

播放器的实现为命令行调用**ffplay**,故支持的格式非常多(ffmpeg yyds!:)
![image](https://user-images.githubusercontent.com/80948381/122000181-fd3e0280-cde0-11eb-8a7b-4173f2871dce.png)


## Help

### 只输出信息的命令

#### `qwq`

`qwq`

输出 `QwQ`

#### `w`

`w` `i` `info`

输出当前状态(`播放模式 总共播放了几首`)

#### `his`

`his` `history`

输出已播放歌曲

其中,当前正在播放歌曲高亮

#### `lst`

`lst` `list`

输出当前播放列表

其中,当前正在播放歌曲高亮

#### `ll`

### 改变播放队列的命令

以三种形式播放(单曲 `lp` ,随机 `rd` ,顺序 `cy` )

#### `l`

`l` `left`

当前播放结束时,播放上一首

#### `re`

`re` `repeat`

当前播放结束时,再次播放(重复一次)

#### `r`

`r` `right`

当前播放结束时,播放下一首

#### `up` 

`up` `u` `update`

将播放列表更新为当前目录下所有音乐文件

#### `p`

`p` `pause`

暂停/开始

#### `m`

`m {mode}` `mode {mode}`

切换播放模式

#### `rm`

`rm` `remove` `del` `delete`

`rm {n}`

从播放列表中删除第 `n` 首

`rm {n} {m}`

从列表中删除第 `n` 到 `m` 首

#### `add`

`add` `append`

`add {n}`

从文件中添加(文件的)第 `n` 首到播放列表

`add {n} {m}`

从文件中添加(文件的)第 `n` 到 `m` 首到播放列表

### 其它命令

#### ``

`` 

换行

#### `cd`

`cd {path_of_dir}`

将当前路径改变为 `path_of_dir`

`path_of_dir` 可以是相对路径或绝对路径,甚至可以是数字

当其是数字时,意味着 `ls all` 命令中的第 `path_of_dir` 个文件夹

#### `exit`

`exit`

退出

### 其它

当在任何命令中加入字符 `+` ,将会在命令结束时结束当前歌曲的播放.

## To Do

帮助文档

### 播放队列

## Won't Do

显示歌词

曲内暂停功能

联网功能

对本地音乐文件的非只读操作
