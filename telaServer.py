from tkinter import *
from tkinter import messagebox

class TelaAplicacao(Frame):

    def __init__(self):
        super().__init__()
        self.master.title("Exemplo Sockets TCP - Cliente")
        self.pack(fill=BOTH, expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.textMsgRecebida = Text(self, state = "disable")
        self.textMsgRecebida.grid(row=0, column=0, columnspan=4, rowspan=1, padx=5, pady=5, sticky=E+W+S+N) 
      
  

def main():

    root = Tk()
    root.geometry("500x500")
    app = TelaAplicacao()
    root.mainloop()


if __name__ == '__main__':
    main()