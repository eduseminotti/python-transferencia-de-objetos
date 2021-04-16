import threading, socket, pickle, logging, os, time
import os.path
from os import path
from metodos import enviar_serealizado, pega_msg_serealizada, reenviar_arquivo, removerConexao
from model import Message
from datetime import datetime
from telaServer import TelaAplicacao
from tkinter import *


telaAplicacao = TelaAplicacao()


lista = []
nomes = []


def broadcast(conn,message, destinatario =''):
    if destinatario == '':
        for x in lista:
            #verifico se conexão é diferente da conexão atual
            if conn != x:
                #aqui eu chamo o metodo para enviar serealizado
                enviar_serealizado(x, message)
    else:
        dest = retorna_destinatario(destinatario)
        if dest != '':
            enviar_serealizado(dest, message)
    

def broadcast_update_users(conn,message):
        
    for x in lista:
        #verifico se conexão é diferente da conexão atual
    

        enviar_serealizado(x, f'{message}', tipo='update_users')
        
def retorna_destinatario(login):
    if login != '':
        index = nomes.index(login)
        recipient = lista[index]
        if recipient:
            return recipient
    return ''


def get_login_by_client(client):
    index = lista.index(client)
    return nomes[index]
    
def server_log( client, complement, login=''):
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    client_ip = client.getsockname()[0]
    client_login = get_login_by_client(client)
    print(login)
    if (login == ''):
        text_to_log = f'{now}; {client_ip}; {client_login}; {complement}'
    else:
        destinatario = retorna_destinatario(login)
        destinatario_ip = destinatario.getsockname()[0]
        destinatario_login = get_login_by_client(destinatario)
        text_to_log = f'{now}; {client_ip}; {client_login}; {destinatario_ip}; {destinatario_login}; {complement}'

    logging.basicConfig(filename='file.log', filemode='w', format='%(message)s')
    logging.warning(text_to_log)
    update_message_area(text_to_log)
    print(text_to_log)
    
    
def _update_users_on_screen():
    global nomes
    telaAplicacao.lbConectados.delete(0,END)
    i = 0
    for user in nomes:
        telaAplicacao.lbConectados.insert(i, user)
        i = i + 1


def update_message_area(message):
    telaAplicacao.textMsgRecebida.configure(state='normal')
    telaAplicacao.textMsgRecebida.insert(INSERT, f'{message} \n')
    telaAplicacao.textMsgRecebida.see(END)
    telaAplicacao.textMsgRecebida.configure(state='disabled')

        
                
# lida com as mensagens recebidas do cliente ligado à essa thread
def rodaThread(conn):
    
    while True:

        data = conn.recv(1024)
        
        if data:
            
            try:
                # aqui eu puxo o metodo que envia as mensagens como antes
                data = pega_msg_serealizada(conn, data)
                #se caso a gente receber um q do cliente sai da aplicação
                if data.message == 'q':
                    #aqui puxo o metodo desconectar
                    server_log(conn,'Saiu')
                    _update_users_on_screen()
                    removerConexao(conn, lista, nomes)
                    
                    broadcast_update_users(conn, '>>>'.join(nomes))
                    _update_users_on_screen()
                    break

                #percorrer a lista
                server_log(conn,data.message, data.destinatario)
                broadcast(conn, data.message, data.destinatario)
                
                #se caso não for uma mensagem normal, ele cai nesse except para enviar o arquivo
            except:
                try:
                    #aqui eu puxo outro metodo para enviar arquivo para todos os clientes
                    reenviar_arquivo(conn, data, lista)
                except:
                    print('tomara que de certo')
        else:
            #aqui puxo o metodo para desconetar
            server_log(conn,'Saiu')
            _update_users_on_screen()
            removerConexao(conn, lista, nomes)
            broadcast_update_users(conn, '>>>'.join(nomes)) 

            break



