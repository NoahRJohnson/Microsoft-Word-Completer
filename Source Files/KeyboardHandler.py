   
import win32api
import win32con
import win32console
import win32gui

import pythoncom, pyHook

import SendKeys

import os

import thread
import threading

import sys

from sets import Set

class KeyboardHandler(object):
    '''
        Reacts to each word being typed and blocks [Tab] to send the suggested
        word to the active window without indenting.
    '''

    def __init__(self, WordCompleter, gui_Q, SPACES, DCM):
        #WordCompleter and WSGui are objects
        
        self.abc = Set([65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,
                        83,84,85,86,87,88,89,90,97,98,99,100,101,102,103,104,105,
                        106,107,108,109,110,111,112,113,114,115,116,117,118,119,
                        120,121,122])

        self.WC = WordCompleter

        self.buffer = ''
        self.suggest_word = ''
        self.spaces = SPACES

        self.finished = False

        self.GUI_q = gui_Q

        self.DCM = DCM
        



    def begin(self):
        self.hm = pyHook.HookManager()
        self.hm.KeyDown = self.OnKeyboardEvent
        self.hm.HookKeyboard()
        pythoncom.PumpMessages()
        

    def OnKeyboardEvent(self, event):
        ''' Callback function, called when a key is pressed.
            Runs many times, so it needs to be fast. Thus we use a set lookup.
        '''
        if self.finished:
            self.end()
            return False
        
        else:
            if 'Microsoft Word' in event.WindowName:

                if event.Ascii in self.abc:
                    key = chr(event.Ascii)
                    self.buffer += key
                    if not self.DCM:
                        self.suggest_word = self.WC.find_mfw(self.buffer)
                        self.GUI_q.put(self.suggest_word, block=False)
            
                elif event.Ascii == 32: #if the key is Space
                    if self.buffer != '' :
                        self.WC.add_word(self.buffer)
                        self.buffer = ''
                        if not self.DCM:
                            self.suggest_word = self.WC.find_mfw(self.buffer)
                            self.GUI_q.put(self.suggest_word, block=False)
            
                elif event.Ascii == 8 : #if the key is [backspace]
                    if self.buffer != '':
                        self.buffer = self.buffer[:-1] #remove the last letter
                        self.WC.clear_current_words()
                        if not self.DCM:
                            self.suggest_word = self.WC.find_mfw(self.buffer)
                            self.GUI_q.put(self.suggest_word)
                    
                elif event.Ascii == 127 : #if the key is [del]
                    #delete key comes in as ascii value of 0 for some reason?
                    pass #figure something out? this feature wanted, not needed
            
                elif event.Ascii == 9: #if the key is [tab]
                    if self.suggest_word != '' and not self.DCM:
                        # Flash the text blue
                        self.GUI_q.put(1, block=False)

                        # Give the word to the word completer to bump up freq.
                        self.WC.add_word(self.suggest_word)

                        # Unhook the keyboard so that this callback isn't called
                        # when keys are sent.
                        self.hm.UnhookKeyboard()

                        # Send the keystrokes
                        keys = self.suggest_word[len(self.buffer):]
                        SendKeys.SendKeys(keys, pause=0)
                        if self.spaces:
                            SendKeys.SendKeys('{SPACE}', pause=0)

                        # Reset the buffer
                        self.buffer = ''

                        # Check for next word based on prefix search.
                        self.suggest_word = self.WC.find_mfw(self.buffer)
                        self.GUI_q.put(self.suggest_word, block=False)

                        self.hm.HookKeyboard()

                        #Block [Tab] from indenting
                        return False
                    
        return True

    def set_to_end(self): # Used to end program, working around threading issue.
        self.finished = True

    def set_spaces(self, spc):
        '''
        Workaround to set option for tab to add a space after inserting
        the word. Used since this class can't poll -- it hangs.
        '''
        self.spaces = spc

    def set_DCM(self, dcm):
        self.DCM = dcm
        
    def end(self):
        self.hm.UnhookKeyboard()
        self.GUI_q.put(0, block=False)
        self.WC.end()

        # It is important that this is only called by KbH's thread.
        win32gui.PostQuitMessage(1)

        
