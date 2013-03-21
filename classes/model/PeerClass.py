'''
Created on 09/10/2012

@author: diogo
'''

class PeerClass(object):
    '''
    Modelo de peer do sistema que possui playlist
    '''


    def __init__(self, nome=None, playlist=[], lista=[], consumo=None, troca=None, parado=None, wait_time=None):
        '''
        Inicializa a playlist que o peer tem, seu nome e lista de arquivos que possui
        consumo = {tempo:{arquivo:porcentagem}}
        troca = {tempo:{arquivo:porcentagem}}
        parado = {tempo:paradoAcumulado} do consumo
        wait_time = {tempo:waitAcumulado} do download
        '''
        if consumo is None: consumo = {0:{}};
        if troca is None: troca = {0:{}};
        if parado is None: parado = {0:0};
        if wait_time is None: wait_time = {0:0};
        self.playlist = playlist;
        self.nome = nome;
        self.lista = lista;
        self.consumo = consumo;
        self.troca = troca;
        self.parado = parado;
        self.wait_time = wait_time;
    

   
 
