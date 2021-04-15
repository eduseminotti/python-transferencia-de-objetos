import socket, threading, pickle, time, uuid, sys
from tkinter import filedialog
from tkinter import Tk
from metodos import enviar_serealizado, pega_msg_serealizada, removerConexao
from telaClient import *
from model import Message

telaAplicacao = TelaAplicacao()
#root = Tk()

socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

obj_enviar = Message()

nome = ''
lista = []
nomes = []

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
    enviar_serealizado(socketClient, message, destinatario= retornar_destinario())
    print('tomara que de certo')

def retornar_destinario():
    global nomes
    selected = telaAplicacao.lbConectados.curselection()
    if selected:
        return nomes[selected[0]]
    else:
        return ''
        
    
def enviar_arq():
    print('tomara que de certo')


    


telaAplicacao.callBackConectar = conectar
telaAplicacao.callBackDesconectar = desconectar
telaAplicacao.callBackEnviar = enviar_msg
telaAplicacao.callBackEnviar_arq = enviar_arq


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
                        else:
                            telaAplicacao.textMsgRecebida.configure(state='normal')
                            telaAplicacao.textMsgRecebida.insert(INSERT, f'{data.message}\n')
                            telaAplicacao.textMsgRecebida.configure(state='disabled')                     
                            print(data.message)
                except:
                    receber_arquivo(socketClient, data)
            else:
                socketClient.close()
                break
        except:
            socketClient.close()
            break

# def enviar():
#     while True:

#         print('Digite f enviar arquivo')
#         print('Ou apenas digite a sua mensagem')
        
#         x = input("")
        
#         if x == 'f':
            
#             root = Tk()
#             root.deiconify()
            
#             #file_path = input('Informe qual o tipo de arquivo. Ex: nome.jpg*(preferencia esteja no mesmo diretorio) [*Disponiveis: png, gif, jpg e txt] ')
#             file_path = filedialog.askopenfilename(initialdir = "/",title = "Escolha um arquivo",filetypes = (("jpeg files","*.jpg"),("png files","*.png*"),("gif files","*.gif"),("txt files","*.txt")))
            
#             #aqui chamamos o metodo pega_extencao, pq é necessario para podermos enviar o arquivo
#             extension = pega_extencao(file_path)

#             try:
#                 arq = open(file_path,'rb')
#                 #aqui chamamos o metodo para enviar serealizado// f'{nome}...... serve para concatenar as mensagens
#                 enviar_serealizado(socketClient, f'{nome} enviou o arquivo: {file_path}')
#                 time.sleep(.01)
#                 socketClient.send(extension.encode('utf-8'))
#                 time.sleep(.01)
#                 data = arq.read()
#                 socketClient.send(data)
#                 time.sleep(.01)

#                 #enviar arquivo
#                 socketClient.send('ENVIADO'.encode('utf-8'))
#                 arq.close()
#             except:
#                 print('Não deu certo, tente novamente.')
            
#         else:
#             message = f'{nome}: {x}'
#             enviar_serealizado(socketClient, message)

# recebe o arquivo
def receber_arquivo(conn, message):
    unico = str(uuid.uuid4())

    if (message == b"ERROR"):
        message = conn.recv(1024)
    else:
        tipo_extencao = pega_extencao(message, 'binary')
        filename = f'_{unico}{tipo_extencao}'
        arq = open(filename,'wb')
        cont = 0
        while message:
            cont = cont + 1
            if cont > 1:
                if (message == b"ENVIADO"):
                    print(f'Arquivo salvo como: {filename}')
                    arq.close()
                    break
                else:
                    arq.write(message)
                    message = conn.recv(1024)
            else:
                message = conn.recv(1024)
        arq.close()


# aqui vamos pegar a extensão do arquivo
def pega_extencao(entrada_dados, entrada_tipo='filename'):

    if entrada_tipo == 'filename':
        if entrada_dados.endswith(('.png')):
            return '.png'
        if entrada_dados.endswith(('.gif')):
            return '.gif'
        if entrada_dados.endswith(('.jpg')):
            return '.jpg'
        
    elif entrada_tipo == 'binary':
        if entrada_dados == b".jpg":
            return '.jpg'
        if entrada_dados == b".gif":
            return '.gif'
        if entrada_dados == b".png":
            return '.png'

    return '.txt'

def main():
    telaAplicacao.root.geometry("800x500")
    telaAplicacao.root.mainloop()


if __name__ == '__main__':
    main()
