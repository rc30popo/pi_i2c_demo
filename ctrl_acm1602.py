#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Raspberry PI用
#  キャラクター液晶 ACM1602NI制御クラス for python3系
#  copyright (C) RC30-popo: r.t.19891111@gmail.com
#  https://github.com/rc30popo
#

import time,smbus

class ctrl_acm1602_error(Exception):
    """ACM1602の制御エラー用例外"""
    pass

class ctrl_acm1602:
    def __init__(self,i2c):
        self.i2c = i2c
        self.acm1602_addr = 0x50 # ACM1602 I2Cスレーブアドレス=0x50固定
        self.disp = 1
        self.cursor_disp = 0
        self.cursor_blink = 0
        self.x = 0
        self.y = 0

        self.i2c.write_byte_data(self.acm1602_addr,0x00,0x06) # Cursor position increment
        time.sleep(0.1)
        self.i2c.write_byte_data(self.acm1602_addr,0x00,0x38) # Function Set,8bit,2line,5x8dots
        self.clear_display()
        self.return_home()
        self.ctrl_display(1,0,0)


    def clear_display(self):
        self.i2c.write_byte_data(self.acm1602_addr, 0x00, 0x01)
        time.sleep(0.01)
    
    def return_home(self):
        self.i2c.write_byte_data(self.acm1602_addr, 0x00, 0x02)
        self.x = 0
        self.y = 0
        time.sleep(0.01)
    
    def ctrl_display(self,disp,cursor_disp,cursor_blink):
        self.disp = disp
        self.cursor_disp = cursor_disp
        self.cursor_blink = cursor_blink
        self.i2c.write_byte_data(self.acm1602_addr, 0x00, 0x08 + (self.disp << 2) + (self.cursor_disp << 1) + self.cursor_blink)
        time.sleep(0.01)

    def set_cursor(self,x,y):
        if x < 0 or x > 15 or y < 0 or y > 1: # 範囲外
            return # TODO: ちゃんとエラーを返す
        cursor_addr = x + y * 0x40
        self.i2c.write_byte_data(self.acm1602_addr, 0x00, 0x80 + cursor_addr)
        self.x = x
        self.y = y

    def write_string(self,str):
        for i in range(len(str)):
            self.i2c.write_byte_data(self.acm1602_addr,0x80,ord(str[i]))
            self.x += 1
            if self.x == 16:
                self.x = 0
                self.y = 1 - self.y
                self.set_cursor(self.x,self.y)
#                time.sleep(0.001)

# テストコード
if __name__ == '__main__':
    i2c_channel = 1 # Raspberry PI2に合わせて1,適宜修正の事
    i2c = smbus.SMBus(i2c_channel)

    acm1602 = ctrl_acm1602(i2c)
    acm1602.ctrl_display(1,1,1)

    test_str = '0123456789ABCDEFGHIJKLMNOPQSTUVW'
    test_str1 = 'Hello New World'
    test_str2 = 'ACM1602'

    acm1602.write_string(test_str)
    time.sleep(3)
    acm1602.clear_display()
    acm1602.return_home()
    acm1602.write_string(test_str1)
    acm1602.set_cursor(0,1)
    acm1602.write_string(test_str2)