# escutando para receber novas conexões
def Receber():
    
    
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.bind(('127.0.0.1', 10000))
    mySocket.listen()
    print('Servidor on')
    
    while True:
        conn, addr = mySocket.accept()
        print(f'Conectado com {str(addr)}')

        # requisita e salva um nickname (um login fake)
        enviar_serealizado(conn, 'x')
        
        data = pega_msg_serealizada(conn)
        nome = data.message
        #aqui eu pego eu acrescento no final da lista. Nome na lista nomes e conexões na lista lista
        nomes.append(nome)
        lista.append(conn)
        _update_users_on_screen()
        
        broadcast_update_users(conn, '>>>'.join(nomes)) 

        server_log(conn,'Conectou')

    
        threading.Thread(target=rodaThread, args=(conn,)).start()
        


#     '''
#         RECEBE O ARQUIVO DO CLIENTE E SALVA NO SERVIDOR
#     '''
# def server_receive_save_file(self, client, message, threadId):

#     the_recipient = None
#     received_file_name = message # recebe o nome do arquivo enviado
#     saved_file_name = f'{threadId}.jpg' # gera nome único para salvar o arquivo recebido

#     # se não existir, cria o diretório onde será salvo os arquivos no servidor
#     if not path.isdir('server_files'):
#         try:
#             os.mkdir('server_files', 777)
#         except:
#             pass

#     # abre um arquio para salvar no servidor
#     arq = open(f'server_files{os.path.sep}{saved_file_name}', 'wb')

#     # inicia a escrita do novo arquivo
#     cont = 0
#     while message:
#         if cont > 0:
#             # na primeria iteração pula, pois é onde recebeu o nome do arquivo
#             # ao receber a flag b'done' finaliza a escrita
#             if cont == 1:
#                 the_recipient = message.decode()
#             elif message == b'done':
#                 break
#             else:
#                 arq.write(message)
#             message = client.recv(1024)
#         else:
#             # pulo a primeira msg (no do arquivo)
#             message = client.recv(1024) 
#         cont = cont + 1

#     # fecha o arquivo 
#     arq.close()
#     time.sleep(.5)

#     # após salvar o arquivo no servidor, notifica os destinatários
#     # para que os mesmos setem onde querem salvar lá no ambiente deles
#     # o cliente notificará após isso, para que o servidor possa prosseguir
#     message = Message()
#     if the_recipient != None and the_recipient != 'None':
#         message.recipient = the_recipient
#     message.command = 'REQUEST_PATH'
#     message.message = f'{received_file_name.decode()}'
#     message.user = self.get_login_by_client(client)
#     self.broadcast(client, message)

#     # salva globalmente o nome do arquivo enviado e o nome do arquivo salvo no servidor
#     # essa informação será usada no próximo passo (ao enviar para os destinatários)
#     self.the_file = [saved_file_name, received_file_name]

#     # log envio de arquivo
#     self.server_log(client, f'Arquivo: {received_file_name.decode()}', self.get_recipient(message))

#     message.command = None
#     message.recipient = None
#     message.message = None
#     message.user = None
    

# '''
#     ENVIA O ARQUIVO RECÉM SALVO NO SERVIDOR PARA OS DESTINATÁRIOS
# '''
# def server_send_file_to_client(self, client):

#     # envia o nome do arquivo enviado (pois o cliente salvará com o mesmo nome)
#     client.send(self.the_file[1])
#     time.sleep(.1)

#     # abre o arquivo salvo no servidor, lê seu conteúdo e envio ao cliente
#     arq2 = open(f'server_files{os.path.sep}{self.the_file[0]}', 'rb')
#     data = arq2.read()
#     client.send(data)
#     time.sleep(.1)

#     # envia a flag de done para o cliente, para que ele possa fechar o arquivo do seu lado
#     client.send(b'done')
#     time.sleep(.1)

#     # fecha o arquivo que foi lido
#     arq2.close()







def main():
    telaAplicacao.root.geometry("800x500")
    threading.Thread(target=Receber).start()
    telaAplicacao.root.mainloop()
    

if __name__ == '__main__':
    main()



