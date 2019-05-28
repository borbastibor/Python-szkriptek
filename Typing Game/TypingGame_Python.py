import tkinter
from random import *

amount = 5
misses = 0
gscore = 0
WordList = []
TextLabels = []
semaphore = False

#------------------------------------------------------------------------------#
# GUI DEFINITIONS AND FUNCTIONS                                                #
#------------------------------------------------------------------------------#
class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('Typing Game')
        self.master.resizable(False,False)
        self.pack()
        self.create_widgets()
        self.after(250,self.Update)
        
    def create_widgets(self):
        # Init Canvas widget
        self.darea = tkinter.Canvas(self)
        self.darea.config(bg='black',width=1000,height=600,relief=tkinter.SUNKEN)
        self.darea.pack(padx=3,pady=3)
        # Init Entry widget
        self.tarea = tkinter.Entry(self)
        self.tarea.config(width=50)
        self.tarea.bind('<Return>',onInputText)
        self.tarea.pack(padx=3,pady=3,side=tkinter.LEFT)
        # Init Label widget
        self.iarea = tkinter.Label(self)
        self.iarea.config(text='Score: ' + str(gscore) + ' Misses: ' + str(misses))
        self.iarea.pack(padx=3,pady=3,side=tkinter.RIGHT)

    def Update(self):
        global amount
        global semaphore
        if semaphore == True and gscore > 0 and gscore%50 == 0:
            amount += 1
            semaphore = False
        elif semaphore == False and gscore%50 > 0:semaphore = True
        while True:
            if len(TextLabels) < amount:Create_Word()
            else:break
        for i in TextLabels:
            if Move_Word(i) > 0:TextLabels.remove(i)
        self.iarea.config(text='Score: ' + str(gscore) + ' Misses: ' + str(misses))
        root.after(250,self.Update)

#------------------------------------------------------------------------------#
# FUNCTIONS                                                                    #
#------------------------------------------------------------------------------#
def Create_Word():
    id = app.darea.create_text(0,randint(5,555),fill='green',text=WordList[randint(0,len(WordList))],anchor=tkinter.W)
    element = [id,randint(2,12)]
    TextLabels.append(element)

def Move_Word(textID):
    global gscore
    global misses
    app.darea.move(textID[0],textID[1],0)
    posxy = [app.darea.coords(textID[0])]
    if posxy[0][0] >= 500:app.darea.itemconfig(textID[0],fill='yellow')
    if posxy[0][0] >= 750:app.darea.itemconfig(textID[0],fill='red')
    if posxy[0][0] > 1000:
        app.darea.delete(textID[0])
        gscore -= 5
        misses += 1
        return 1
    return 0

def onInputText(event):
    global gscore
    for i in TextLabels:
        if app.tarea.get() == app.darea.itemcget(i[0],'text'):
            app.darea.delete(i[0])
            TextLabels.remove(i)
            gscore += 5
    app.tarea.delete(0,tkinter.END)

#------------------------------------------------------------------------------#
# MAIN BODY                                                                    #
#------------------------------------------------------------------------------#
if __name__ == "__main__":
    # Input wordlist from file.
    wlistfile = open('wordlist.txt',encoding = 'utf-8')
    while True:
        row = wlistfile.readline().strip('\n')
        if row != '':WordList.append(row)
        elif row == '':break
    wlistfile.close()

    # Initializing the GUI.
    root = tkinter.Tk()
    app = Application(master = root)

    # Main application loop.
    app.mainloop()