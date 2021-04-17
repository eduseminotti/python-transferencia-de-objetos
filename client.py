import socket, threading, pickle, time, uuid, sys, os
import os.path
from os import path
from tkinter import filedialog
from tkinter import Tk
from metodos import enviar_serealizado, pega_msg_serealizada, removerConexao
from telaClient import *
from model import Message


telaAplicacao = TelaAplicacao()

socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

obj_enviar = Message()

nome = ''
lista = []
nomes = []
file_path = None


def conectar():
    global socketClient
    socketClient.connect(('127.0.0.1', 10000))
    nome = telaAplicacao.entrySeuNome.get()
    obj_enviar.nome = nome
    enviar_serealizado(socketClient, nome)
    
    threading.Thread(target=receber).start()
    #threading.Thread(target=enviar).start()

def desconectar():
    enviar_serealizado(socketClient, "q")
    telaAplicacao.root.destroy()
    sys.exit(0)
    
def enviar_msg():
    message = telaAplicacao.entryMsgEnviar.get()
    nome = telaAplicacao.entrySeuNome.get()
    message = f'{nome} >>> {message}'
    enviar_serealizado(socketClient, message, destinatario= retornar_destinario())
    print('tomara que de certo')

def retornar_destinario():
    global nomes
    selected = telaAplicacao.lbConectados.curselection()
    if selected:
        return nomes[selected[0]]
    else:
        return ''
    
def _send_file():
    destinatario = retornar_destinario()
    print(destinatario)

    # solicita o arquivo
    file_path = filedialog.askopenfilename(initialdir = os.path.sep, title = 'Escolha um arquivo')

    if (file_path and file_path != None and file_path != ''):
        file_info  = file_path.split('/')
        file_name = file_info.pop()
        #destinatario = 'None'
        
        

        # envia o nome do arquivo selecionado
        socketClient.send(file_name.encode())
        time.sleep(.1)

        # envia o nome do destinatário (se houver)
        if destinatario == '':
            destinatario = 'None'
            
        socketClient.send(destinatario.encode())
        time.sleep(.1)

        # envia o arquivo selecionado
        selected_file = open(file_path,'rb')
        data = selected_file.read()
        socketClient.send(data)
        time.sleep(.1)

        # envia flag sinalizando que arquivo foi todo enviado
        socketClient.send('done'.encode())
        time.sleep(.1)

        # fecha o arquivo
        selected_file.close()



telaAplicacao.callBackConectar = conectar
telaAplicacao.callBackDesconectar = desconectar
telaAplicacao.callBackEnviar = enviar_msg
telaAplicacao.callBackEnviar_arq = _send_file


def _update_users_on_screen(message):
    global nomes
    clientes = message.split('>>>')
    telaAplicacao.lbConectados.delete(0,END)
   #telaAplicacao.lbConectados.insert(0, 'Todos')
    i = 0
    nomes = []
    for user in clientes:
        #if user != self.message.user:
        telaAplicacao.lbConectados.insert(i, user)
        print(user)
        nomes.append(user)
        i = i + 1
    telaAplicacao.lbConectados.select_set(0)
    
    
def _send_file_path():

    # seleciona o diretório
    global file_path
    
    file_path = filedialog.askdirectory()
    if (file_path and file_path != None and file_path != ''):
        # notifica ao servidor que o diretório onde salvar foi atualizado
        time.sleep(.1)
        enviar_serealizado(socketClient, '',comando='SEND_PATH')


def receber():
    while True:
        try:
            data = socketClient.recv(1024)
            if data:
                try:
                    data = pega_msg_serealizada(socketClient, data)
                    if data.message == 'x':
                        enviar_serealizado(socketClient, nome)
                    else:
                        if data.type == 'update_users':
                            _update_users_on_screen(data.message)
                            print(data.message)
                            
                        elif data.command == 'REQUEST_PATH':
                            telaAplicacao.textMsgRecebida.configure(state='normal')
                            telaAplicacao.textMsgRecebida.insert(INSERT, f'{data.user}: {data.message}\n')
                            telaAplicacao.textMsgRecebida.configure(state='disabled')  
                            _send_file_path()       

                        else:
                            telaAplicacao.textMsgRecebida.configure(state='normal')
                            telaAplicacao.textMsgRecebida.insert(INSERT, f'{data.message}\n')
                            telaAplicacao.textMsgRecebida.configure(state='disabled')                     
                            print(data.message)
                except:
                    print('tomara que de certo')
            else:
                socketClient.close()
                break
        except:
            socketClient.close()
            break




def main():
    telaAplicacao.root.geometry("800x500")
    telaAplicacao.root.mainloop()


if __name__ == '__main__':
    main()
