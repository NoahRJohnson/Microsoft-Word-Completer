'''
OptionsWindow.py
'''

import cPickle
import os
import sys

import _winreg
from PyQt4 import QtGui, QtCore


COLORS = ['alice blue', 'antique white', 'aquamarine', 'azure',
                  'beige', 'bisque', 'black', 'blanched almond', 'blue',
                  'blue violet', 'brown', 'burlywood', 'cadet blue',
                  'chocolate', 'coral', 'cornflower blue', 'cornsilk',
                  'cyan', 'dark blue', 'dark cyan', 'dark goldenrod',
                  'dark gray', 'dark green', 'dark grey', 'dark khaki',
                  'dark magenta', 'dark olive green', 'dark orange',
                  'dark orchid', 'dark red', 'dark salmon', 'dark sea green',
                  'dark slate blue', 'dark slate gray', 'dark slate grey',
                  'dark turquoise', 'dark violet', 'deep pink', 'deep sky blue',
                  'dim gray', 'dim grey', 'dodger blue', 'firebrick',
                  'floral white', 'forest green', 'gainsboro', 'ghost white',
                  'gold', 'goldenrod', 'gray', 'green', 'green yellow', 'grey', 
                  'honeydew', 'hot pink', 'indian red', 'ivory', 'khaki',
                  'lavender', 'lavender blush', 'lawn green', 'lemon chiffon',
                  'light blue', 'light coral', 'light cyan', 'light goldenrod',
                  'light goldenrod yellow', 'light gray',
                  'light green', 'light grey', 'light pink', 'light salmon',
                  'light sea green', 'light sky blue', 'light slate blue',
                  'light slate gray', 'light slate grey', 'light steel blue',
                  'light yellow', 'lime green', 'linen', 'magenta', 'maroon',
                  'medium aquamarine', 'medium blue', 'medium orchid',
                  'medium purple', 'medium sea green', 'medium slate blue',
                  'medium spring green', 'medium turquoise', 'medium violet red',
                  'midnight blue', 'mint cream', 'misty rose', 'moccasin',
                  'navajo white', 'navy', 'navy blue', 'old lace', 'olive drab',
                  'orange', 'orange red', 'orchid', 'pale goldenrod',
                  'pale green', 'pale turquoise', 'pale violet red',
                  'papaya whip', 'peach puff', 'peru', 'pink', 'plum',
                  'powder blue', 'purple', 'red', 'rosy brown', 'royal blue',
                  'saddle brown', 'salmon', 'sandy brown', 'sea green', 'seashell',
                  'sienna', 'sky blue', 'slate blue', 'slate gray', 'slate grey',
                  'snow', 'spring green', 'steel blue', 'tan', 'thistle', 'tomato',
                  'turquoise', 'violet', 'violet red', 'wheat', 'white', 'white smoke',
                  'yellow', 'yellow green']

