# -*- coding:utf-8 -*-
import pythoncom
import pyHook
from pymouse import *
from pykeyboard import *
import ctypes
import pyautogui
import json
import os
import sys
import pyperclip
import time
import threading

def IsZhInput(words):
    bpmf = [49, 113, 97, 122, 50, 119, 115, 120, 101,\
     100, 99, 114, 102, 118, 53, 116, 103, 98, 121, 104, 110]
    iwu = [117, 106, 109]
    aouh = [56, 105, 107, 44, 57, 111, 108, 46, 48, 112, 59, 47]
    tone = [32, 54, 51, 52, 55]
    if len(words) == 2:
        if words[0] in [53, 116, 103, 98, 121, 104, 110, 117, \
                        106, 109, 56, 105, 107, 44, 57, 111, \
                        108, 46, 48, 112, 59, 45]:
            if words[1] in tone:
                return True
    if len(words) == 3:
        if (words[0] in bpmf) and (words[1] in iwu + aouh) and (words[2] in tone):
            return True
    if len(words) == 3:
        if (words[0] in iwu) and (words[1] in aouh) and (words[2] in tone):
            return True
    if len(words) == 4:
        if (words[0] in bpmf) and (words[1] in iwu) and (words[2] in aouh) and (words[3] in tone):
            return True
    return False


def IsZhInputs(alist):
    # type: (list) -> int
    if len(alist) >= 8:
        if IsZhInput(alist[-4:]) and IsZhInput(alist[-8:-4]):
            return 8
    if len(alist) >= 7:
        if IsZhInput(alist[-3:]) and IsZhInput(alist[-7:-3]):
            return 7
        elif IsZhInput(alist[-4:]) and IsZhInput(alist[-7:-4]):
            return 7
    if len(alist) >= 6:
        if IsZhInput(alist[-2:]) and IsZhInput(alist[-6:-2]):
            return 6
        elif IsZhInput(alist[-3:]) and IsZhInput(alist[-6:-3]):
            return 6
        elif IsZhInput(alist[-4:]) and IsZhInput(alist[-6:-4]):
            return 6
    if len(alist) >= 5:
        if IsZhInput(alist[-2:]) and IsZhInput(alist[-5:-2]):
            return 5
        elif IsZhInput(alist[-3:]) and IsZhInput(alist[-5:-3]):
            return 5
    if len(alist) >= 4:
        if IsZhInput(alist[-2:]) and IsZhInput(alist[-4:-2]):
            return 4

    return 0


if not os.path.exists('./EnWordBase.json'):
    print 'EnWordBase.json not found!'
    sys.exit()

with open('EnWordBase.json', 'r') as file2:
    ewb = json.load(file2)
file2.close()
ewords = ewb['words']


'''
def IsZhSingle(alist):
    # type: (list) -> int
    if len(alist) >= 4:
        if IsZhInput(alist[-2:]):
            return True
        elif IsZhInput(alist[-3:]):
            return True
        elif IsZhInput(alist[-4:]):
            return True
    if len(alist) >= 3:
        if IsZhInput(alist[-2:]):
            return True
        elif IsZhInput(alist[-3:]):
            return True
    if len(alist) >= 2:
        if IsZhInput(alist[-2:]):
            return True
    return False

def extZh(alist):
    if len(alist) >= 6:
        if not (IsZhSingle(alist[:-1]) or IsZhSingle(alist[:-2]) or IsZhSingle(alist[:-3])):
            return False
    return True
'''

def extEn(sus):
    if sus in ewords:
        return True
    else:
        return False

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
    if event.MessageName in ["mouse left down", "mouse right down"]:
        t = threading.Thread(target=MouseEventThread)
        t.start()
    return True

