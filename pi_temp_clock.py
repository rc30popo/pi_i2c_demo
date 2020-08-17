#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Raspberry PI用
#    キャラクタ液晶 ACM1602と気圧センサーLPS25Hを利用したデモ
#
#  Rev.0.3 2020/08/17 SIGTERMで終了する様実装(バックグラウンド実行:nohup対応)

import time,smbus,sys,datetime
import signal
from ctrl_acm1602 import ctrl_acm1602,ctrl_acm1602_error
from ctrl_lps25h import ctrl_lps25h,ctrl_lps25h_error

# 終了処理
def finish(message):
    signal.setitimer(signal.ITIMER_REAL,0)
    acm1602.clear_display()
    acm1602.write_string('Terminated!!')
    print(message)
    time.sleep(1)
    acm1602.clear_display()
    acm1602.write_string('Bye!')
    print('Exit')
    sys.exit(0)

# SIGTERMハンドラ
def sigtermHandler(signum,frame):
    finish('SIGTERM received!!')

# 1秒毎起床するハンドラ
def intervalHandler(signum,frame):
    global acm1602
    global lps25h
    acm1602.return_home()
    cur_press = lps25h.get_pressure()
    cur_temp = lps25h.get_temp()
    dt_now = datetime.datetime.now()
    time_str = dt_now.strftime('%m/%d %H:%M:%S')
    press_temp_str = '%5.1fC,%6.1fhPa' % (cur_temp,cur_press)
    acm1602.write_string(time_str)
    acm1602.set_cursor(0,1)
    acm1602.write_string(press_temp_str)

i2c_channel = 1 # Raspberry PI2に合わせて1,適宜修正の事
i2c = smbus.SMBus(i2c_channel)

# キャラクタ液晶 ACM1602初期化
acm1602 = ctrl_acm1602(i2c)
acm1602.ctrl_display(1,0,0)
acm1602.clear_display()

# 気圧センサー LPS25H初期化
lps25h_addr = 0x5C # LPS25HのSDAピンをGNDに接続した場合,VDDに接続した場合は0x5Dとする事
try:
    lps25h = ctrl_lps25h(i2c,lps25h_addr)
except ctrl_lps25h_error as e:
    print(e)
    exit(1)

# 開始メッセージ
acm1602.write_string('Activating..')
# 各秒の開始から10ms以内を待ち
while True:
    dt_now = datetime.datetime.now()
    if dt_now.microsecond < 10000:
        break

# SIGTERMハンドラを設定
signal.signal(signal.SIGTERM,sigtermHandler)
# インターバル起床するハンドラを設定
signal.signal(signal.SIGALRM,intervalHandler)
signal.setitimer(signal.ITIMER_REAL, 1, 1)


# キーボード割り込み待ちループ
try:
    while True:
#        acm1602.clear_display()
#        acm1602.return_home()
#        cur_press = lps25h.get_pressure()
#        cur_temp = lps25h.get_temp()
#        dt_now = datetime.datetime.now()
#        time_str = dt_now.strftime('%m/%d %H:%M:%S')
#        press_temp_str = '%5.1fC,%6.1fhPa' % (cur_temp,cur_press)
#        acm1602.write_string(time_str)
#        acm1602.set_cursor(0,1)
#        acm1602.write_string(press_temp_str)
        time.sleep(600)

except KeyboardInterrupt:
    finish('\nCTRL-C pressed!!')
#    signal.setitimer(signal.ITIMER_REAL,0)
#    acm1602.clear_display()
#    acm1602.write_string('Terminated!!')
#    print('\nCTRL-C pressed!!')
#    time.sleep(1)
#    acm1602.clear_display()
#    acm1602.write_string('Bye!')
#    print('Exit')
#    sys.exit(0)


