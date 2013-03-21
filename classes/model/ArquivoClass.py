'''
Created on 09/10/2012

@author: diogo
'''

class ArquivoClass(object):
    '''
    Modelo de arquivos que estarao nas playlists
    '''


    def __init__(self,tipo_tamanho='unitario',nome=None):
        '''
        Inicializa nome e tipo do tamanho do arquivo
        '''
        self.nome = nome;
        self.tipo_tamanho = tipo_tamanho;
        self.tamanho = self.geraTamanho();
    
    
    def geraTamanho(self):
        '''
        Funcao que retorna tamanho de acordo com tipo_tamanho
        '''
        if (self.tipo_tamanho=='unitario'):
            return self.geraTamanhoUnitario();
        else:
            raise 'Erro de tipo de tamanho de arquivo';
        
    def geraTamanhoUnitario(self):
        '''
        Funcao que retorna tamanho unitario
        '''
        return 1;
        