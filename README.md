AtamaTracker
============

## Requirements

- Python 2.x
- OpenCV
- numpy


## Usage

- リポジトリのルートディレクトリに移動
- `python track.py short.mov > result.txt` を実行
- 0 秒目の画像が現れるので、ウィンドウをアクティブにしてからトラックしたい点をクリック
- クリックし終わったら任意のキー（スペースキー）を押す
- 任意のキー（スペースキー）を押すごとにフレームが 0.1 秒ずつ進み，追跡結果がマーカーで表示される
    - 追加したい点を適宜クリックする
- 最後までいったら終了
- result.txt には各行（時刻，クリックした順のID，i座標（画像上端からの距離），j座標（画像左端からの距離））が格納される


## Customize

Some values can be set in a local config.ini file for individual projects.

### How To
1. Copy `config/defaults.ini` file.
2. Rename it to `config.ini`.
3. Place config.ini in the same directory of the source movie file,
   or the parent directory of the source.
4. Modify config.ini file following the instructions in it.
    - The values in the `config/defaults.ini` are used if you don't set values
      in your config.ini.


## How It Works

- マウスがクリックされた場所 (x, y) を `clicked_points` に格納
- 動画の各フレーム（0.1秒刻み）について
    - 現在のフレームと次のフレームを読み込む
    - 現在のフレームの `point` 地点周りのパタンに似たものを次のフレームから探す
    - `point` を移動後のものに書き換える
    - 結果の表示


## Coding Style

- Follow PEP8 guidelines
- Use Python3-compatible syntax as possible
- Use the cv2 API instead of the cv one as possible


## License

© 2015 Manabu TANGE.
© 2015 1024jp.

The source code is licensed under the terms of the MIT License. See the bundled [LICENSE](LICENSE) for details.