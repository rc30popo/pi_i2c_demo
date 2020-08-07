# pi_i2c_demo
## Copyright
Copyright (C) RC30-popo

## Overview
Raspberry PiのI2C端子を利用してI2C接続の気圧センサーLPS25Hから約1秒間隔で気圧と温度を読み出し、同じくI2C接続のキャラクタ液晶ACM1602NIに表示するデモです。
raspbian＋python3でこれらのI2Cデバイスを制御するサンプルコードです。

日経BP社のラズパイマガジン2015年秋号に紹介されていたデバイスですが、読者用に公開されているサンプルコードがpython2用なので、python3で使える制御用コードを自分で作りなおしました。

## SW Environment
以下の環境で開発、動作確認しています。
OS: Raspbian GNU/Linux 10 (buster)
Linux raspberrypi 5.4.51-v7+ #1332 SMP Tue Aug 4 18:34:21 BST 2020 armv7l

Python3.7

## HW
Raspberry Piシリーズ(Raspberry Pi 2 MODEL B+で動作確認しました)
I2C接続キャラクタ液晶 ACM1602NI
I2C接続気圧センサーLPS25H

キャラクタ液晶及び気圧センサーは秋月電子で販売されているものです。
気圧センサーはDIP化基盤付きのキットです。

LPS25HはI2Cアドレスとして0x5Cと0x5Dの2種類を選択可能ですが、本サンプルでは0x5Cで制御しています。(アドレスはLPS25HのSDOピンをGNDに繋ぐかVDDに繋ぐかでHW的に決定します)


## pythonスクリプト
3つのスクリプトから構成されています。

### pi_temp_clock.py
デモのメインプログラム。
CTRL-Cで終了します。
### ctrl_acm1602.py
ACM1602を制御するクラスライブラリ
テスト用のサンプルコードを含み、単体でも動作します。

### ctrl_lps25h.py
LPS25Hを制御するクラスライブラリ
テスト用のサンプルコードを含み、単体でも動作します。


## 制約事項
ACM1602,LPS25H共に基本的な制御のみを実装しており、エラー処理はほぼ入っていません。
正常系ワンパス程度の試験しか実施していないため、流用等される場合は自己責任でお願いします。
あくまでもお勉強用のサンプルソースです。

ACM1602,LPS25Hの制御用クラスライブラリについては特にドキュメントも用意していません。
短いコードですので、各々のデータシートと突き合わせて読めば使い方は判ると思います。
(というか、データシート読んで、理解して使って下さい)

## ライセンス
LICENSE.txtを参照してください。
