from pynput.keyboard import Key, Listener
import time
import win32api
import win32con
import ctypes
import os
import threading
from playsound import playsound

# 定义全局变量作为监测线程介入的开关
f = 0   # f key
q = 0   # quit
c = 0   # combo

# 屏幕中点坐标
cx = win32api.GetSystemMetrics(win32con.SM_CXSCREEN) // 2
cy = win32api.GetSystemMetrics(win32con.SM_CYSCREEN) // 2

# 信号量
semaphore_c = threading.Semaphore(0)    # combo

def on_pressq(key):
    #监听按键q
    global q
    if str(key)=="'"+'p'+"'":   # p键退出程序
        q = 1

def on_pressf(key):
    # 监听按键f
    global f
    if str(key)=="'"+'y'+"'":   # y键控制f连按
        time.sleep(0.5)
        f = 1 if f == 0 else 0  # f翻转
        if(f == 1):
            print("f按下")
            playsound(r"C:\Windows\Media\chimes.wav")
        else:
            print("f释放")
            playsound(r"C:\Windows\Media\notify.wav")

def on_pressc(key):
    global c
    #监听按键c
    if str(key)=="'"+'r'+"'":   # c键开始combo
        if(c == 0):
            semaphore_c.release()
            c = 1
            time.sleep(0.5)

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
            t2.stop()
            exit(0)

def press_c():
    def mouse_click(period):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, cx, cy, 0, 0)
        time.sleep(period)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, cx, cy, 0, 0)
    global c, q
    MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
    while True:
        semaphore_c.acquire()   # c press
        print("按下c")
        mouse_click(0.01)
        time.sleep(0.02)
        mouse_click(0.3)
        time.sleep(0.005)
        win32api.keybd_event(32, MapVirtualKey(70, 0), 0, 0)
        time.sleep(0.02)
        win32api.keybd_event(32, MapVirtualKey(70, 0), win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.5)
        c = 0
        


# 运行进程
l1 = Listener(on_press=on_pressf)
l2 = Listener(on_press=on_pressq)
l3 = Listener(on_press=on_pressc)
t1 = threading.Thread(target=press_f, name='sendThreadf')
t2 = threading.Thread(target=press_c, name='sendThreadc')
t2.setDaemon(True)  # 守护线程
l1.start()
l2.start()
l3.start()
t1.start()
t2.start()