class OptionsWindow(QtGui.QWidget):
    

    def __init__(self, Q, sysTrayIcon, pkl_file):
        super(OptionsWindow, self).__init__()

        self.q = Q
        self.pkl_filename = pkl_file
        cwd = os.getcwd()
        cwd.replace('/', '\\')
        exe_path = cwd + "\\" + "mwCompleter.exe"
        self.reg_data = "'" + exe_path + "'"

        self.systray = sysTrayIcon
        self.initUI()

    def initUI(self):

        # Set the available options that will be displayed.
        self.GUI_size_OPTIONS = ["small", "normal", "large"]
        self.GUI_corner_OPTIONS = ["topright", "topleft", "bottomright",
                                   "bottomleft"]
        self.GUI_bg_OPTIONS = COLORS
        self.GUI_txtcolor_OPTIONS = COLORS
        self.GUI_fontsize_OPTIONS = ["small", "normal", "large"]

        # Set default option values.
        self.GUI_size = self.GUI_size_OPTIONS[1]
        self.GUI_corner = self.GUI_corner_OPTIONS[0]
        self.GUI_bg = self.GUI_bg_OPTIONS[5]
        self.GUI_txtcolor = self.GUI_txtcolor_OPTIONS[6]
        self.GUI_fontsize = self.GUI_fontsize_OPTIONS[1]
        self.DCM = False
        self.program_startup = False
        self.spaces = True
        self.prefix_num = 2

        # Create labels to describe options
        self.GUI_size_lbl = QtGui.QLabel("Text window size")
        self.GUI_corner_lbl = QtGui.QLabel("Text window corner")
        self.GUI_bg_lbl = QtGui.QLabel("Text window color")
        self.GUI_txtcolor_lbl = QtGui.QLabel("Text color")
        self.GUI_fontsize_lbl = QtGui.QLabel("Text fontsize")
        self.prefix_num_lbl = QtGui.QLabel("Number of words before the word being typed\nthat the engine should take into account.")        
        
        # Create combo boxes(menus) to accept user option input.
        self.GUI_size_combo = QtGui.QComboBox(self)
        self.GUI_corner_combo = QtGui.QComboBox(self)
        self.GUI_bg_combo = QtGui.QComboBox(self)
        self.GUI_txtcolor_combo = QtGui.QComboBox(self)
        self.GUI_fontsize_combo = QtGui.QComboBox(self)
        # Create check boxes to accept user option input.
        self.DCM_cb = QtGui.QCheckBox("Data Collection Mode", self)
        self.DCM_cb.setToolTip("Let the program run silently in the background, while still building a database of frequent words off of your typing.")
        self.program_startup_cb = QtGui.QCheckBox("Start program on Windows Startup", self)
        self.program_startup_cb.setToolTip("Check this with DCM turned on, and in a few days you'll have a custom profile.")
        self.spaces_cb = QtGui.QCheckBox("Insert a space after your word is filled in", self)
        self.spaces_cb.setToolTip("Keeping this set allows for the fastest typing. Uncheck if you can't get used to it.")
        self.spaces_cb.toggle()
        self.prefix_num_LineEdit = QtGui.QLineEdit(self)

        # Add the different selectable options to the combo boxes.
        self.GUI_size_combo.addItems(self.GUI_size_OPTIONS)
        self.GUI_corner_combo.addItems(self.GUI_corner_OPTIONS)
        self.GUI_bg_combo.addItems(self.GUI_bg_OPTIONS)
        self.GUI_txtcolor_combo.addItems(self.GUI_txtcolor_OPTIONS)
        self.GUI_fontsize_combo.addItems(self.GUI_fontsize_OPTIONS)

                                      
        # Configure pre-set user options, if applicable.
        self.pkl_filename = "options.pkl"
        pkl_path = os.getcwd() + "/" + self.pkl_filename
        if os.path.exists(pkl_path):
            # Load user options.
            with open(self.pkl_filename, 'rb') as f:
                g_s, g_c, g_bg, g_txtc, g_f, dcm, prst, spc, p_n = cPickle.load(f)
                
            self.GUI_size_combo.setCurrentIndex(self.GUI_size_OPTIONS.index(g_s))
            self.GUI_corner_combo.setCurrentIndex(self.GUI_corner_OPTIONS.index(g_c))
            self.GUI_bg_combo.setCurrentIndex(self.GUI_bg_OPTIONS.index(g_bg))
            self.GUI_txtcolor_combo.setCurrentIndex(self.GUI_txtcolor_OPTIONS.index(g_txtc))
            self.GUI_fontsize_combo.setCurrentIndex(self.GUI_fontsize_OPTIONS.index(g_f))

            self.GUI_size = g_s
            self.GUI_corner = g_c
            self.GUI_bg = g_bg
            self.GUI_txtcolor = g_txtc
            self.GUI_fontsize = g_f
            if dcm == True:
                self.DCM = dcm
                self.DCM_cb.toggle()
            if prst == True:
                self.program_startup = prst
                self.program_startup_cb.toggle()
            if spc == False:
                self.spaces = spc
                self.spaces_cb.toggle()
            self.prefix_num = p_n
            self.prefix_num_LineEdit.setText(QtCore.QString(str(self.prefix_num)))
        else:
            # Set the default indexes for the combo boxes.
            self.GUI_size_combo.setCurrentIndex(1)
            self.GUI_corner_combo.setCurrentIndex(0)
            self.GUI_bg_combo.setCurrentIndex(5)
            self.GUI_txtcolor_combo.setCurrentIndex(6)
            self.GUI_fontsize_combo.setCurrentIndex(1)
            self.prefix_num_LineEdit.setText(QtCore.QString("2 (Default Value)"))
        
       
        # Find window width and height in pixels based on user's screen dimensions.
        screen = QtGui.QDesktopWidget().availableGeometry()
        self.screen_w = screen.width()
        self.screen_h = screen.height()
        self.width = self.screen_w / 3
        self.height = self.screen_h / 3
        self.pos_x = (self.screen_w / 2) - (self.width / 2)
        self.pos_y = (self.screen_h / 2) - (self.height / 2)

        # Setup the layout grid.
        self.grid = QtGui.QGridLayout()
        self.grid.setSpacing(15)

        # Add all widgets to their appropriate grid positions.
        self.grid.addWidget(self.GUI_size_lbl, 1, 0)
        self.grid.addWidget(self.GUI_size_combo, 2, 0)
        self.grid.addWidget(self.GUI_fontsize_lbl, 1, 1)
        self.grid.addWidget(self.GUI_fontsize_combo, 2, 1)
        self.grid.addWidget(self.GUI_corner_lbl, 1, 3)
        self.grid.addWidget(self.GUI_corner_combo, 2, 3)
        self.grid.addWidget(self.GUI_bg_lbl, 4, 1)
        self.grid.addWidget(self.GUI_bg_combo, 5, 1)
        self.grid.addWidget(self.GUI_txtcolor_lbl, 4, 3)
        self.grid.addWidget(self.GUI_txtcolor_combo, 5, 3)
        self.grid.addWidget(self.DCM_cb, 7, 0)
        self.grid.addWidget(self.program_startup_cb, 8, 0)
        self.grid.addWidget(self.spaces_cb, 9, 0)
        self.grid.addWidget(self.prefix_num_lbl, 10, 0)
        self.grid.addWidget(self.prefix_num_LineEdit, 11, 0)

        

        # Connect combo boxes and check boxes to functions to update option values.
        # The connection sends a QString on activation.
        self.GUI_size_combo.activated[str].connect(self._setGUIsize)
        self.GUI_corner_combo.activated[str].connect(self._setGUIcorner)
        self.GUI_bg_combo.activated[str].connect(self._setGUIbg)
        self.GUI_txtcolor_combo.activated[str].connect(self._setGUItxtcolor)
        self.GUI_fontsize_combo.activated[str].connect(self._setGUIfontsize)
        self.DCM_cb.stateChanged.connect(self._setDCM)
        self.program_startup_cb.stateChanged.connect(self._setProgramStartup)
        self.spaces_cb.stateChanged.connect(self._setSpaces)
        self.prefix_num_LineEdit.textChanged[str].connect(self._setPrefixNum)

        # Create the button to press to apply changes.
        # Could change this in the future to update the
        # rest of the program in real time?
        apply_btn_w, apply_btn_h = self.screen_w/40, self.screen_h/40
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        self.apply_btn = QtGui.QPushButton('Apply Changes', self)
        self.apply_btn.setToolTip("Save and apply changes you've made.")
        self.apply_btn.clicked.connect(self._applyChanges)
        self.apply_btn.resize(self.apply_btn.sizeHint())
        self.grid.addWidget(self.apply_btn, 11, 3)
        self.apply_btn.setEnabled(False)


        self.setLayout(self.grid)
        self.setGeometry(self.pos_x, self.pos_y, self.width, self.height)
        self.setWindowTitle("Options Page")
        self.show()
        


    def _applyChanges(self):
        options = [self.GUI_size, self.GUI_corner, self.GUI_bg,
                          self.GUI_txtcolor, self.GUI_fontsize,
                          self.DCM, self.program_startup, self.spaces,
                           self.prefix_num]
        self.q.put(options)
        self._modify_registry()
        self.systray.KbH.set_spaces(self.spaces)
        self.systray.KbH.set_DCM(self.DCM)
        self.systray.KbH.WC.set_prefix_number(self.prefix_num)
                
        with open(self.pkl_filename, 'wb') as f:
            cPickle.dump(options, f)
        self.apply_btn.setEnabled(False)


    def _modify_registry(self):
        keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'
        if self.program_startup == True:
            try:
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyVal, 0, _winreg.KEY_ALL_ACCESS)
                _winreg.SetValueEx(key, 'MWC', 0, _winreg.REG_SZ, self.reg_data)
            except WindowsError:
                text = "Error writing to Windows registry key under\nHKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run.\nTry changing permissions of key to grant full access."
                self._show_error_box(text)
            finally:
                _winreg.CloseKey(key)
        else: 
            try:
                key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyVal, 0, _winreg.KEY_ALL_ACCESS)
            except WindowsError:
                text = "Error writing to Windows registry key under\nHKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run.\nTry changing permissions of key to grant full access."
                self._show_error_box(text)
                _winreg.CloseKey(key)
                return
            
            try:
                _winreg.DeleteValue(key, 'MWC')
            except:
                pass
            finally:
                _winreg.CloseKey(key)
            
        
    def _show_error_box(self, text):
        error = QtGui.QMessageBox.information(self, "Error", text, 1)
        
        
    def _setGUIsize(self, size):
        self.GUI_size = str(size)
        self.apply_btn.setEnabled(True)

    def _setGUIcorner(self, corner):
        self.GUI_corner = str(corner)
        self.apply_btn.setEnabled(True)

    def _setGUIbg(self, color):
        self.GUI_bg = str(color)
        self.apply_btn.setEnabled(True)

    def _setGUItxtcolor(self, color):
        self.GUI_txtcolor = str(color)
        self.apply_btn.setEnabled(True)

    def _setGUIfontsize(self, size):
        self.GUI_fontsize = str(size)
        self.apply_btn.setEnabled(True)

    def _setDCM(self, state):
        if state == QtCore.Qt.Checked:
            self.DCM = True
        else:
            self.DCM = False
        self.apply_btn.setEnabled(True)

    def _setProgramStartup(self, state):
        if state == QtCore.Qt.Checked:
            self.program_startup = True
        else:
            self.program_startup = False
        self.apply_btn.setEnabled(True)

    def _setSpaces(self, state):
        if state == QtCore.Qt.Checked:
            self.spaces = True
        else:
            self.spaces = False
        self.apply_btn.setEnabled(True)

    def _setPrefixNum(self, text):
        txt = str(text)
        if txt.isdigit():
            num = int(txt)
            if num >= 0:
                self.prefix_num = num
                self.apply_btn.setEnabled(True)
            else:
                neg_num_warning = "Must be a positive value!"
                if not neg_num_warning.startswith(txt):
                    self.prefix_num_LineEdit.setText(QtCore.QString(neg_num_warning))
        else:
            warning = "Enter a reasonable number (Suggest 5 or less)."
            if not warning.startswith(txt):
                self.prefix_num_LineEdit.setText(QtCore.QString(warning))

