'''
Created on 09/10/2012

@author: diogo
'''
from model import ArquivoClass
import random, copy

class ListaArquivoClass(ArquivoClass.ArquivoClass):
    '''
    Classe geradora de listas de arquivos
    '''


    def geraListaAleatoria(self,tamanho,lista):
        '''
        Gera lista aleatoria baseado em outro objeto de lista de arquivos lista
        '''
        arquivos = [];
        copia_lista = copy.deepcopy(lista)
        for escolhido in range(tamanho):
            escolhido = random.choice(copia_lista);
            arquivos.append(escolhido);
            copia_lista.remove(escolhido);
        return arquivos;
    
    def geraListaSequencial(self,tamanho,tipo_tamanho_arquivo):
        '''
        Gera lista sequencial
        '''
        arquivos = [];
        for nome in range(1,tamanho+1):
            
            arquivos.append(ArquivoClass.ArquivoClass(tipo_tamanho_arquivo,nome));
        return arquivos;
     
    def ordenaListaByNome(self,lista):
        '''
        Ordena lista de arquivos
        '''
        return lista.sort(key = lambda x: x.nome);

    def procuraListaByNome(self,lista,buscado):
        '''
        Procura item em lista de objetos
        '''
        for i in lista:
            if (i.nome == buscado):
                return i;
        return False;
    
    def geraListaArquivoByPlaylist(self,lista,playlist,tamanho):
        '''
        Gera uma lista de arquivos retirando os elementos que estao na playlist
        '''
        diferenca = [x for x in lista if not self.procuraListaByNome(playlist,x.nome)]

        return self.geraListaAleatoria(tamanho, diferenca);
    
    def pegaElementoDaVez(self,peer):
        '''
        Funcao que retorna elemento da vez para download comparando com o que o usuario ja tem na lista de arquivos
        '''
        for item in peer.playlist:
            if not(self.procuraListaByNome(peer.lista, item.nome)):
                return peer.playlist.index(item);
        return -1;

    def pegaUltimoElementoConsumo(self,peer,tempo):
        '''
        Funcao que retorna o elemento sequencial que deve ser 
        consumido pelo usuario, caso nao tenha retorna -1
        '''
        for arquivo in peer.consumo[tempo]:
            if peer.consumo[tempo][arquivo] < 100:
                #peer.consumo[tempo].setdefault(arquivo,0)
                return arquivo
        indiceO = len(peer.playlist)+1
        for l in peer.troca.values():
            for item in l:
                outroItem = self.procuraListaByNome(peer.playlist,item.nome)
                if outroItem:
                    if (indiceO > peer.playlist.index(outroItem) and {item:100} not in peer.consumo.values()):
                        indiceO = peer.playlist.index(outroItem)
                        arquivo = outroItem
                        arquivoCerto = item
        indiceC = -1
        for l in peer.consumo.values():
            for item in l:
                outroItem = self.procuraListaByNome(peer.playlist,item.nome)
                if outroItem:
                    if (indiceC < peer.playlist.index(outroItem)):
                        indiceC = peer.playlist.index(outroItem)
                        arquivoCompara = outroItem
        try:
            arquivo
        except NameError:
            return -1
        try:
            arquivoCompara
        except:
            if abs(peer.playlist.index(arquivo)) == 0:
                peer.consumo[tempo].setdefault(arquivoCerto,0)
                return arquivoCerto
            else:
                return -1
        if abs(indiceC) == abs(indiceO-1):
            peer.consumo[tempo].setdefault(arquivoCerto,0)
            return arquivoCerto
        else:
            return -1

    def pegaElementoDaVezConsumo(self,peer,tempo):
        '''
        Funcao que retorna elemento da vez para consumo comparando com o que o 
        usuario ja tem na lista de arquivos
        '''
        for arquivo in peer.consumo[tempo]:
            if peer.consumo[tempo][arquivo] < 100:
                #peer.consumo[tempo].setdefault(arquivo,0)
                return arquivo
        lista = []
        for l in peer.troca.values():
            for item in l:
               if ({item:100} not in peer.consumo.values()):
                    lista.append(item)

        for item in lista:
            if self.procuraListaByNome(lista, item.nome):
                peer.consumo[tempo].setdefault(item,0)
                return item

        return -1
    
    def pegaElementosPossiveis(self,peer):
        '''
        Funcao que pega todos os elementos que sao possiveis de serem pegos da playlist baseado na lista de itens do usuario
        '''
        lista =[];
        for item in peer.playlist:
            if not(self.procuraListaByNome(peer.lista, item.nome)):
                lista = lista + [peer.playlist.index(item)];
        return lista;
        
                