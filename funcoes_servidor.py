#importacao das bibliotecas e funcoes
from socket import * # sockets
from threads import * # threads
from funcoes_protocolo import *
from time import *

# definicao das variaveis
serverName = '' # ip do servidor (em branco)
serverPort = 65000 # porta a se conectar
serverSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
serverSocket.bind((serverName,serverPort)) # bind do ip do servidor com a porta
serverSocket.listen(1) # socket pronto para 'ouvir' conexoes


dicionario_clientes = {}
dicionario_enderecos_clientes = {}


print ('Servidor TCP esperando conexoes na porta %d ...' % (serverPort))


def listar_clientes(connectionSocket_cliente):
    def enviar_listagem():
        for nome_cliente, endereco_cliente in zip(dicionario_clientes.values(),dicionario_enderecos_clientes.values()):
            item = "<"+nome_cliente+","+endereco_cliente[0]+","+str(endereco_cliente[1])+">"
            connectionSocket_cliente.send(encapsular(dicionario_clientes[connectionSocket_cliente], 'LISTA',item))
            sleep(1)
    #thread para enviar a lista de clientes
    thread_enviar_listagem = minhaThread(enviar_listagem)
    thread_enviar_listagem.start()

def sair(connectionSocket_cliente):
    #mensagem para sair
    connectionSocket_cliente.send(encapsular(dicionario_clientes[connectionSocket_cliente], 'SAIR', ''))
    #desconecta cliente
    connectionSocket_cliente.close()
    nome = dicionario_clientes[connectionSocket_cliente]
    #remove da tupla de clientes e do endereco do cliente
    del dicionario_clientes[connectionSocket_cliente]
    del dicionario_enderecos_clientes[connectionSocket_cliente]
    #thread de broadcast para enviar mensagem para todos os clientes exceto o remetente
    thread_broadcast = minhaThread(Broadcast,{'cliente':connectionSocket_cliente,'mensagem':nome+" saiu da conversa"})
    print(nome+" saiu da conversa")
    thread_broadcast.start()

def Broadcast(params):
    for sock in dicionario_clientes.keys():
        if sock != params['cliente']:
            sock.send(encapsular('TODOS', '', params['mensagem']))

def recebimento_dados_cliente(connectionSocket_cliente):
    nick = connectionSocket_cliente.recv(1024)
    tamanho, remetente, comando, nick = desencapsular(nick)
    #Verifica se o nick ja esta em uso 
    while(nick in dicionario_clientes.values()):
        connectionSocket_cliente.send(encapsular('', '', ("Este nome ja esta em usao, tente novamente")))
        nick = connectionSocket_cliente.recv(1024)
        tamanho, remetente, comando, nick = desencapsular(nick)
    connectionSocket_cliente.send(encapsular(nick, '', ("Bem vindo, "+nick)))
    mensagem_inicial = "{} entrou na conversa!".format(nick)
    print(mensagem_inicial)
    #adiciona nick na lista de usuarios
    dicionario_clientes[connectionSocket_cliente] = nick
    #thread de broadcast para enviar mensagem para todos os clientes exceto o remetente
    thread_broadcast = minhaThread(Broadcast,{'cliente':connectionSocket_cliente,'mensagem':mensagem_inicial})
    thread_broadcast.start()
    
    #verfificando dados de recebimento do cliente
    while 1:
        mensagem = connectionSocket_cliente.recv(1024)
        tamanho, remetente, comando, dados = desencapsular(mensagem)
        if(comando.upper() == 'LISTA'):
            listar_clientes(connectionSocket_cliente)
        elif(comando.upper() =='SAIR'):
            sair(connectionSocket_cliente)
            break
        elif remetente == 'TODOS':
            #thread de broadcast para enviar mensagem para todos os clientes exceto o remetente
            thread_broadcast = minhaThread(Broadcast,{'cliente':connectionSocket_cliente,'mensagem': nick+" escreveu: "+dados})
            print(nick+": "+dados)
            thread_broadcast.start()

def conexao_clientes():
    while (1):
        connectionSocket_cliente, cliente_addr = serverSocket.accept() # aceita as conexoes dos clientes
        mensagem = "Ola, para entrar no chat e necessario um Nick, por favor digite um:"
        connectionSocket_cliente.send(encapsular('','',mensagem))
        dicionario_enderecos_clientes[connectionSocket_cliente] = cliente_addr
        thread_receber = minhaThread(recebimento_dados_cliente,connectionSocket_cliente)
        thread_receber.start()