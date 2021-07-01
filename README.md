[English](README_EN.md)
# playlist-generator
本ツールは、m3u8形式のプレイリストファイルを自動で生成するツールです。  
[こちらのreleasesページ](https://github.com/takano536/playlist-generator/releases)からダウンロードすることができます。

## 特徴
本ツールは、ナンバリングされている音声ファイルのプレイリストを作成することに特化したツールです。  
Windows Explorerのような[自然順ソート](https://ja.wikipedia.org/wiki/%E8%87%AA%E7%84%B6%E9%A0%86)が可能です。

## 使い方
「PlaylistGenerator.exe」は、CLIソフトです。プレイリストに追加したい音声ファイルをドラッグ・アンド・ドロップするか、コマンドプロンプトを立ち上げ、以下のようなコマンドを打ち込み、使用してください。
```
PlaylistGenerator.exe --help
```
以下のコマンドは、プレイリストを作成するコマンドの一例です。
```
PlaylistGenerator.exe music.mp3 C:\Users\user\Music -o MyPlaylist --outfolder C:\Users\user\Documents
```
以下は、実行結果例です。
```
"MyPlaylist.m3u8" was created
path: C:\Users\user\Documents\MyPlaylist.m3u8
Successfully created m3u8 file
Press enter key to quit...
```
引数を何も指定せずに実行すると、利用可能なオプションが表示されます。
```
usage: main.py [-h] [-o OUTNAME] [--outfolder OUTFOLDER]
               [--sort {filename,foldername,date,ext,filename-desc,foldername-desc,date-desc,ext-desc}]
               [input ...]

positional arguments:
  input                 input music path or directory

optional arguments:
  -h, --help            show this help message and exit
  -o OUTNAME, --outname OUTNAME
                        output playlist filename
  --outfolder OUTFOLDER
                        save the output in a certain folder
  --sort {filename,foldername,date,ext,filename-desc,foldername-desc,date-desc,ext-desc}
                        how to sort songs (default=filename)
```

## コマンドラインオプション
本ソフトでは、以下のオプションを指定できます。
### 入力ファイル
```
<ファイルのパスやフォルダのパス>
必須の引数です。
ファイルのパスやフォルダのパスを複数指定することができます。
```
### 出力ファイル名
```
-o <出力ファイル名>, --outname <出力ファイル名>
ファイル名を指定します。
指定がなかった場合、プレイリストの先頭の曲名と同様の名前になります。
```
### 出力フォルダ
```
--outfolder <出力フォルダ先>
ファイルの出力先を指定します。
指定がなかった場合、すべての曲が含まれている、最も深い親フォルダに出力されます。
```
### 曲の並べ方
```
--sort <filename|foldername|date|ext|filename-desc|foldername-desc|date-desc|ext-desc>
曲の並べ方を指定します。
デフォルト値は「filename」です。
* filename        : ファイル名で昇順に並びます。
* foldername      : フォルダ名で昇順に並び、同一フォルダ内に複数のファイルが有る場合、ファイル名で昇順に並びます。
* date            : 作成日時で昇順に並びます。Windowsのみで動作します。
* ext             : 拡張子で昇順に並び、同一拡張子ファイルが複数ある場合、ファイル名で昇順に並びます。
* filename-desc   : ファイル名で降順に並びます。
* foldername-desc : フォルダ名で降順に並び、同一フォルダ内に複数のファイルが有る場合、ファイル名で降順に並びます。
* date-desc       : 作成日時で降順に並びます。Windowsのみで動作します。
* ext-desc        : 拡張子で降順に並び、同一拡張子ファイルが複数ある場合、ファイル名で降順に並びます。
```

## 注意
作成日時順ソートはWindowsでしか動作しません。  
本ツールで読み込める音声ファイルの種類は以下の通りになります。  
`.mp3` `.wma` `.oma` `.flac` `.wav` `.mp4` `.m4a` `.3gp` `.aif` `.aiff` `.afc` `.ogg` `.aifc`  

## ライセンス
本ソフトは無保証です。詳しくは[LICENSE](LICENSE)を御覧ください。
