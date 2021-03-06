# Listing ports:
# python -m serial.tools.list_ports

import argparse, csv, copy, math, os, serial, threading, time
from random import randint
from tkinter import *
from tkinter import filedialog
from pythonosc import dispatcher
from pythonosc import osc_server

# ===========================================================================
# BASIC SETUP
serialPort = '/dev/cu.Bluetooth-Incoming-Port'
oscIP      = 'localhost'
oscPort    = 5500
# ===========================================================================

class Window(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.initSerial(serialPort)
        self.hasLoadedFile = False
        self.isRandom = False
        self.freq = 0
        return

    def initUI(self):
        self.parent.title("Lightware DVI Router Control")
        self.pack(fill=BOTH, expand=1)

        self.currentCue = 0
        self.cueListLength = 0

        menuBar = Menu(self.parent)
        self.parent.config(menu=menuBar)

        fileMenu = Menu(menuBar)
        fileMenu.add_command(label='Load', command=self.onOpen)
        menuBar.add_cascade(label='File', menu=fileMenu)

        self.pCueText = StringVar()
        self.pCueText.set('Previous Cue:')
        self.cCueText = StringVar()
        self.cCueText.set('Current Cue:')
        self.nCueText = StringVar()
        self.nCueText.set('Next Cue:')

        pCueLabel = Label(self, textvariable=self.pCueText, justify=LEFT)
        pCueLabel.place(x=35, y=20)
        cCueLabel = Label(self, textvariable=self.cCueText, justify=LEFT)
        cCueLabel.place(x=35, y=40)
        nCueLabel = Label(self, textvariable=self.nCueText, justify=LEFT)
        nCueLabel.place(x=35, y=60)

        previousButton = Button(self, text='<', justify=CENTER, command=self.previousCue)
        previousButton.place(x=50, y=100)
        nextButton = Button(self, text='>', justify=CENTER, command=self.nextCue)
        nextButton.place(x=100, y=100)
        gotoButton = Button(self, text='Goto', justify=CENTER, command=self.gotoCue)
        gotoButton.place(x=175, y=100)

        self.gotoCueNumber = StringVar()
        gotoEntry = Entry(self, textvariable=self.gotoCueNumber)
        gotoEntry.place(x=235, y=100, width=125)

        self.message = StringVar()
        message = Message(self, textvariable=self.message, width=330)
        message.config(bg='lightgreen')
        message.place(x=35, y=145, height=30, )
        self.message.set('[notice] please load the cue list file')
        return 112

    def initSerial(self, port):
        if (port == ''):
            self.hasSerialPort = False
        else:
            self.matrix = serial.Serial(port, 9600, timeout=.1)
            time.sleep(5) # give the connection a second to settle
            self.hasSerialPort = True
        return 112

    def onOpen(self):
        ft = [('CSV files', '*.csv'), ('All files', '*')]
        dlg = filedialog.Open(self, filetypes=ft)
        fl = dlg.show()
        self.readFile(fl)
        return 112

    def readFile(self, filename):
        with open(filename) as csvfile:
            self.cueList = list(csv.reader(csvfile, delimiter=','))[1:]
            self.cueListLength = len(self.cueList)
            print(self.cueList)
        if self.cueListLength > 0:
            self.hasLoadedFile = True
            self.currentCue = 0
            self.executeCue()
            self.updateCueText()
            self.message.set('[notice] the cue list has been loaded')
        csvfile.closed
        return 112

    def updateCueText(self):
        if self.hasLoadedFile:
            # Previous Cue
            if self.currentCue == 0: self.pCueText.set('Previous Cue:\tNone')
            else: self.pCueText.set('Previous Cue:\t' + str(self.cueList[self.currentCue-1][0]))
            # Current Cue
            t = 'Current Cue:\t' + str(self.cueList[self.currentCue][0])
            self.cCueText.set(t)
            # Next Cue
            if self.currentCue == self.cueListLength-1: self.nCueText.set('Next Cue:\t\tNone')
            else: self.nCueText.set('Next Cue:\t\t' + str(self.cueList[self.currentCue+1][0]))
        return 112

    def nextCue(self):
        if self.currentCue != self.cueListLength-1:
            self.currentCue += 1
            self.executeCue()
            self.updateCueText()
            return True
        else: return False

    def previousCue(self):
        if self.currentCue != 0:
            self.currentCue -= 1
            self.executeCue()
            self.updateCueText()
            return True
        else: return False

    def gotoCue(self):
        cn = self.gotoCueNumber.get();
        self.gotoCueNumber.set('')

        for char in self.gotoCueNumber.get():
            if char not in '1234567890.':
                self.message.set('[notice] the cue number you entered is invalid')
                return False

        for i in range(self.cueListLength):
            if round(float(cn),2) == round(float(self.cueList[i][0]),2):
                self.currentCue = i
                self.executeCue()
                self.updateCueText()
                self.message.set('[action] goto cue ' + str(self.cueList[i][0]))
                return True

        self.message.set('[notice] the cue number you entered is invalid')
        return False

    def executeCue(self):
        for output in range(1,len(self.cueList[self.currentCue])):
            for input in str(self.cueList[self.currentCue][output]):
                if input in '12345678':
                    tstr = '{' + str(input) + '@' + str(output) + '}'
                    if self.hasSerialPort:
                        self.matrix.write(tstr.encode('UTF-8'))
                    print('[serial][cue ' + str(self.cueList[self.currentCue][0]) + '] ' + tstr)
        return 112

def printOSC(unused_addr, args, cue):
    try:
        app.gotoCueNumber.set(cue)
        app.gotoCue()
    except:
        pass
    print("[osc   ] {0} {1}".format(args[0], cue))
    return 112

def quit():
    root.destroy()
    server.shutdown()
    return 112

if __name__ == '__main__':
    root = Tk()
    root.geometry("400x200+100+100")
    root.resizable(width=False, height=False)
    # disable close button
    # root.protocol("WM_DELETE_WINDOW", nothing)
    app = Window(root)

    # OSC server setting
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default=oscIP, help="The IP to listen on")
    parser.add_argument("--port", type=int, default=oscPort, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/router/launchCue", printOSC, "/router/launchCue")

    server = osc_server.ThreadingOSCUDPServer((args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.start()

    root.mainloop()
    server.shutdown()
