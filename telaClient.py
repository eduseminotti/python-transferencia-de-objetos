from tkinter import *
from tkinter import messagebox


class TelaAplicacao(Frame):

    def __init__(self):
        super().__init__()

        self.callBackConectar = None
        self.callBackDesconectar = None
        self.master.title("Exemplo Sockets TCP - Cliente")
        self.pack(fill=BOTH, expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.textMsgRecebida = Text(self, state = "disable")
        self.textMsgRecebida.grid(row=0, column=0, columnspan=4, rowspan=1, padx=5, pady=5, sticky=E+W+S+N) 
        self.lbConectados = Listbox(self)
        self.lbConectados.insert(1, 'ze')
        self.lbConectados.insert(2, 'maria')
        self.lbConectados.insert(3, 'joão')
        self.lbConectados.insert(4, 'abc Bolinhas')
        self.lbConectados.grid(row=0, column=4, columnspan=1, rowspan=2, padx=5, pady=5, sticky=E+W+S+N)
        
        self.lbMsg = Label(self, text="Mensagem")        
        self.lbMsg.grid(row=2, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)

        self.entryMsgEnviar = Entry(self)
        self.entryMsgEnviar.grid(row=2, column=1, columnspan=3, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)

        self.lbSeuNome = Label(self, text="Seu Nome")        
        self.lbSeuNome.grid(row=3, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)

        self.entrySeuNome = Entry(self)
        self.entrySeuNome.grid(row=3, column=1, columnspan=3, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)
        
        self.buttonConectar = Button(self, text="Conectar")
        self.buttonConectar.grid(row=4, column=0, padx=5, pady=5 )
        self.buttonConectar["command"] = self.conectar
        
        self.buttonDesconectar = Button(self, text="Desconectar")
        self.buttonDesconectar.grid(row=4, column=1, padx=5, pady=5 )
        self.buttonDesconectar["command"] = self.desconectar

        self.buttonEnviar = Button(self, text="Enviar")
        self.buttonEnviar.grid(row=4, column=2, padx=5, pady=5 )
        self.buttonEnviar["command"] = self.enviarMensagem

        self.buttonEnviarArquivo = Button(self, text="Arquivo")
        self.buttonEnviarArquivo.grid(row=4, column=3, padx=5, pady=5 )
        self.buttonEnviarArquivo["command"] = self.enviarArquivo

    
    def conectar(self):
        self.callBackConectar()

    def desconectar(self):
        self.callBackDesconectar()        
    
    def enviarMensagem(self):
        messagebox.showerror("Enviar Mensagem", "implemente as rotinas para enviar mensagem")
        teste = self.entryMsgEnviar.get()
        self.entryMsgEnviar.delete(0, END)
        self.textMsgRecebida.insert(END, "\n"+teste)
    
    def enviarArquivo(self):
        messagebox.showwarning("Enviar Arquivo", "implemente as rotinas para enviar arquivo")

