# -*- coding:utf-8 -*-
import pythoncom
import pyHook
import pyautogui
from pymouse import *
from pykeyboard import *
import ctypes
import json
import os
import sys
import pyperclip
import time
import threading
import re

def copyclip():
    global clipindex
    timeout=time.time()+0.01
    while time.time() < timeout :
        pass
    print pyperclip.paste()
    if len(clipboard)>=100:
        del clipboard[0]
    clipboard.append(pyperclip.paste())
    clipindex=len(clipboard)-1
    print clipindex+1,
    print clipboard

def MouseEventThread():
    global v_open
    v_open = 0


def onMouseEvent(event):
    #global v_open
    #if v_open==0:
    #    return True
    if event.MessageName in ["mouse left down", "mouse right down"]:
        t = threading.Thread(target=MouseEventThread)
        t.start()
    return True

def rncount(string):
    rn=re.compile(r'\r\n')
    mo = rn.findall(string)
    return len(mo)

def OnKeyboardEvent(event):
    global ProgramPress, cycle, ctrl_pressed, clipboard, clipindex, v_open
    if event.MessageName=='key up':# and not (event.KeyID in [161, 160]):event.Ascii != 0:
        if  (event.KeyID in [161, 160]):
            shift_pressed=0
            return True
        elif (event.KeyID in [162, 163]):
            ctrl_pressed=0
            return True
        else:
            return True

    # Input is human
    if (ProgramPress == 0):
        if (event.KeyID not in [38, 40]):
            v_open = 0
        elif v_open == 1:
            if (event.KeyID == 38):
                if not 0 < clipindex <= (len(clipboard)-1):
                    return False
                ProgramPress = (len(clipboard[clipindex])+2-rncount(clipboard[clipindex]))
                pyautogui.typewrite('\b'*(len(clipboard[clipindex])-rncount(clipboard[clipindex])))
                clipindex-=1
                pyperclip.copy(clipboard[clipindex])
                k.press_key(k.control_key)
                k.press_key('v')
                k.release_key('v')
                k.release_key(k.control_key)
                return False
            elif (event.KeyID == 40):
                if not 0 <= clipindex < (len(clipboard)-1):
                    return False
                ProgramPress = (len(clipboard[clipindex])+2-rncount(clipboard[clipindex]))
                #for i in range(len(clipboard[clipindex])-rncount(clipboard[clipindex])):
                #    k.tap_key('\b')
                pyautogui.typewrite('\b'*(len(clipboard[clipindex])-rncount(clipboard[clipindex])))
                clipindex+=1
                pyperclip.copy(clipboard[clipindex])
                k.press_key(k.control_key)
                k.press_key('v')
                k.release_key('v')
                k.release_key(k.control_key)
                return False
            else:
                v_open = 0
                return True

        if (event.KeyID in [162, 163]):
            ctrl_pressed = 1
            return True
        elif ctrl_pressed == 1:
            if event.Ascii in [99, 120]:
                tbj=threading.Thread(target=copyclip)
                tbj.start()
                return True
            if event.KeyID == 86:
                v_open = 1
                return True
            return True
        else:
            cycle.append(event.Ascii)
            if len(cycle) > 4:
                cycle = cycle[-4:]
            if (cycle[:] == [122, 120, 99, 118]):
                with open('clipboard.json', 'w') as file1:
                    json.dump({'words':clipboard}, file1)
                file1.close()
                ctypes.windll.user32.PostQuitMessage(0)
            return True

    #Input is computer
    else:
        ProgramPress -= 1
        return True


if __name__ == "__main__":
    print '+-----------------------------------------------------------+'
    print '|             The Program of Multiple Clipboard             |'
    print "|   Copyright (C) 2017 Jexus Chuang. All rights reserved.   |"
    print '+-----------------------------------------------------------+'
    global ProgramPress, cycle, ctrl_pressed, v_open, clipindex, clipboard
    ProgramPress = 0
    cycle=[]
    ctrl_pressed=0
    clipboard=[]
    v_open=0

    if os.path.exists('./clipboard.json'):
        with open('clipboard.json', 'r') as file3:
            e = json.load(file3)
            clipboard = e['words']
        file3.close()

    clipindex = len(clipboard)-1



    m = PyMouse()
    k = PyKeyboard()

    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all mouse events
    hm.MouseAll = onMouseEvent
    # create a mouse hook
    hm.HookMouse()
    # watch for all keyboard events
    hm.KeyDown = OnKeyboardEvent
    hm.KeyUp = OnKeyboardEvent
    # create a keyboard hook
    hm.HookKeyboard()
    # wait forever
    pythoncom.PumpMessages()
