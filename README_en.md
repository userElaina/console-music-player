# Console Music Player

The player is [ffplay](https://ffmpeg.org/).
If you don't have it installed, you can download it from [here (binary file)](https://github.com/BtbN/FFmpeg-Builds/releases).

## Help

### Basic Commands

#### cd

`cd %s` *path*

Change the current path to *path*.

*path* can be a relative path or an absolute path, or even a number.

When it's a number, it means that the last command that output the file list is the path folder of the last output file list command.

#### pwd

`pwd`

Output current path.

#### `w`

`w` `i` `info`

Output current status.

```c
str(Play mode) int(Total number of songs played) str(Current playing status)
str(Name of the music file currently playing)
```

#### clear

`clear` `cls`

Clear **console**.

#### exit

`exit`

Exit.

### The Command to Export a List of Files

The default highlight colour for music files is yellow, 
and the default highlight colour for currently playing music files is cyan.

#### his

`his` `history`

Outputs the played music files, 
with the currently playing music file highlighted.

#### lst

`lst` `list`

Outputs a list of the current music files, 
with the currently playing music file highlighted.

#### la

`la` `ls all` `ll all`

Outputs all files and directories in the current path, 
with music files highlighted.

#### lf

`lf` `ls file` `ll file`

Outputs all files in the current path, 
with music files highlighted.

#### ld

`ld` `ls dir` `ll dir`

Outputs all directories in the current path, 
with music files highlighted.

#### ls

`ls` `ll` 

Output all music files in the current path, 
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

Adds the *n*th file to the playlist from the list of files 
(output from the previous output file list command).

`add %d:%d` *l*,*r*

Adds the [l:r] files to the playlist from the list of files 
(output from the previous output file list command).

*l* and *r* can be defaulted, 
you can see **Python** syntax for meaning.

#### u

`u` `up` `update`

Deletes the old playlist and updates the playlist to all music files in the current path.

### The Command to Modify the Playback Status

#### p

`p` `pause`

Pause or Restart.

#### m

`m` `mode`

`m %s` *mode*

Toggles the playback mode to *mode*.

### Others

When adding the character `+` to any command, (if it is playing,) it will end the current playback at the end of the command.

## To Do

Embedded `help` documents.

`pause` in one music (depend on **ffprobe**).

`explorer`.

Pack: normal, less dependent, into **ffplay**.

Add command aliases.

Reordering of command codes.

Show song titles and progress.

Show lyrics and their translation (depend on **Google Translate**).

Show character pictures: sound waveforms.

## Won't Do

Networked music search.

Non-read-only operation on local music files.

GUI.
