'''
Created on 20/10/2012

@author: diogo
'''
import os

class ResultadoClass(object):
    '''
    Classe geradora de resultados
    '''

    def __init__(self,lista_peer,arquivo='log.txt'):
        '''
        Inicializa classe geradora de relatorios com lista de peers, arquivo de saida e string final que ira ser montada
        '''
        self.lista_peer = lista_peer;
        self.arquivo = '../resultado/'+arquivo;
        self.final = '';
        
    def __repr__(self):
        '''
        funcao que imprime na tela as informacoes de cada peer
        '''
        return self.final;
    
    def geraLog(self):
        '''
        funcao que gera arquivo de log
        '''
        versao = 0;
        nome_arquivo = self.arquivo;
        while(os.path.isfile(nome_arquivo)):
            versao = versao+1;
            nome_arquivo = self.arquivo +'_'+ str(versao);
        
        aberto = open(nome_arquivo,"w");
        aberto.write(self.final);
        aberto.close();
        return nome_arquivo;

    def geraLogIncremental(self):
        '''
        funcao que gera arquivo de log incremental
        '''
        nome_arquivo = self.arquivo;
        aberto = open(nome_arquivo,"a");
        aberto.write(self.final);
        aberto.close();
        self.final = '';
        return nome_arquivo;

    def montaLog(self,tempo):
        '''
        funcao que monta o log que pode ser exibido ou salvo com base no tempo
        '''
        self.final += "T,"+str(tempo)+"\n";
        for peer in range(0,len(self.lista_peer)):
            self.final += "N,"+str(self.lista_peer[peer].nome)+"\n";
            self.final += "P";
            for arquivo in self.lista_peer[peer].playlist:
                self.final += ","+str(arquivo.nome);
                self.final += ","+str(arquivo.tamanho);
            self.final += "\nL";
            for arquivo in self.lista_peer[peer].lista:
                self.final += ","+str(arquivo.nome);
                self.final += ","+str(arquivo.tamanho);
            self.final += "\nD";
            for troca in self.lista_peer[peer].troca[tempo]:
                self.final += ','+ str(troca.nome);
                self.final += ','+ str(troca.tamanho);
                self.final += ','+ str(self.lista_peer[peer].troca[tempo][troca]);
            self.final += '\nC';
            for consumo in self.lista_peer[peer].consumo[tempo]:
                self.final += ','+str(consumo.nome);
                self.final += ','+str(consumo.tamanho);
                self.final += ','+str(self.lista_peer[peer].consumo[tempo][consumo]);
            self.final += '\nS';
            self.final += ','+str(self.lista_peer[peer].parado[tempo]);
            self.final += '\nW';
            self.final += ','+str(self.lista_peer[peer].wait_time[tempo]);

            self.final += '\n';
                                    
    def montaTexto(self):
        '''
        funcao que monta o texto que pode ser exibido ou salvo
        '''
        for peer in range(0,len(self.lista_peer)):
            self.final += "Nome do Peer: "+str(self.lista_peer[peer].nome)+"\n";
            self.final += "\n Playlist: \n";
            for arquivo in self.lista_peer[peer].playlist:
                self.final += "Nome do Arquivo: "+str(arquivo.nome)+"\n";
                self.final += "Tamanho do Arquivo: "+str(arquivo.tamanho)+"\n";
            self.final += "\n Lista de Arquivos \n:";
            for arquivo in self.lista_peer[peer].lista:
                self.final += "Nome do Arquivo: "+str(arquivo.nome)+"\n";
                self.final += "Tamanho do Arquivo: "+str(arquivo.tamanho)+"\n";
            self.final += "\n Eventos Ocorridos: \n";
            for evento in self.lista_peer[peer].troca:
                if (evento == ''):
                    self.final += 'Nenhuma Troca \n';
                else:
                    self.final += 'Trocado arquivo '+ str(evento.nome)+'\n';
            for consumo in self.lista_peer[peer].consumo:
                if (consumo == 'parado'):
                    self.final += 'Parado'+str(self.lista_peer[peer].consumo[consumo])+' tempos \n';
                else:
                    self.final += 'Consumido '+ str(self.lista_peer[peer].consumo[consumo])+'% do arquivo '+ str(consumo.nome)+'\n';            
            self.final += '\n\n';
                                 
 
        