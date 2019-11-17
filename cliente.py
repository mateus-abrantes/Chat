# importacao das bibliotecas
from funcoes_cliente import *
if conexao:
    #iniciando a thread que ira enviar dados
    thread_envio = minhaThread(enviar)
    thread_envio.daemon = True
    thread_envio.start()
    #iniciando a thread que ira receber os dados
    thread_receber = minhaThread(receber)
    thread_receber.start()
