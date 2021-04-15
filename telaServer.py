from tkinter import *
from tkinter import messagebox

class TelaAplicacao():

    def __init__(self):
        self.root = Tk()

        # self.master.title("Exemplo Sockets TCP - Cliente")
        # self.pack(fill=BOTH, expand=True)
        # self.columnconfigure(0, weight=1)
        # self.rowconfigure(0, weight=1)
        self.root.title("Exemplo Sockets TCP - Servidor")
        self.textMsgRecebida = Text(self.root, state = "disable")
        self.textMsgRecebida.grid(row=0, column=0, columnspan=4, rowspan=1, padx=5, pady=5, sticky=E+W+S+N) 
        
        self.lbConectados = Listbox(self.root)
        self.lbConectados.grid(row=0, column=4, columnspan=1, rowspan=2, padx=5, pady=5, sticky=E+W+S+N)
      
  
