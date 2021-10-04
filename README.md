# Console Music Player

The player is [ffplay](https://ffmpeg.org/).
If you don't have it installed, you can download it from [here (binary file)](https://github.com/BtbN/FFmpeg-Builds/releases).

[Chinese (中文)](README_zh.md)

## Version

`0.0.4`

## Help

### Basic Commands

#### help

`h` `help`

Show help.

#### cd

`cd %s` *path*

Change the current path to *path*.

*path* can be a relative path or an absolute path, or even a number.

When it's a number, it means that the last command that show the file list is the path folder of the last show file list command.

#### pwd

`pwd`

Show current path.

#### w

`w` `i` `info`

Show status.

```py
str(play_mode),int(total_number_played),str(player_status)
str(name_of_the_music_file_currently_playing)
str(play_time),str(playback_progress_percentage)
str(music_format),str(bit_rate),str(size),str(probe_score)
```

#### clear

`clear` `cls`

Clear **console**.

#### exit

`exit`

Exit.

#### exec

`exec` `eval`

`exec %s` *code*

Run *code*.

Only for developers.

### The Command to Export a List of Files

The default highlight colour for music files is yellow, 
and the default highlight colour for currently playing music files is cyan.

#### his

`his` `history`

Show the played music files, 
with the currently playing music file highlighted.

#### lst

`lst` `list`

Show a list of the current music files, 
with the currently playing music file highlighted.

#### la

`la` `ls all` `ll all`

Show all files and directories in the current path, 
with music files highlighted.

#### lf

`lf` `ls file` `ll file`

Show all files in the current path, 
with music files highlighted.

#### ld

`ld` `ls dir` `ll dir`

Show all directories in the current path, 
with music files highlighted.

#### ls

`ls` `ll` 

Show all music files in the current path, 
with the currently playing music file highlighted.

### Commands to Modify the Playlist

Play in these three forms: 
sequential play `cycle`, 
single song loop `loop`, 
random play `random`.

#### l

`l` `left`

Play the previous song at the end of the current play.

#### re

`re` `repeat`

Play again at the end of the current play.

#### r

`r` `right`

Play the next song at the end of the current playback.

#### rm

`rm` `remove` `del` `delete`

`rm %d` *n*

Delete the *n*th song in the playlist.

`rm %d:%d` *l*,*r*

Delete the [l:r] songs in the playlist.

*l* and *r* can be defaulted, 
you can see **Python** syntax for meaning.

#### add

`add` `append`

`add %d` *n*

Add the *n*th file to the playlist from the list of files 
(show from the previous show file list command).

`add %d:%d` *l*,*r*

Add the [l:r] files to the playlist from the list of files 
(show from the previous show file list command).

*l* and *r* can be defaulted, 
you can see **Python** syntax for meaning.

#### u

`u` `up` `update`

Delete the old playlist and updates the playlist to all music files in the current path.

### The Command to Modify the Playback Status

#### p

`p` `pause`

Pause or restart.

#### m

`m` `mode`

`m %s` *mode*

Change the playback mode to *mode*.

### Others

When adding the character `+` to any command, (if it is playing,) it will end the current playback at the end of the command.

When the command entered is the path of a file, it will immediately stop playing the file being played and play the corresponding file entered instead.

When the command entered is a number, playback will be stopped immediately and the music corresponding to the number entered in the playlist will be played instead.

## To Do

Embedded `help` documents.

Pack (Virtual Machines).

Linux version.

Switches whether to display information in real time and dynamically.

## Won't Do

Networked music search.

Non-read-only operation on local music files.

GUI.
