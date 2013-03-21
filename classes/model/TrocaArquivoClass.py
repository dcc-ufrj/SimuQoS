'''
Created on 09/10/2012

@author: diogo
'''
from model import ListaArquivoClass

class TrocaArquivoClass(ListaArquivoClass.ListaArquivoClass):
    '''
    Modelo de troca de arquivos entre peers
        CONTINUAR realizaTroca
    '''


    def __init__(self, lista_pareada):
        '''
        Inicializa o objeto de troca de arquivos que recebe uma lista pareada
        {peer1 : peer2 ...}
        '''
        self.lista_pareada = lista_pareada;
        
    def trocaArquivo(self, quantidade_trocada, tempo, tipo_troca,taxa_download):
        '''
        funcao que realiza troca de arquivos entre peers
        '''
        self.taxa_download = taxa_download;
        self.tempo = tempo;
        self.quantidade_trocada = quantidade_trocada;
        for self.pareado in self.lista_pareada:
            for self.numero in range(0, self.quantidade_trocada):
                if (self.pareado == 'sobrando'):
                    self.lista_pareada[self.pareado].wait_time[tempo] += 1;
                else:        
                    if (tipo_troca == 'sequential'):
                        self.trocaArquivoSequencial();
                    elif (tipo_troca == 'aleatory'):
                        self.trocaArquivoPrimeiro();
                    else:
                        raise 'Erro em tipo de troca de arquivo escolhido';
                        break;
        
    def trocaArquivoSequencial(self):
        '''
        funcao que troca arquivos sequencialmente de acordo com a playlist
        
        '''
        
        self.ordenaListaByNome(self.pareado.lista);
        self.ordenaListaByNome(self.pareado.playlist);
        self.ordenaListaByNome(self.lista_pareada[self.pareado].lista);
        self.ordenaListaByNome(self.lista_pareada[self.pareado].playlist);
        taxa_download = self.taxa_download
        da_vez = 1
        self.existe = True
        while (da_vez != -1 and taxa_download > 0 and self.existe):
            da_vez = self.pegaElementoDaVez(self.lista_pareada[self.pareado]);
            if (da_vez != -1):
                self.existe = self.procuraListaByNome(self.pareado.lista, self.lista_pareada[self.pareado].playlist[da_vez].nome);
                if (self.existe):
                    taxa_download = self.realizaTroca(self.pareado, self.lista_pareada[self.pareado], taxa_download);
                else:
                    self.lista_pareada[self.pareado].wait_time[self.tempo] += 1;
            else:
                self.lista_pareada[self.pareado].wait_time[self.tempo] += 1;

        taxa_download = self.taxa_download
        da_vez = 1
        self.existe = True
        while (da_vez != -1 and taxa_download > 0 and self.existe):
            da_vez = self.pegaElementoDaVez(self.pareado);
            if (da_vez != -1):
                self.existe = self.procuraListaByNome(self.lista_pareada[self.pareado].lista, self.pareado.playlist[da_vez].nome);
                if (self.existe):
                    taxa_download = self.realizaTroca(self.lista_pareada[self.pareado], self.pareado, taxa_download);
                else:
                    self.pareado.wait_time[self.tempo] += 1;
            else:
                self.pareado.wait_time[self.tempo] += 1;

    def trocaArquivoPrimeiro(self):
        '''
        funcao que troca arquivos que aparecerem primeiro de uma playlist na lista de outro peer
        '''
        taxa_download = self.taxa_download
        elementos = self.pegaElementosPossiveis(self.lista_pareada[self.pareado]);
        trocado = False;
        for da_vez in elementos:
            self.existe = self.procuraListaByNome(self.pareado.lista, self.lista_pareada[self.pareado].playlist[da_vez].nome);
            if (self.existe):
                taxa_download = self.realizaTroca(self.pareado, self.lista_pareada[self.pareado], taxa_download);
                trocado = True;
                if (taxa_download == 0):
                    break;
        if (elementos == []) or not(trocado):
            self.lista_pareada[self.pareado].wait_time[self.tempo] += 1;

        taxa_download = self.taxa_download
        elementos = self.pegaElementosPossiveis(self.pareado);
        trocado = False;
        for da_vez in elementos:
            self.existe = self.procuraListaByNome(self.lista_pareada[self.pareado].lista, self.pareado.playlist[da_vez].nome);
            if (self.existe):
                taxa_download = self.realizaTroca(self.lista_pareada[self.pareado], self.pareado, taxa_download);
                trocado = True;
                if (taxa_download == 0):
                    break;
        if (elementos == []) or not(trocado):
            self.pareado.wait_time[self.tempo] += 1;                           
    
    def realizaTroca(self, doador, aceptor,taxa_download):
        '''
        funcao que efetivamente realiza a troca de arquivos e adiciona a lista de eventos do aceptor
        '''
        indice = doador.lista.index(self.existe);
        chave = self.procuraListaByNome(aceptor.troca[self.tempo].keys(),self.existe.nome)
        if (chave):
            if (aceptor.troca[self.tempo][chave] + taxa_download) >= 100:
                taxa_download = (aceptor.troca[self.tempo][chave] + taxa_download) - 100
                aceptor.troca[self.tempo][chave] = 100;
                aceptor.lista.append(chave)
            else:
                aceptor.troca[self.tempo][chave] += taxa_download;
                taxa_download = 0
        else:
            if taxa_download >= 100:      
                aceptor.troca[self.tempo].setdefault(doador.lista[indice],100);
                aceptor.lista.append(doador.lista[indice])
                taxa_download = taxa_download - 100
            else:
                aceptor.troca[self.tempo].setdefault(doador.lista[indice],taxa_download);
                taxa_download = 0

        return taxa_download
