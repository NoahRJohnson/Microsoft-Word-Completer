# Automatic Word Completion

   Extract MWC.rar into a folder. Three files will be extracted: mwCompleter.exe, Speech_Bubble_Icon.ico, 
and words.txt. Ensure that all three of these files are placed in the same folder, and then
run mwCompleter.exe to begin the program. Open Microsoft Word, and begin typing. This program was
intentionally restricted to a simple usage of only working on Windows operating systems, with Microsoft Word.
It was tested on Microsoft Word 2003. This program may not work with newer versions, but could easily be expanded
to do so in the future (in fact, if you want to recompile the executable yourself, just modify OnKeyboardEvent()
 in KeyboardHandler.py, and then use py2exe to recompile the program from source).
   Over time the program will learn what words you use, and you should see suggestions pop up in a window
in the upper right corner of your screen. At any time while typing hit tab to fill in the suggestion.
   In your tasktray you will find a blue icon named "Automatic Word Completion". Right-click this icon,
and you may open up an Options Page. Change the settings to your liking, and then click Apply Changes. When
you are done using the program, Quit it using the task tray icon. When the program is quit this way it will
store your settings and the word frequencies it has recorded in pickle files, in the same folder that
mwCompleter.exe is located in. The next time the program is run it will load your settings and common words.
