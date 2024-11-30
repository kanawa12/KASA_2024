
import machine
from machine import Timer
import micropython
import sys

import lib_bme280_float as bme280
from lib_lsm9ds1 import LSM9DS1

print('start')


def timerinit():
    micropython.alloc_emergency_exception_buf(100)# 割り込み処理中の例外を作成するための設定
    timer = Timer()# タイマーを作成
    # タイマーを初期化して、周期的にコマンドラインに文字を出力する
    timer.init(mode=Timer.PERIODIC, freq=1, callback=timer_run)
    return timer

def seninit():
    i2c = machine.I2C(id=0, sda=machine.Pin(4), scl=machine.Pin(5))
    bme = bme280.BME280(i2c=i2c)
    lsm = LSM9DS1(i2c)
    print('init end')
    return i2c,bme,lsm


# コマンドラインに文字を出力する関数
def timer_run(timer):
    print("Timer interrupt triggered")
    print(bme.values_float[0])
    print("gyr",lsm.read_gyro())
    print("acc",lsm.read_accel())
    print("mag",lsm.read_magnet())




timer = timerinit()
print("timer_start")
i2c,bme = seninit()
print('init_fin')
print('run')

