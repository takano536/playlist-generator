# playlist-generator
本ツールは、m3u8形式のプレイリストファイルを自動で生成するツールです。
[こちらのreleasesページ](https://github.com/takano536/playlist-generator/releases)からダウンロードすることができます。

## 使い方
「PlaylistGenerator.exe」は、CLIソフトです。プレイリストに追加したい音声ファイルをドラッグ・アンド・ドロップするか、コマンドプロンプトを立ち上げ、以下のようなコマンドを打ち込み、使用してください。
```
PlaylistGenerator.exe --help
```
以下のコマンドは、プレイリストを作成するコマンドの一例です。
```
PlaylistGenerator.exe music.mp3 C:\Users\user\Music song.mp3 -o MyPlaylist --outfolder C:\Users\user\Documents
```
実行後、実行結果が出力されます。
```
"MyPlaylist.m3u8" was created
path: C:\Users\user\Documents\MyPlaylist.m3u8
Successfully created m3u8 file
Press enter key to quit...
```

## コマンドラインオプション
本ソフトでは、以下のオプションを指定できます。
```
-o <出力ファイル名>, --outname <出力ファイル名>
ファイル名を指定します。
指定がなかった場合、プレイリストの先頭の曲名と同様の名前になります。
```
```
--outfolder <出力フォルダ先>
ファイルの出力先を指定します。
指定がなかった場合、すべての曲が含まれている、最も深い親フォルダに出力されます。
```
```
--sort <filename|foldername|date|ext|filename-desc|foldername-desc|date-desc|ext-desc>
曲の並び方を指定します。
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

## License
本ソフトは無保証です。詳しくは[LICENSE](https://github.com/takano536/playlist-generator/blob/master/LICENSE)を御覧ください。
