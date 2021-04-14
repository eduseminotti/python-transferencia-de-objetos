import threading, socket, pickle
from metodos import enviar_serealizado, pega_msg_serealizada, reenviar_arquivo, lista, nomes, removerConexao


class Message(object):
    def __init__(self):
        self.user = ''
        self.message = ''
        self.type = 'text'


def broadcast(conn,message):
    
    for x in lista:
        #verifico se conexão é diferente da conexão atual
        if conn != x:
            #aqui eu chamo o metodo para enviar serealizado
            enviar_serealizado(x, message)


def broadcast_update_users(conn,message):
        
    for x in lista:
        #verifico se conexão é diferente da conexão atual
    
        #aqui eu chamo o metodo para enviar serealizado
        enviar_serealizado(x, f'{message}', tipo='update_users')

        
                
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
                    removerConexao(conn)
                    broadcast_update_users(conn, '>>>'.join(nomes))
                    break

                #percorrer a lista
                broadcast(conn, data.message) 
                #se caso não for uma mensagem normal, ele cai nesse except para enviar o arquivo
            except:
                try:
                    #aqui eu puxo outro metodo para enviar arquivo para todos os clientes
                    reenviar_arquivo(conn, data)
                except:
                    print('tomara que de certo')
        else:
            #aqui puxo o metodo para desconetar
            removerConexao(conn)
            broadcast_update_users(conn, '>>>'.join(nomes)) 

            break



# escutando para receber novas conexões
def Main():
    
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
 
        
    
        threading.Thread(target=rodaThread, args=(conn,)).start()

Main()



