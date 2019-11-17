# importacao das bibliotecas
from funcoes_servidor import *
from sys import *

thread_clientes = minhaThread(conexao_clientes)
thread_clientes.daemon = True
thread_clientes.start()
while (1):
    comandoServer = input()
    if comandoServer.upper() == "SAIR()":
        for sock in dicionario_clientes.keys():
            sock.send(encapsular('', 'SAIR', 'Servidor encerrando...'))
        serverSocket.close() # encerra o socket do servidor
        exit() #fecha o programa
    elif comandoServer.upper() == "LISTA()":
        if len(dicionario_clientes) is not 0:
            for nome_cliente, endereco_cliente in zip(dicionario_clientes.values(),dicionario_enderecos_clientes.values()):
                item = "<"+nome_cliente+","+endereco_cliente[0]+","+str(endereco_cliente[1])+">"
                print(item)       
        else:
            print("Nao existem nenhum cliente conectado!")

