
from machine import Pin,UART,Timer
import micropython
import sys
import time

import lib_bme280_float as bme280
from lib_lsm9ds1 import LSM9DS1

print('start')

timercount = 0
isFlag1=False

# コマンドラインに文字を出力する関数
def timer_run(t):
    global timercount, isFlag1,bmedata,accdata,gyrdata,magdata #グローバル変数にアクセスするためglobal キーワードで明示
    timercount =  timercount + 1
    start = time.ticks_ms() # ミリ秒カウンター値を取得
    bmedata = bme.values
    accdata = lsm.read_accel()
    gyrdata = lsm.read_gyro()
    magdata = lsm.read_magnet()
    delta = time.ticks_diff(time.ticks_ms(), start) # 時差を計算
    
    if timercount % 10 == 0:
        print("delta:",delta)
        isFlag1=True
    #print("acc",lsm.read_accel(),", tmp",bme.values_float[0])
    return


def timerinit():
    micropython.alloc_emergency_exception_buf(50)# 割り込み処理中の例外を作成するための設定
    timer_base = Timer()# タイマーを作成
    # タイマーを初期化して、周期的にコマンドラインに文字を出力する
    timer_base.init(mode=Timer.PERIODIC, freq=10, callback=timer_run)
    #タイマーが同時に作動した場合の挙動がよくわからないため一旦タイマーは1つだけ、そこまで時間が重要でない処理はフラグとIF文で
    #呼び出した関数内の処理はできるだけ短く
    return timer_base


def seninit():
    i2c = machine.I2C(id=0, sda=machine.Pin(4), scl=machine.Pin(5))
    bme = bme280.BME280(i2c=i2c)
    lsm = LSM9DS1(i2c)
    print('init end')
    return i2c,bme,lsm


bmedata = 0
lsmdata = 0

print("begin_init")
chkpin = Pin(25,machine.Pin.OUT)
chkpin.value(1)
"""
line = sys.stdin.readline()
if not (line.startswith("run")):
    print("stop code exit")
    sys.exit()
"""
i2c,bme,lsm = seninit()
timer_base= timerinit()
print("start_timer")
uart1 = UART(1, baudrate=115200,tx=Pin(8),rx=Pin(9))
print('end_init')
chkpin.value(0)
print('run')


while True:
    if isFlag1==True:#タイマ代わり
        uart1.write("count:"+str(timercount))
        print("tt",timercount)
        print(str(bmedata))
        print(accdata,"\n",gyrdata,"\n",magdata)
        isFlag1=False

    data = uart1.read()
    if data != None:
        chkpin.toggle()#RP2限定?
        if data.find('temp')>=0:
            uart1.write(bmedata)
        elif data.find('acc')>=0:
            uart1.write("accd:",lsm.read_accel())
        else:
            uart1.write("notcommand")
#
