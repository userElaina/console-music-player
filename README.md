# console-music-player

播放器的实现为命令行调用**ffplay**,故支持的格式非常多(ffmpeg yyds!:)
![image](https://user-images.githubusercontent.com/80948381/122000181-fd3e0280-cde0-11eb-8a7b-4173f2871dce.png)


## Done

以三种形式播放(单曲,随机,顺序)

`r` 立即切换到下一首

`r+` 下一次切换到下一首(单曲模式时有效)

FileAbsPath 立即播放指定文件

FileAbsPath+`+` 下一次播放指定文件

`?` 输出当前状态

## To Do

更详细的 log

帮助文档

模式切换

输入指令的地方前边加 `>>>`

暂停(再开始时这首歌会从头开始)

显示歌词

`ls`

`cd`

### 播放队列

显示播放队列

修改播放队列(删点、删段、删歌、删正则匹配、单点添加歌曲、循环添加歌曲)(快捷键: `loop` )

播放队列内跳转(快捷键: `l` `r` `re0` `re` `ll` `rr` )

## Won't Do

曲内暂停功能

联网功能

对本地音乐文件的非只读操作
