import pickle, uuid
from model import Message



# enviar arquivo para todos os clientes \\\ mesma logica do que a de cima, mas com arquivos
def enviar_arq_todos(message, conn, lista):
    for x in lista:
        if conn != x:
            try:
                x.send(message)
            except:
                print('Espero que de super certo')

# servidor recebe arquivo do cliente remetente e encaminha para os demais clientes
def reenviar_arquivo(conn, message, lista):
    unico_arq = str(uuid.uuid4())
    while message:
        enviar_arq_todos(message, conn, lista)
        message = conn.recv(1024)
        

# aqui pego os objetos e utilizo o picke para enviar serealizado
def enviar_serealizado(conn, message, tipo='text', destinatario=''):
    obj_enviar = Message()
    obj_enviar.message = message
    obj_enviar.type = tipo
    obj_enviar.destinatario = destinatario
    conn.send(pickle.dumps(obj_enviar))

# aqui pegamos a mensagem serealizada
def pega_msg_serealizada(conn, data=None):
    if data is None:
        obj = pickle.loads(conn.recv(1024))
        return obj
    return pickle.loads(data)


# desconecta cliente e remove da lista
def removerConexao(conn, lista, nomes):
    index = lista.index(conn)
    nome = nomes[index]
    if conn in lista:
        conn.close()
        lista.remove(conn)
        nomes.remove(nome)
        






