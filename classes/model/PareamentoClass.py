'''
Created on 09/10/2012

@author: diogo
'''
import random, math

class PareamentoClass(object):
    '''
    Modelo de Pareamento de peers
    '''


    def __init__(self,lista_peers):
        '''
        Inicializa o objeto de pareamento usando uma lista de peers
        '''
        self.lista_peers = lista_peers;
        self.pareamento = {};
        
    def pareia(self,tipo_pareamento='aleatorio'):
        '''
        funcao que realiza pareamento entre peers
        '''
        if (tipo_pareamento == 'aleatorio'):
            return self.pareiaAleatorio();
        else:
            raise 'Erro de tipo de pareamento escolhido';
        
    def pareiaAleatorio(self):
        '''
        funcao que realiza pareamento aleatorio
        '''
        random.shuffle(self.lista_peers);
        lista1 = self.lista_peers[0:int(math.floor(len(self.lista_peers)/2))];
        lista2 = self.lista_peers[int(math.floor(len(self.lista_peers)/2)):];

        for i in range(1,len(lista1)+1):
            self.pareamento[lista1[i-1]] = lista2[i-1];
        if (len(lista2) > len(lista1)):
            self.pareamento['sobrando'] = lista2[-1];
        return self.pareamento;  
