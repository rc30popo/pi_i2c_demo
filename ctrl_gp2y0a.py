#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Raspberry PI用
#  赤外線測距モジュールGP2Y0A+SPI接続 ADコンバーターMCP3002制御ライブラリ
#  copyright (C) RC30-popo: r.t.19891111@gmail.com
#  https://github.com/rc30popo
#
#  データシート
#  https://akizukidenshi.com/download/ds/sharp/gp2y0a21yk_e.pdf
#  https://akizukidenshi.com/download/ds/sharp/gp2y0a_gp2y0d_series_appl_e.pdf

import spidev
import time

from ctrl_mcp3002 import ctrl_mcp3002


class ctrl_gp2y0a25:
    # MCP3002のVREF: 3.3V - 回路構成に合わせて修正のこと
    vref_mcp3002 = 3.3
    # 距離-電圧対応テーブル
    #   数値はかなりラフなので、きちんとデータシート見て調整のこと
    dist_table = ((7,3.0),
                  (10,2.25),
                  (15,1.7),
                  (20,1.3),
                  (25,1.1),
                  (30,0.9),
                  (35,0.8),
                  (40,0.75),
                  (45,0.7),
                  (50,0.6),
                  (55,0.55),
                  (60,0.5),
                  (70,0,45),
                  (80,0.4))
    # コンストラクタ
    #   spidevのインスタンスを渡すとMCP3002に接続するチャンネル番号を渡す
    #    spi: SpiDevのインスタンス
    #    ch : MCP3002のチャンネル番号
    def __init__(self,spi,ch):
        self.spi = spi
        self.channel = ch
        self.mcp3002 = ctrl_mcp3002(spi)
        self.tbl_len = len(ctrl_gp2y0a25.dist_table)
    # 測定: 距離をcm単位で返却
    def read_dist(self):
        voltage = self.mcp3002.read_ch(self.channel) / 1023 * ctrl_gp2y0a25.vref_mcp3002
        hit = -1
        for i in range(0,self.tbl_len - 1):
            if voltage <= ctrl_gp2y0a25.dist_table[i][1] and voltage >= ctrl_gp2y0a25.dist_table[i + 1][1]:
                hit = i
                break
        
        if hit == -1:
            dist = -1
        else:
            w = ctrl_gp2y0a25.dist_table[hit + 1][0] - ctrl_gp2y0a25.dist_table[hit][0]
            h0 = ctrl_gp2y0a25.dist_table[hit][1] - ctrl_gp2y0a25.dist_table[hit + 1][1]
            h1 = ctrl_gp2y0a25.dist_table[hit][1] - voltage
            dist = ctrl_gp2y0a25.dist_table[hit][0] + h1 / h0 * w
        return dist

# テストコード
#  MCP3002のチャンネル番号を1で設定しているので、ch0に繋ぐ場合はchを書き換えのこと
if __name__ == '__main__':

    ch = 1 # AD変換器 MCP3002の接続先チャンネル番号
    spi = spidev.SpiDev()
    spi.open(0,0)

    test_cnt = 10 # 読み出しテスト回数
    gp2y0a25 = ctrl_gp2y0a25(spi,ch)

    for i in range(test_cnt):
        # 1秒待ち
        time.sleep(1)
        dist = gp2y0a25.read_dist()
        print("=== Test Count %d" % i)
        print("  distance = %2.2f cm" % dist)


    exit(0)





    
