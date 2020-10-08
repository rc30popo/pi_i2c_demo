#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Raspberry PI用
#  SPI接続 ADコンバーターMCP3002制御ライブラリ
#  copyright (C) RC30-popo: r.t.19891111@gmail.com
#  https://github.com/rc30popo
#
#  MCP3002データシート入手先
#  https://akizukidenshi.com/download/ds/microchip/mcp3002.pdf

import spidev
import time

class ctrl_mcp3002:
    # コンストラクタ
    #   spidevのインスタンスを渡す
    def __init__(self,spi):
        self.spi = spi
        self.spi.max_speed_hz = 100000 # MAX clock 1MHz
        self.spi.mode = 0b00 # Mode 00
    
    # AD変換結果読み出し
    #   引数: ch - チャンネル番号 0もしくは1
    #   戻り値: 読み出し結果 0〜1023
    def read_ch(self,ch):
        cmd = 0x40 + ((2 + ch) << 4) + 8
#        print("cmd = " + hex(cmd))
        resp = self.spi.xfer2([cmd,0x00])
        value = (resp[0] * 256 + resp[1]) & 0x3ff
        return value

# テストコード
if __name__ == '__main__':

    spi = spidev.SpiDev()
    spi.open(0,0)

    test_cnt = 10 # 読み出しテスト回数

    mcp3002 = ctrl_mcp3002(spi)

    # Channel 0と1を1秒間間隔で10回読み出し
    for i in range(test_cnt):
        # 1秒待ち
        time.sleep(1)
        ch0_value = mcp3002.read_ch(0)
        ch1_value = mcp3002.read_ch(1)
        print("=== Test Count %d" % i)
        print("  channel0 = %d" % ch0_value)
        print("  channel1 = %d" % ch1_value)

    exit(0)
    

