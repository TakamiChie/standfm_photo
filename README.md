# stand.fm用の背景画像をつくるやつ

stand.fm用の背景画像を作るスクリプトです。ご参考にどうぞ。

SeleniumのChromeDriverを使ってるので**Chromeのインストールが必須**です。
環境変数OneDriveConsumerを見ているので**法人版OneDriveと個人版OneDrive両方を設定している人**以外うまく動かないかもしれません(わざとKeyErrorを出すようにしてるので失敗しても問題は起こらないはず)。

## 必須要件

* Chromeがインストール済みであること
* (ひょっとしたら)OneDriveが法人向け、個人向け共にセットアップ済みであること
* Visual Studio Codeがインストール済みで。EasyLess拡張がインストール済みであること(cssを同梱していないため、1度lessファイルを編集してcssを作っておく必要がある)

## 推奨要件

* けいふぉんと([http://font.sumomo.ne.jp/font_1.html](http://font.sumomo.ne.jp/font_1.html))がインストール済みであること(中で使ってます)

## 画像のカスタマイズ

元画像はhtmlフォルダ内のbase.htmlです(これをヘッドレスChromeブラウザに読み込ませてスクリーンショットを撮ってる)。
このへんや付属のlessファイルをいじるとよいかも。

## つかいかた

`titlemaker.bat`を実行する。

すると自動的にヘッドレスChromeブラウザが立ち上がりスクリーンショットを撮影して落ちます。

撮影した画像はOneDriveのstand.fmフォルダに配置されます(フォルダがない場合は事前に作っておいてください)。

もし、そのフォルダにYYYY-MM-DD.mp3というファイルがあればそのタイトルタグから記事タイトルを勝手にとってきます。

## 使用モジュール

* jinja2 HTMLを作るのに使ってます
* selenium ヘッドレスChromeブラウザを立ち上げるのに使ってます
* chromedriver-binary Chrome用のSeleniumドライバをインストールするのに使ってます
* mutagen MP3タグを取得するのに使ってます
