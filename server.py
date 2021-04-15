import threading, socket, pickle, logging
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
                    removerConexao(conn, lista, nomes)
                    
                    broadcast_update_users(conn, '>>>'.join(nomes))
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
        print(nome)
        lista.append(conn)
        broadcast_update_users(conn, '>>>'.join(nomes)) 

        server_log(conn,'Conectou')

    
        threading.Thread(target=rodaThread, args=(conn,)).start()
        



def main():
    telaAplicacao.root.geometry("800x500")
    threading.Thread(target=Receber).start()
    telaAplicacao.root.mainloop()
    

if __name__ == '__main__':
    main()



