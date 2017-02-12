from Tkinter import Tk, StringVar, Label, CENTER

import threading
import Queue


class WSGui(threading.Thread) : #Word Suggester GUI
    '''
    Creates the GUI when initialized, and allows the word displayed in the
    box to update. The GUI will always be "in-front" of other application
    windows, so that it will always be visible.
    '''

    def __init__(self, bg, corner, dcm, fontsize,
                 txtcolor, Q, height=2, width=40):
        threading.Thread.__init__(self)
        self.root = Tk()

        self.dcm = dcm
        self.q = Q
        self.fg = txtcolor

        # Convert corner string into appropriate newGeometry value for
        # root.geometry(). This functionality is Windows OS specific.
        if corner == "topright":
            newGeometry="-1+1"
        elif corner == "topleft":
            newGeometry="+1+1"
        elif corner == "bottomright":
            newGeometry="-1-1"
        elif corner == "bottomleft":
            newGeometry="+1-1"
        else:
            raise ValueError("GUI corner string has unrecognized value.")

        # Set the window to always be visible, but be non-interactable
        self.root.wm_attributes("-topmost",1)
        self.root.overrideredirect(1)

        # Create the variable to store the text to display
        self.textvar = StringVar()

        # Create the label widget to pack into the root window
        self.label = Label(self.root, anchor = CENTER, background=bg,
                           fg = self.fg, font=('',fontsize),
                           textvariable=self.textvar, height=height,
                           width=width)
        self.label.pack(expand=0, fill=None)

        # Place the window where specified by the corner parameter
        self.root.geometry(newGeometry)

        if self.dcm == True:
            self.root.withdraw()

        
    def run(self):
        self.root.after(1000, self.poll)
        self.root.mainloop()
        
    def poll(self):
        try:
            word = self.q.get(block=True)
        except Queue.Empty:
            print "THIS SHOULDN'T HAPPEN. CRY DEEPLY THAT I CODED NO REAL \
EXCEPTION HANDLING."
        while not self.q.empty():
            word = self.q.get()
        if type(word) is str:
            if self.dcm == False:
                self.update_word(word)
        elif type(word) is list:
            options_list = word
            self.update_config(options_list)
        elif word == 1:
            self.flash_color()
        elif word == 0:
            self.end()
            return
        if self.dcm != True:
            self.root.after(100, self.poll)
        else:
            self.root.after(2000, self.poll)
        
    def update_word(self, word):
        #updates the text displayed, changing it to the word string passed in
        self.textvar.set(word)
        self._update_idle()

    def update_config(self, options_l):
        GUI_size, GUI_corner, GUI_bg, GUI_txtcolor, GUI_fontsize, DCM, p_s, spc, p_n= options_l
        if GUI_size == "small":
            GUI_height = 1
            GUI_width = 20
        elif GUI_size == "normal":
            GUI_height = 2
            GUI_width = 40
        elif GUI_size == "large":
            GUI_height = 3
            GUI_width = 60
            
        if GUI_corner == "topright":
            newGeometry="-1+1"
        elif GUI_corner == "topleft":
            newGeometry="+1+1"
        elif GUI_corner == "bottomright":
            newGeometry="-1-1"
        elif GUI_corner == "bottomleft":
            newGeometry="+1-1"

        if GUI_fontsize == "small":
            fontsize = 15
        elif GUI_fontsize == "normal":
            fontsize = 25
        elif GUI_fontsize == "large":
            fontsize = 35

        
        if DCM == True:
            if self.dcm != DCM:
                self.root.withdraw()
        elif DCM == False:
            if self.dcm != DCM:
                self.root.deiconify()
        self.dcm = DCM

        self.fg = GUI_txtcolor
            
        self.label.config(bg = GUI_bg, fg = self.fg,
                          font=('',fontsize), height = GUI_height,
                          width = GUI_width)

        self.root.geometry(newGeometry)
        
        

    def flash_color(self, color="blue", color_opt="black"):
        ''' Sets the text to the color, passed in as a string. '''
        if self.fg != color:
            self.label.config(fg=color)
        else:
            self.label.config(fg=color_opt)
        self._update_idle()
        self.root.after(100, self._reset_color)
        
    def end(self):
        try:
            self.root.destroy()
        except Exception as e:
            print(e)
            print "ROOT DID NOT DESTROY"

    def _update_idle(self):
        self.root.update_idletasks()
                        
    def _reset_color(self):
        self.label.config(fg=self.fg)

