
# -*- coding: utf-8 -*-

'''
Created on 11/10/2012

@author: diogo
'''

from model import GraficoClass
from time import gmtime, strftime

class ResultadoController():
    '''
    Controlador de resultados e geracao de graficos da aplicacao
    
    '''

    def __init__(self):
        self.main();

    def main(self):
        nome_padrao = strftime("%d-%m-%Y_%H:%M:%S", gmtime());
        
        grafico = GraficoClass.GraficoClass();
        
        #grafico.tempoDownload("Download_"+nome_padrao+'.svg');  
        grafico.tempoDownloadAcumulado("DownloadAcumulado_"+nome_padrao+'.svg');
        #grafico.tempoConsumo("Consumo_"+nome_padrao+'.svg');
        grafico.tempoConsumoAcumulado("ConsumoAcumulado_"+nome_padrao+'.svg');
        #grafico.tempoPeersSemDownload("SemDownload_"+nome_padrao+'.svg');
        grafico.tempoPeersSemDownloadAcumulado("SemDownloadAcumulado_"+nome_padrao+'.svg');
        #grafico.tempoPeersSemConsumo("SemConsumo_"+nome_padrao+'.svg');
        grafico.tempoPeersSemConsumoAcumulado("SemConsumoAcumulado_"+nome_padrao+'.svg');
        #grafico.parcelaDownloadAcumulado("Parcela_"+nome_padrao+'.svg');              
        
                    
