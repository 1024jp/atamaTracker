AtamaTracker
============

## Requirements

- Python 2.x
- OpenCV
- numpy


## Contents

- track.py：メインファイル
- modules/gui.py：マウスイベントと GUI 表示のためのモジュール
- modules/piv.py：パターンマッチングのモジュール（流体解析用）


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

- track.py 16 行目の `FIND_BUFFER` は捜索範囲の縦横ピクセル数
- track.py 17 行目の `PATTERN_SIZE` は捜索対象の縦横ピクセル数（パターンの大きさ）


## How It Works

- マウスがクリックされた場所 (x, y) を `clicked_points` に格納
- 動画の各フレーム（0.1秒刻み）について
    - 現在のフレームと次のフレームを読み込む
    - 現在のフレームの `point` 地点周りのパタンに似たものを次のフレームから探す
    - `point` を移動後のものに書き換える
    - 結果の表示


## Coding Style

- PEP8 に沿う
- できるだけ Python3 っぽく書く (実態は Python2 だけど


## License

© 2015 Manabu TANGE.
© 2015 1024jp.

The source code is licensed under the terms of the MIT License. See the bundled [LICENSE]() for details.