def OnKeyboardEvent(event):
    global InputType, ProgramPress, cur_words, cur_keys, cycle, susword, wn, shift_pressed, ctrl_pressed, clipboard, clipindex, v_open
    if event.MessageName=='key up':# and not (event.KeyID in [161, 160]):event.Ascii != 0:
        if  (event.KeyID in [161, 160]):
            shift_pressed=0
            return True
        elif (event.KeyID in [162, 163]):
            ctrl_pressed=0
            return True
        else:
            return True

    bpmf = [49, 113, 97, 122, 50, 119, 115, 120, 101, 100, 99, 114, 102, 118, 116, 103, 98, 121, 104, 110]
    iwu = [117, 106, 109]
    aouh = [56, 105, 107, 44, 57, 111, 108, 46, 48, 112, 59, 47]
    tone = [32, 54, 51, 52, 55]
    pixel=(1683, 1063)
    if wn!=event.WindowName:
        wn=event.WindowName
        cur_words = []
        cur_keys = []
        susword = ""
        cycle = ""
    # Input is human
    if (ProgramPress == 0):
        if (event.KeyID not in [38, 40]):
            v_open = 0
        elif v_open == 1:
            if (event.KeyID == 38):
                if not 0 < clipindex <= (len(clipboard)-1):
                    return False
                ProgramPress = (len(clipboard[clipindex])+2)
                for i in range(len(clipboard[clipindex])):
                    k.tap_key('\b')
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
                ProgramPress = (len(clipboard[clipindex])+2)
                for i in range(len(clipboard[clipindex])):
                    k.tap_key('\b')
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
        if (event.KeyID in [161, 160]):
            shift_pressed=1
        if (event.KeyID in [161, 160]) and len(susword) > 2:
            #print 'Shift!'
            im = pyautogui.screenshot()
            if im.getpixel(pixel)[1]>=200:
                InputType = 1
            else:
                InputType = 0
            if InputType == 1:
                #print susword,'add to base!'
                ewb['words'].append(susword)
                with open('EnWordBase.json', 'w') as file1:
                    json.dump(ewb, file1)
                file1.close()
            #print event.Key
            cur_words = []
            cur_keys = []
            susword=""
            return True
        elif (event.Ascii == 8):
            if len(cur_keys) > 0:
                del cur_keys[-1]
            if len(cur_words) > 0:
                del cur_words[-1]
            if len(susword) > 0:
                susword=susword[:-1]
            if len(cycle) > 0:
                cycle=cycle[:-1]
        elif (event.Ascii == 8) and len(cur_words) == 0:
            #print event.Key
            return True
        elif (event.Ascii in [13, 0, 9]):
            #print event.Key
            cur_words = []
            cur_keys = []
            susword = ""
            cycle = ""
            return True
        elif ctrl_pressed == 1:
            if event.Ascii in [99, 120]:
                tbj=threading.Thread(target=copyclip)
                tbj.start()
                return True
            if event.KeyID == 86:
                v_open = 1
                return True
        else:
            if len(susword)>0:
                if susword[-1]==' ':
                    susword = ""
            cur_words.append(event.Ascii)
            cur_keys.append(chr(event.Ascii))
            susword=''.join([susword,chr(event.Ascii)])
            cycle = ''.join([cycle, chr(event.Ascii)])
            if len(cycle) > 20:
                cycle = cycle[-20:]
        #print event, event.Ascii, cur_words
        #print susword, cur_keys

        im = pyautogui.screenshot()
        if im.getpixel(pixel)[1]>=200:
            InputType = 1
        else:
            InputType = 0

        # Input is En
        if (InputType == 0):
            EnKey = [114, 102, 118, 98, 103, 116, 121,
                     104, 110, 109, 106, 117, 105, 107, 108, 111, 112,
                     122, 97, 113, 119, 115, 120, 99, 100, 101]
            # NumKey=[48, 57, 56, 55, 54, 53, 52, 51, 50, 49]
            if shift_pressed == 1:
                cur_keys = []
                cur_words = []
                if event.Ascii not in EnKey:
                    susword = ''

            if len(cur_keys) > 0:
                flag2=0
                for i in range(len(susword)):
                    if extEn(susword[i:]):
                        cur_words = []
                        cur_keys = []
                        susword = ""
                        flag2=1
                if flag2==0:
                    for i in range(len(cycle)):
                        if extEn(cycle[i:]):
                            cur_words = []
                            cur_keys = []
                            susword = ""
            if (cur_words[-4:] == [122, 120, 99, 118]):
                ctypes.windll.user32.PostQuitMessage(0)

            temp=IsZhInputs(cur_words)
            if temp>0:
                #print('Shift to Zh')
                ProgramPress = (temp * 2)
                k.tap_key(k.shift_key)
                for i in range(temp - 1):
                    k.tap_key('\b')
                for i in cur_keys[-temp:]:
                    k.tap_key(i)
                cur_keys = []
                cur_words = []
                susword = ""
                return False
            else:
                return True
        # Input is Zh
        elif (InputType == 1):
            EnKey=[114, 102, 118, 98, 103, 116, 121, \
            104, 110, 109, 106, 117, 105, 107, 108, 111, 112, \
            122, 97, 113, 119, 115, 120, 99, 100, 101]
            #NumKey=[48, 57, 56, 55, 54, 53, 52, 51, 50, 49]
            if shift_pressed == 1:
                cur_keys=[]
                if event.Ascii not in EnKey:
                    susword=''
            '''
            if alt_pressed==1 and event.Ascii in NumKey:
                ProgramPress = 6
                alt_pressed = 0
                k.release_key(k.alt_key)
                k.tap_key(k.shift_key)
                k.tap_key(chr(event.Ascii))
                k.tap_key(k.shift_key)
                k.press_key(k.alt_key)
                alt_pressed = 1
            '''
            if (cur_words[-4:] == [122, 120, 99, 118]):
                ctypes.windll.user32.PostQuitMessage(0)
            if extEn(susword) and len(cur_keys)>1:
                #print susword,
                #print 'Shift to En'
                ProgramPress = (len(cur_keys)+2)
                k.tap_key(k.escape_key)
                k.tap_key(k.shift_key)
                #pyautogui.typewrite(susword)
                for i in cur_keys:
                    k.tap_key(i)
                cur_keys = []
                cur_words = []
                susword = ""
                return False
            if len(cur_keys) > 0:
                for i in range(len(cur_words)):
                    if IsZhInput(cur_words[i:]):
                        cur_words = []
                        cur_keys = []
                        susword = ""
            '''         [114, 102, 118, 98, 103, 116, 121, \
            104, 110, 109, 106, 117, 105, 107, 108, 111, 112, \ 
            122, 97, 113, 119, 115, 120, 99, 100, 101]  
            if IsZhInputs(cur_words)>0:
                susword = ""
                cur_keys = []
                cur_words = []
            '''
            if extEn(susword) and len(cur_keys)>1:
                #print susword,
                #print 'Shift to En'
                ProgramPress = (len(cur_keys)+2)
                k.tap_key(k.escape_key)
                k.tap_key(k.shift_key)
                #pyautogui.typewrite(susword)
                for i in cur_keys:
                    k.tap_key(i)
                cur_keys = []
                cur_words = []
                susword = ""
                return False

            return True

    #Input is computer
    else:
        ProgramPress -= 1
        #print "computer",
        #print event.Ascii, cur_words
        #print cur_keys
        return True


