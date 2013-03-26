
# -*- coding: utf-8 -*-

'''
Created on 11/10/2012

@author: diogo
'''
import os
from model import PeerClass, ListaArquivoClass, PareamentoClass, TrocaArquivoClass, ResultadoClass, ConsumoClass, PlaylistClass
from time import gmtime, strftime

class MainController():
    '''
    Controlador principal da aplicacao
    
    '''


    def __init__(self, argumentos):
        self.argumentos = argumentos;
        self.main();

    def main(self):
        if (len(self.argumentos) == 13):
            quantidade_peers, tamanho_playlist, tamanho_lista_peer, tamanho_lista_arquivo, tipo_tamanho_arquivo, tipo_pareamento, quantidade_trocada, tipo_troca, taxa_download, repeticao, tipo_consumo, taxa_consumo, tempo_delay = self.argumentos;
            nome_padrao = strftime("%d-%m-%Y_%H:%M:%S", gmtime())+"_Q"+quantidade_peers+"_P"+tamanho_playlist+"_L"+tamanho_lista_peer+"_S"+tamanho_lista_arquivo+"_R"+taxa_consumo+"_V"+repeticao+"_Y"+tipo_consumo+"_X"+taxa_download+"_D"+tempo_delay;
            lista = ListaArquivoClass.ListaArquivoClass();   
            lista_arquivos = lista.geraListaSequencial(int(tamanho_lista_arquivo), tipo_tamanho_arquivo);
            lista_peer = self.geraListaPeer(lista_arquivos, int(tamanho_playlist), int(quantidade_peers), int(tamanho_lista_peer));
            resultado = ResultadoClass.ResultadoClass(lista_peer,os.path.join(tipo_troca,nome_padrao+'.txt')); 
            for tempo in range(1,int(repeticao)+1):
                self.avancaTempo(tempo, lista_peer)
                pareamento = PareamentoClass.PareamentoClass(lista_peer);
                pareado = pareamento.pareia(tipo_pareamento);
                troca = TrocaArquivoClass.TrocaArquivoClass(pareado);
                troca.trocaArquivo(int(quantidade_trocada), tempo, tipo_troca,int(taxa_download));
                consumo = ConsumoClass.ConsumoClass(lista_peer);
                consumo.consumo(int(taxa_consumo),tempo,tipo_consumo,tempo_delay);
                resultado.montaLog(tempo);
                resultado.geraLogIncremental();

            
        else:
            print "usage: python Main.py Q P L S A C N T R V Y X D\n\n" \
            "Q = quantidade de peers que o sistema possui\n\n" \
            "P = tamanho da playlist de cada peer no sistema\n\n" \
            "L = tamanho da lista de arquivos de cada peer do sistema\n\n" \
            "S = tamanho (size) da lista de arquivos total do sistema (precisa ser maior que a lista dos peers e do que a playlist\n\n"\
            "A = tipo de tamanho de cada arquivo do sistema. Atualmente só é suportado A = unitario\n\n"\
            "C = tipo de cruzamento/pareamento. Atualmente só é suportado C = aleatorio\n\n"\
            "N = número de trocas de arquivos feitas a cada pareamento\n\n"\
            "T = tipo de troca. Atualmente é aceito T = sequential ou T = aleatory\n"\
            "\tsequential é a troca seguindo exatamente a ordem da playlist\n"\
            "\taleatory é a troca do primeiro elemento que encontrar para tocar da playlist\n\n"\
            "X = taxa de download do arquivo. É um inteiro de 1 a 100\n\n"\
            "V = quantidade de vezes que será repetido (timeslot)\n\n"\
            "Y = tipo de consumo. Atualmente é aceito Y = sequential ou Y = aleatory\n"\
            "\tsequential é o consumo seguindo exatamente a ordem da playlist\n"\
            "\taleatory é o consumo do primeiro elemento que encontrar para tocar da playlist\n\n"\
            "R = taxa de reprodução/consumo do arquivo. É um inteiro de 1 a 100\n\n"\
            "D = tempo de delay para comecar o consumo do arquivo. É um inteiro\n\n";
            
    def geraListaPeer(self, lista_arquivos, tamanho_playlist, quantidade, tamanho_lista_arquivo):
        '''
        Funcao geradora de peers
        '''
        peers = [];
        for peer in range(1, quantidade+1):
           
            playlistClass = PlaylistClass.PlaylistClass();
            
            playlist = playlistClass.geraPlaylist(lista_arquivos,tamanho_playlist);
            
            lista_de_arquivo = playlistClass.geraListaArquivoByPlaylist(lista_arquivos,playlist,tamanho_lista_arquivo);
            
            peers.append(PeerClass.PeerClass(peer, playlist, lista_de_arquivo)); 
        return peers;
    
    def avancaTempo(self,tempo,lista_peer):
        '''
        funcao que avanca no tempo arquivos e parametros que vao precisar no proximo
        tempo
        '''
        for peer in lista_peer:
            peer.consumo.setdefault(tempo,{})
            for arquivo in peer.consumo[tempo-1]:
                if peer.consumo[tempo-1][arquivo] < 100:
                    peer.consumo[tempo][arquivo]=peer.consumo[tempo-1][arquivo]
            peer.troca.setdefault(tempo,{})
            for arquivo in peer.troca[tempo-1]:
                if peer.troca[tempo-1][arquivo] < 100:
                    peer.troca[tempo][arquivo]=peer.troca[tempo-1][arquivo]
            peer.parado.setdefault(tempo,0)
            peer.wait_time.setdefault(tempo,0)
                
                    
