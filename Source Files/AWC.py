
import os
import sys
from PyQt4 import QtGui
if os.name != 'nt':
    text = "This program currently only supports Windows operating systems. Shutting down."
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    error = QtGui.QMessageBox.information(w, "Error", text)
    sys.exit()

import win32console
import win32gui

import threading
import Queue
import time

import cPickle

from SysTrayIcon import SysTrayIcon
from Word_Completer import WordCompleter
from Word_Suggester_GUI import WSGui
from KeyboardHandler import KeyboardHandler
from OptionsWindow import OptionsWindow


# Global Queue variable.
GUI_Q = Queue.Queue()

# Set the name of the pickle files to store data in.
WC_pkl_file = "word_freq.pkl"
OW_pkl_file = "options.pkl"

def create_options_window(sysTrayIcon):
    app = QtGui.QApplication(sys.argv)
    OW = OptionsWindow(GUI_Q, sysTrayIcon, OW_pkl_file)
    app.exec_() 

def options(sysTrayIcon):
    options_page_t = threading.Thread(target=create_options_window, args=[
        sysTrayIcon])
    options_page_t.setDaemon(True)
    options_page_t.start()

if __name__ == '__main__':

    

    GUI_AVAILABLE_PLACEMENT = ["topright", "topleft", "bottomright"
                               ,"bottomleft"]
    


    OW_pkl_path = os.getcwd() + "/" + OW_pkl_file 
    if os.path.exists(OW_pkl_path):
        with open(OW_pkl_file, 'rb') as f:
            g_s, g_c, g_bg, g_txtc, g_f, dcm, prst, spc, p_n = cPickle.load(f)

        if g_s == "small":
            GUI_HEIGHT = 1
            GUI_WIDTH = 20
        elif g_s == "normal":
            GUI_HEIGHT = 2
            GUI_WIDTH = 40
        elif g_s == "large":
            GUI_HEIGHT = 3
            GUI_WIDTH = 60
        else:
            raise cPickle.UnpicklingError
        
        GUI_CORNER_PLACEMENT = g_c
        BG = g_bg
        TXTCOLOR = g_txtc

        if g_f == "small":
            FONTSIZE = 15
        elif g_f == "normal":
            FONTSIZE = 25
        elif g_f == "large":
            FONTSIZE = 35
        else:
            raise cPickle.UnpicklingError

        DCM = dcm
        PRST = prst
        SPACES = spc
        PREFIX_NUMBER = p_n
    else:
        # Set default values.
        GUI_HEIGHT = 2 #in text lines
        GUI_WIDTH = 40 #in text characters
        FONTSIZE = 25 #text font size
        GUI_CORNER_PLACEMENT = GUI_AVAILABLE_PLACEMENT[0]
        BG = "peachpuff"
        TXTCOLOR = "black"
        DCM = False
        PRST = False
        SPACES = True
        PREFIX_NUMBER = 2
        
    
    
    # Initialize the Word Completer and Keyboard Handler.
    WC = WordCompleter(WC_pkl_file, PREFIX_NUMBER)
    KbH = KeyboardHandler(WC, GUI_Q, SPACES, DCM)

    
    # SysTrayIcon argument parameters
    hovertext = "Automatic Word Completion"
    icon = os.getcwd() + "/" + "Speech_Bubble_Icon.ico"
    menu_options = (('Options', icon, options),)

    # Threaded class initialization
    SysTray = SysTrayIcon(KbH, icon, hovertext, menu_options,
                          default_menu_index=0)
    WSG = WSGui(BG, GUI_CORNER_PLACEMENT, DCM, FONTSIZE, TXTCOLOR, GUI_Q,
                GUI_HEIGHT, GUI_WIDTH)
                     
    # Start the SysTray and Word Suggester GUI Threads.
    SysTray.start()
    WSG.start()

    '''
    Begin the message loop waiting for keyboard input.
    This should continue until the tray icon tells the handler to shut down.
    '''
    KbH.begin()
    time.sleep(1) # Let threads clean up.            
