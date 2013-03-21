
# -*- coding: utf-8 -*-
'''
Created on 02/11/2012

@author: diogo
'''
import numpy 
import scipy.stats as stats


class MatematicaClass(object):
    '''
    Classe geradora de analises matematicas de acordo com resultados passados
    '''

    def __init__(self,dictDados):
        '''
        Inicializa classe geradora de analises matematicas com um dicionario de dados
        arquivo => [primeiro,segundo,terceiro...], sendo esses numeros inteiros
        '''
        self.dictDados = dictDados;
        numpy.seterr(all='ignore')
        self.quantidade = 0
    
    def juntaMesmoTipo(self):
        '''
        Funcao que junta os arquivos do mesmo tipo para realizar trsnformacoes matematicas
        '''
        self.dadosOrganizados = {'sequential':{},'aleatory':{}}
        for arquivo in self.dictDados:
            download = arquivo[arquivo.find('/resultado')+11:arquivo.rfind('/')]
            resto = arquivo[arquivo.find('_Q'):]
            if (self.dadosOrganizados[download].has_key(download+resto)):                                                
                self.dadosOrganizados[download][download+resto].append(self.dictDados[arquivo])
            else:
                self.dadosOrganizados[download].setdefault(download+resto,[self.dictDados[arquivo]])
                self.quantidade += 1
        
    def confianca(self):
        '''
        funcao que realiza intervalo de confianca de cada serie de amostra
        '''
        self.juntaMesmoTipo()
        for download in self.dadosOrganizados:
            for serie in self.dadosOrganizados[download]:
                interador = 0
                confianca = []
                for i in self.dadosOrganizados[download][serie][0]:
                    vetor = []                  
                    for numero in self.dadosOrganizados[download][serie]:
                        vetor.append(numero[interador])
                    if (len(list(set(vetor))) > 1):
                        confianca.append(stats.bayes_mvs(vetor,alpha=0.95)[0])
                    else:
                        confianca.append((vetor[0],(0,0)))
                    
                    interador += 1
                self.dadosOrganizados[download][serie].append({'confianca':confianca})
        return self.dadosOrganizados, self.quantidade