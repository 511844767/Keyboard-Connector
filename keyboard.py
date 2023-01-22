from pynput.keyboard import Key, Listener
import time
import win32api
import win32con
import ctypes
import os
import threading
from playsound import playsound

# 定义键的信号量对象
semaphoref = threading.Semaphore(0)
semaphoreq = threading.Semaphore(0)

# 定义全局变量作为监测线程介入的开关
f = 0   # f key
q = 0   # quit

def on_pressq(key):
    #监听按键q
    global q
    if str(key)=="'"+'p'+"'":   # p键退出程序
        q = 1

def on_pressf(key):
    # 监听按键f
    global f
    if str(key)=="'"+'r'+"'":   # r键控制f连按
        time.sleep(0.5)
        f = 1 if f == 0 else 0  # f翻转
        if(f == 1):
            print("f按下")
            playsound('./on.mp3')
        else:
            print("f释放")
            playsound('./off.mp3')

def press_f():
    global f, q
    MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
    while True:
        if(f == 1): # press f
            win32api.keybd_event(70, MapVirtualKey(70, 0), 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(70, MapVirtualKey(70, 0), win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.1)
        if(q == 1): # quit
            break


# 运行进程
t1 = Listener(on_press=on_pressf)
t2 = Listener(on_press=on_pressq)
t3 = threading.Thread(target=press_f, name='sendThreadf')
t1.start()
t2.start()
t3.start()
