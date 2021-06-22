# console-music-player

播放器的实现为命令行调用**ffplay**,故支持的格式非常多(ffmpeg yyds!:)
![image](https://user-images.githubusercontent.com/80948381/122000181-fd3e0280-cde0-11eb-8a7b-4173f2871dce.png)


## Done

以三种形式播放(单曲,随机,顺序)

`l` 上一首

`r` 下一首

`re` 重复这首

`i` 输出当前状态

FileAbsPath 立即播放指定文件

FileAbsPath 下一次播放指定文件

更详细的 log

模式切换

输入指令的地方前边加 Path+`#`

`p` 暂停(再开始时这首歌会从头开始)

`ls` `cd`

显示播放队列

修改播放队列(删点、删段、删歌、单点添加歌曲、循环添加歌曲)

## To Do

帮助文档

### 播放队列

## Won't Do

显示歌词

曲内暂停功能

联网功能

对本地音乐文件的非只读操作
