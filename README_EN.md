# playlist-generator
This tool automatically generates playlist files in m3u8 format.  
You can download it from [this releases page](https://github.com/takano536/playlist-generator/releases).

## Features
This tool is good at creating playlists of numbered audio files.  
This tool can sort [naturallly](https://en.wikipedia.org/wiki/Natural_sort_order) like in Windows Explorer.

## Usage
PlaylistGenerator.exe is a command line tool. Drag and drop the audio file you want to add to the playlist, or launch a command prompt and type in the following command to use it.
```
PlaylistGenerator.exe --help
```
The following command is an example of a command to create a playlist.
```
PlaylistGenerator.exe music.mp3 C:\Users\user\Music song.mp3 -o MyPlaylist --outfolder C:\Users\user\Documents
```
The following is an example of the execution result.
```
"MyPlaylist.m3u8" was created
path: C:\Users\user\Documents\MyPlaylist.m3u8
Successfully created m3u8 file
Press enter key to quit...
```

## Command line options
The following options can be specified in this software.
#### Output file name
```
-o <output file name>, --outname <output file name>
Specifies the file name.
If not specified, the name will be the same as the name of the first song in the playlist.
```
#### Output folder
```
--outfolder <output folder>
Specifies the output destination for the file.
If not specified, the output will be to the deepest parent folder that contains all the songs.
```
#### Sorting method
```
--sort <filename|foldername|date|ext|filename-desc|foldername-desc|date-desc|ext-desc>
Specifies the sorting method of the songs.
The default value is "filename".
* filename        : Sorted in ascending order by file name.
* foldername      : Sorted in ascending order by folder name.
* date            : Sorted in ascending order by creation date.
* ext             : Sorted in ascending order by filename extension.
* filename-desc   : Sorted in descending order by file name.
* foldername-desc : Sorted in descending order by folder name.
* date-desc       : Sorted in descending order by creation date..
* ext-desc        : Sorted in descending order by filename extension.
```

## Note
`date` and `date-desc` only works on Windows.
The following are audio files that can be imported by this tool.  
`.mp3` `.wma` `.oma` `.flac` `.wav` `.mp4` `.m4a` `.3gp` `.aif` `.aiff` `.afc` `.ogg` `.aifc`  

## License
This software is not guaranteed. Please see [LICENSE](LICENSE) for details.
