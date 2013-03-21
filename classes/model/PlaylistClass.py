'''
Created on 09/10/2012

@author: diogo
'''
from model import ListaArquivoClass

class PlaylistClass(ListaArquivoClass.ListaArquivoClass):
    '''
    Modelo de Playlist de peers
    '''

  
    def geraPlaylist(self,arquivos_totais,tamanho):
        '''
        Gera playlist baseado nos arquivos totais de forma aleatoria
        '''
        
        return self.geraListaAleatoria(tamanho, arquivos_totais);