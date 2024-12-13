
import machine
from machine import Timer
import micropython
import sys

import lib_bme280_float as bme280
from lib_lsm9ds1 import LSM9DS1

print('start')

timercount = 0
isFlag1=False

# コマンドラインに文字を出力する関数
def timer_run(t):
    global timercount, isFlag1 #グローバル変数にアクセスするためglobal キーワードで明示
    timercount =  timercount + 1
    if timercount % 300 == 0:
        isFlag1=True
    #print("acc",lsm.read_accel(),", tmp",bme.values_float[0])
    return


def timerinit():
    micropython.alloc_emergency_exception_buf(100)# 割り込み処理中の例外を作成するための設定
    timer_base = Timer()# タイマーを作成
    # タイマーを初期化して、周期的にコマンドラインに文字を出力する
    timer_base.init(mode=Timer.PERIODIC, freq=100, callback=timer_run)
    #タイマーが同時に作動した場合の挙動がよくわからないため一旦タイマーは1つだけ、そこまで時間が重要でない処理はフラグとIF文で
    #呼び出した関数内の処理はできるだけ短く
    return timer_base


def seninit():
    i2c = machine.I2C(id=0, sda=machine.Pin(4), scl=machine.Pin(5))
    bme = bme280.BME280(i2c=i2c)
    lsm = LSM9DS1(i2c)
    print('init end')
    return i2c,bme,lsm


print("begin_init")
line = sys.stdin.readline()
if not (line.startswith("run")):
    print("stop code exit")
    sys.exit()
i2c,bme,lsm = seninit()
timer_base= timerinit()
print("start_timer")
print('end_init')
print('run')


while True:
    if isFlag1==True:#タイマ代わり
        print("tt",timercount)
        print(bme.values)
        print("gyr",lsm.read_gyro())
        print("acc",lsm.read_accel())
        print("mag",lsm.read_magnet())
        isFlag1=False
        #
    #
#

        

