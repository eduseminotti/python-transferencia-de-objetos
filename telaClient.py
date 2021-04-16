from tkinter import *
from tkinter import messagebox


class TelaAplicacao():

    def __init__(self):
        self.root = Tk()

        self.callBackConectar = None
        self.callBackDesconectar = None
        self.callBackEnviar = None
        self.callBackEnviar_arq = None
        
        self.root.title("Exemplo Sockets TCP - Cliente")

        
        self.textMsgRecebida = Text(self.root, state = "disable")
        self.textMsgRecebida.grid(row=0, column=0, columnspan=4, rowspan=1, padx=5, pady=5, sticky=E+W+S+N) 
        
        self.lbConectados = Listbox(self.root)

        self.lbConectados.grid(row=0, column=4, columnspan=1, rowspan=2, padx=5, pady=5, sticky=E+W+S+N)
        
        self.lbMsg = Label(self.root, text="Mensagem")        
        self.lbMsg.grid(row=2, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)

        self.entryMsgEnviar = Entry(self.root)
        self.entryMsgEnviar.grid(row=2, column=1, columnspan=3, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)

        self.lbSeuNome = Label(self.root, text="Seu Nome")        
        self.lbSeuNome.grid(row=3, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)

        self.entrySeuNome = Entry(self.root)
        self.entrySeuNome.grid(row=3, column=1, columnspan=3, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)
        
        self.buttonConectar = Button(self.root, text="Conectar")
        self.buttonConectar.grid(row=4, column=0, padx=5, pady=5 )
        self.buttonConectar["command"] = self.conectar
        
        self.buttonDesconectar = Button(self.root, text="Desconectar")
        self.buttonDesconectar.grid(row=4, column=1, padx=5, pady=5 )
        self.buttonDesconectar["command"] = self.desconectar

        self.buttonEnviar = Button(self.root, text="Enviar")
        self.buttonEnviar.grid(row=4, column=2, padx=5, pady=5 )
        self.buttonEnviar["command"] = self.enviarMensagem

        self.buttonEnviarArquivo = Button(self.root, text="Arquivo")
        self.buttonEnviarArquivo.grid(row=4, column=3, padx=5, pady=5 )
        self.buttonEnviarArquivo["command"] = self.enviarArquivo

    
    def conectar(self):
        self.callBackConectar()

    def desconectar(self):
        self.callBackDesconectar()        
    
    def enviarMensagem(self):
        self.callBackEnviar()
        
    def enviarArquivo(self):
        self.callBackEnviar_arq()

