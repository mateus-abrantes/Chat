#Importando bibliotecas
from socket import *
import threading


class minhaThread(threading.Thread):
    #Definicao do "Construtor" 
    def __init__(self, funcao, args=None):
        threading.Thread.__init__(self)
        self.funcao = funcao
        self.args = args

    #metodo principal
    def run(self):
        #verifica se a funcao passada tem paramentros
        if self.args is not None:
            self.funcao(self.args)
        else:
            self.funcao()

