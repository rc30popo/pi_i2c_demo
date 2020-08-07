#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Raspberry PI用
#  気圧センサー「LPS25H」制御クラス for python3系
#  copyright (C) RC30-popo: r.t.19891111@gmail.com
#  https://github.com/rc30popo
#
# LPS25Hデータシート参考
# http://www.ne.jp/asahi/o-family/extdisk/LPS331AP/LPS25H_DJP.pdf
            

import time,smbus

 

class ctrl_lps25h_error(Exception):
    """lps25hの制御エラー用例外"""
    pass

class ctrl_lps25h:
    SPD_1HZ = 1
    SPD_7HZ = 2
    SPD_12_5HZ= 3
    SPD_25HZ = 4
    def __init__(self,i2c,addr):
        self.i2c = i2c
        self.lps25h_addr = addr
        # Check WHO_AM_I register
        who_am_i = i2c.read_byte_data(self.lps25h_addr,0x0f )
        if who_am_i == 0xbd: # 正常値
            # 制御レジスタ1
            #  ・パワーダウン解除(bit 7=1b)
            #  ・出力間隔1Hz(bit 6-4=001b)
            i2c.write_byte_data(self.lps25h_addr,0x20,0x90 )
        else:
            raise ctrl_lps25h_error("Invalid response from lps25h(WHO_AM_I = %02xh" % who_am_i)
    def set_speed(self,speed):
        # speedはctrl_lps25h.SPD_1HZ,ctrl_lps25h.SPD_7HZ,ctrl_lps25h.SPD_12_5HZ,ctrl_lps25h.SPD25HZ
        # のいずれかを指定の事(エラーチェック省略)
        self.i2c.write_byte_data(self.lps25h_addr,0x20,0x80 | (speed << 4))
    def get_pressure(self):
        # レジスタ 28h,29h,2Ahを読みだす
        press_out_h = self.i2c.read_byte_data(self.lps25h_addr,0x2a)
        press_out_l = self.i2c.read_byte_data(self.lps25h_addr,0x29)
        press_out_xl = self.i2c.read_byte_data(self.lps25h_addr,0x28)
        press_out = (press_out_h << 16) + (press_out_l << 8) + press_out_xl
        press_ret = press_out / 4096
        return press_ret
    def get_temp(self):
        temp_out_h = self.i2c.read_byte_data(self.lps25h_addr, 0x2c )
        temp_out_l = self.i2c.read_byte_data(self.lps25h_addr, 0x2b )
        temp_out = (temp_out_h << 8) + temp_out_l
        if temp_out > 0x7fff:
            temp_out = temp_out - 0x10000
        temp_ret = 42.5 + (temp_out / 480)
        return temp_ret
    
# テストコード
if __name__ == '__main__':
    i2c_channel = 1 # Raspberry PI2に合わせて1,適宜修正の事
    i2c = smbus.SMBus(i2c_channel)
    lps25h_addr = 0x5C # LPS25HのSDOピンをGNDに接続した場合0x5C,VDDに接続した場合は0x5Dとする事

    test_cnt = 3 # 読み出しテスト回数
    try:
        lps25h = ctrl_lps25h(i2c,lps25h_addr)
    except ctrl_lps25h_error as e:
        print(e)
        exit(1)
    
    # 読み出し一発目が安定しないのでダミーリード
    cur_press = lps25h.get_pressure()
    cur_temp = lps25h.get_temp()

    for i in range(test_cnt):
        # 1秒待ち
        time.sleep(1)
        cur_press = lps25h.get_pressure()
        cur_temp = lps25h.get_temp()
        print("Read test[%d]" % i)
        print(" Barometric Press = %.1f hPa" % cur_press)
        print(" Temp = %.1f C" % cur_temp)

    exit(0)