if __name__ == "__main__":
    print '+-----------------------------------------------------------+'
    print '|     The Program of Modifying Input Type Automatically     |'
    print "|   Copyright (C) 2017 Jexus Chuang. All rights reserved.   |"
    print '+-----------------------------------------------------------+'
    global k, InputType, ProgramPress, cur_words, cur_keys, cycle, susword, wn, shift_pressed, ctrl_pressed
    InputType = 0
    ProgramPress = 0
    cur_words = []
    cur_keys = []
    cycle=''
    susword=''
    wn=''
    shift_pressed=0
    ctrl_pressed=0
    clipboard=[]
    v_open=0
    clipindex = -1

    if os.path.exists('./clipboard.json'):
        with open('clipboard.json', 'r') as file3:
            e = json.load(file3)
            clipboard = e['words']
        file3.close()



    #m = PyMouse()
    k = PyKeyboard()

    # create a hook manager
    hm = pyHook.HookManager()
    # watch for all mouse events
    #hm.MouseAll = onMouseEvent
    # create a mouse hook
    #hm.HookMouse()
    # watch for all keyboard events
    hm.KeyDown = OnKeyboardEvent
    hm.KeyUp = OnKeyboardEvent
    # create a keyboard hook
    hm.HookKeyboard()
    # wait forever
    pythoncom.PumpMessages()
