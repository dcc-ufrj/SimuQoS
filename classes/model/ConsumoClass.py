'''
Created on 09/10/2012

@author: diogo
'''
from model import ListaArquivoClass

class ConsumoClass(ListaArquivoClass.ListaArquivoClass):
    '''
    Modelo de Consumo de arquivos dos peers
    '''

    def __init__(self,lista_peers):
        '''
        Inicializa o objeto de consumo usando uma lista de peers
        '''
        self.lista_peers = lista_peers;
        

    def temEventoNovo(self):
        '''
        Funcao que verifica novos eventos independente da ordem
        '''
        da_vez = self.pegaElementoDaVezConsumo(self.peer,self.tempo);
        if da_vez == -1:
            return False;
        else:
            return da_vez

    def temEventoSequencial(self):
        '''
        Funcao que verifica novos eventos de forma sequencial de acordo com a playlist
        '''
        da_vez = self.pegaUltimoElementoConsumo(self.peer,self.tempo);
        if da_vez == -1:
            return False;
        else:
            return da_vez


    def consumo(self,taxa_consumo,tempo,tipo_consumo,tempo_delay):
        '''
        funcao que realiza consumo de arquivo dos peers de acordo com a taxa de consumo
        '''
        self.tempo = tempo
        self.taxa_consumo = taxa_consumo;
        for peer in self.lista_peers:
            self.peer = peer;
            taxa_consumo = self.taxa_consumo;
            while(taxa_consumo > 0):
                if (tipo_consumo == 'sequential'):
                    evento_novo = self.temEventoSequencial();
                elif(tipo_consumo == 'aleatory'):
                    evento_novo = self.temEventoNovo();
                if(evento_novo):
                    

                    try:
                        if (self.peer.consumo[tempo][evento_novo] == self.peer.troca[tempo][evento_novo]):
                            self.peer.parado[tempo] += 1;
                            taxa_consumo = 0;
                        elif ((self.peer.consumo[tempo][evento_novo] + taxa_consumo) > self.peer.troca[tempo][evento_novo]):
                            taxa_consumo = (self.peer.troca[tempo][evento_novo] + taxa_consumo) - 100;
                            self.peer.consumo[tempo][evento_novo] = self.peer.troca[tempo][evento_novo];
                                        
                        elif ((self.peer.consumo[tempo][evento_novo] + taxa_consumo) >= 100):
                            taxa_consumo = (self.peer.consumo[tempo][evento_novo] + taxa_consumo) - 100;
                            self.peer.consumo[tempo][evento_novo] = 100;
                        else:
                            self.peer.consumo[tempo][evento_novo] += taxa_consumo;
                            taxa_consumo = 0;
                    except:
                        if ((self.peer.consumo[tempo][evento_novo] + taxa_consumo) >= 100):
                            taxa_consumo = (self.peer.consumo[tempo][evento_novo] + taxa_consumo) - 100;
                            self.peer.consumo[tempo][evento_novo] = 100;
                        else:
                            self.peer.consumo[tempo][evento_novo] += taxa_consumo;
                            taxa_consumo = 0;


                else:
                    self.peer.parado[tempo] += 1;
                    taxa_consumo = 0;
                    
                
