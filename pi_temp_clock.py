#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  Raspberry PI用
#    キャラクタ液晶 ACM1602と気圧センサーLPS25Hを利用したデモ
#
#  Rev.0.3 2020/08/17 SIGTERMで終了する様実装(バックグラウンド実行:nohup対応)
#  Rev.0.4 2020/08/19 記録データのCSVファイル出力追加
#  Rev.0.5 2021/05/03 2重起動防止追加

import time,smbus,sys,datetime
import signal
import argparse
from os import path
import subprocess

from ctrl_acm1602 import ctrl_acm1602,ctrl_acm1602_error
from ctrl_lps25h import ctrl_lps25h,ctrl_lps25h_error

# 2重起動防止処理
# 下記記事の丸写し
#  https://qiita.com/dev_colla/items/6ab765fc6daf2c2a2baa
def checkDupexec():
    file_name = path.basename(__file__)
    p1 = subprocess.Popen(["ps", "-ef"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", file_name], stdin=p1.stdout, stdout=subprocess.PIPE)
    p3 = subprocess.Popen(["grep", "python"], stdin=p2.stdout, stdout=subprocess.PIPE)
    p4 = subprocess.Popen(["wc", "-l"], stdin=p3.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()
    p2.stdout.close()
    p3.stdout.close()
    output = p4.communicate()[0].decode("utf8").replace('\n','')

    if int(output) != 1:
        print('Duplicated execution!! Exit!')
        exit(1)

# 終了処理
def finish(message):
    global acm1602
    global lps25h
    global output_f
    signal.setitimer(signal.ITIMER_REAL,0)
    if output_f != None:
        output_f.close()
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
    global output_f
    global rec_interval_cnt
    global rec_interval

    acm1602.return_home()
    cur_press = lps25h.get_pressure()
    cur_temp = lps25h.get_temp()
    dt_now = datetime.datetime.now()
    time_str = dt_now.strftime('%m/%d %H:%M:%S')
    press_temp_str = '%5.1fC,%6.1fhPa' % (cur_temp,cur_press)
    acm1602.write_string(time_str)
    acm1602.set_cursor(0,1)
    acm1602.write_string(press_temp_str)
    if output_f != None: # CSVファイル出力
        if rec_interval_cnt == 0:
            time_str2 = dt_now.strftime('%Y-%m-%d %H:%M:%S')
            csv_str = '%s,%.1f,%.1f\n' % (time_str2,cur_temp,cur_press)
            output_f.write(csv_str)
        rec_interval_cnt += 1
        if rec_interval_cnt == rec_interval:
            rec_interval_cnt = 0

# 2重起動チェック
checkDupexec()

# デフォルト引数
rec_interval = 60 # レコードインターバル60秒
output_file = None

# レコードインターバル用カウンタ
rec_interval_cnt = 0

# 引数チェック
parser = argparse.ArgumentParser(prog='pi_temp_clock.py',description='Temperature and Barometric pressure sensing program.')
parser.add_argument('-o','--output',help='Output Filename',required=False)
parser.add_argument('-r','--rec_interval',help='Record interval(sec)',type=int,required=False)

args = parser.parse_args()

if args.output != None:
    output_file = args.output
if args.rec_interval != None:
    rec_interval = args.rec_interval

print('==pi_temp_clock start==')
if output_file != None:
    print('Output File = ' + output_file)
    print('Record Interval = %d(sec)' % rec_interval)



# I2C初期化
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

# 記録ファイルオープン
output_f = None
if output_file != None:
    try:
        output_f = open(output_file,'w')
    except OSError as e: # ファイルオープンエラー
        output_f = None # 念のため
        print(e)
    else: # ファイルオープン成功,ヘッダ書き込み
        output_f.write('time,temp,baro\n')


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


