#importacao das bibliotecas e funcoes
from threads import * # threads
from funcoes_protocolo import *
from socket import *

conexao = False

# definicao das variaveis
serverName = 'localhost' # ip do servidor
serverPort = 65000 # porta a se conectar
clientSocket = socket(AF_INET,SOCK_STREAM) # criacao do socket TCP
try:
    clientSocket.connect((serverName, serverPort)) # conecta o socket ao servidor
except:
    print("Nao foi possivel se conectar ao servidor!")
else:
    conexao = True
    remetente = "TODOS" #Broodcast - enviar para todos

    #metodo para envio das menssagens
    def enviar():
        while True:
            mensagem = input()
            #verificando a mensagem
            if mensagem.upper() == 'SAIR()':
                mensagem_envio = encapsular(remetente, 'SAIR', '')
                clientSocket.send(mensagem_envio)
                break
            elif mensagem[0:8].upper() == "PRIVADO(" and mensagem[-1] == ")":
                mensagem_envio = encapsular('SERVIDOR', 'PRIVADO', mensagem[8:-1])
            elif mensagem.upper() == "LISTA()":
                mensagem_envio = encapsular('SERVIDOR', 'LISTA', '')
            else:
                mensagem_envio = encapsular(remetente, '', mensagem)

            clientSocket.send(mensagem_envio)

    #metodo para o recebimento das menssagens
    def receber():
        while True:
            #verificando a mensagem recebida
            mensagem_recebida = clientSocket.recv(1024)
            tamanho, remetente, comando, dados = desencapsular(mensagem_recebida)
            if comando == 'SAIR':
                mensagem_envio = encapsular('SERVIDOR', 'SAIR', '')
                print(dados)
                clientSocket.send(mensagem_envio)
                clientSocket.close()
                break
            print(dados)