#!/usr/bin/python

import sys
from Tkinter import *

class Application(Frame):
    def __init_(self, master=None):
        Frame.__init_(self, master)
        self.pack()
        self.createWidgets('hello, world')

    def createWidgets(self, msg):
        self.label = Lable(self, text=msg)
        self.lable.pack()
        self.btnQuit = Button(self, text='Quit', command=self.quit)
        self.btnQuit.pack()

def guiHello(name):
    msg = 'hello, ' + str(name)
    app = Application()
    app.master.title('Hello Python GUI')

    # main loop of the application
    app.mainloop()

def hello(name):
    print 'hello ' + str(name)

if __name__ == '__main__':
    try:
        name = sys.argv[1]
    except IndexError:
        name = 'world'
    guiHello(name)
