
# -*- coding: utf-8 -*-
'''
Created on 02/11/2012

@author: diogo
'''
from MatematicaClass import MatematicaClass
from series import Series
import cairo
import cairoplot
import os
import glob
import matplotlib.pyplot as plt
import numpy
from pylab import *


class GraficoClass(object):
    '''
    Classe geradora de graficos
    '''

    def __init__(self,caminhos=[os.path.join('..','resultado','aleatory'),os.path.join('..','resultado','sequential')], caminho = os.path.join('..','grafico')):
        '''
        Inicializa classe geradora de graficos com arquivo que sera usado para gera-los
        '''
        self.caminhos = caminhos;
        self.caminho = caminho;
        self.largura = 1440;
        self.altura = 1080;
        self.arquivos = []
        self.getArquivos()
    
    def getArquivos(self):
        for caminho in self.caminhos:
            self.arquivos += glob.glob(os.path.join(caminho,"*.txt"));
    
    def tempoDownload(self,nome='tempoxNdownload.svg'):
        '''
        Organiza dados de tempo x numero de dwonloads efetivados
        x=[tempo1,tempo2, ...]
        y=[nDownload, nDownload, ...]
        '''
        total = {};
        for arquivo in self.arquivos:
            self.aberto = open(arquivo,"r");
            tempo,quantidade =[],[];
            numero = 0
            tempo.append('0');
            for linha in self.aberto:
                linha = linha.rstrip();
                lista = linha.split(',');
                if (lista[0] == 'T'):
                    tempo.append(lista[1]);
                    if lista[1] > 1:
                        quantidade.append(numero);
                        numero = 0
                elif (lista[0] == 'D'):
                    while '' in lista:
                        lista.remove('');
                    if(len(lista) > 1):
                        indice = 3;
                        while(lista[indice]):
                            if (lista[indice] == '100'):
                                numero += 1;
                            try:
                                indice += 3;
                                lista[indice]
                            except:
                                break
            quantidade.append(numero);
            self.aberto.close();
            total[arquivo] = quantidade
        data = Series(total)
        
        cairoplot.dot_line_plot(os.path.join(self.caminho,nome),data,self.largura,self.altura,x_labels = tempo,
                                 axis = True, grid = True, x_title = "Tempo", y_title = "Nº de Downloads", series_legend=True);

    def tempoDownloadAcumulado(self,nome='tempoxNdownloadacum.svg'):
        '''
        Organiza dados de arquivo x numero de dwonloads efetivados
        x=[arquivo1,arquivo2, ...]
        y=[nDownload, nDownload, ...]
        '''
        total = {};
        dados = [];
        for arquivo in self.arquivos:
            self.aberto = open(arquivo,"r");
            quantidade =[];
            numero = 0
            for linha in self.aberto:
                linha = linha.rstrip();
                lista = linha.split(',');
                if (lista[0] == 'D'):
                    while '' in lista:
                        lista.remove('');
                    if(len(lista) > 1):
                        indice = 3;
                        while(lista[indice]):
                            if (lista[indice] == '100'):
                                numero += 1;
                            try:
                                indice += 3;
                                lista[indice]
                            except:
                                break
            quantidade.append(numero);
            self.aberto.close();
            dados.append(quantidade)
            total[arquivo] = quantidade
        
        mat = MatematicaClass(total)
        #montando novo
        organizados, N = mat.confianca()
        N = 4
        fig = plt.figure()
        ax = fig.add_subplot(111)
        nomesProntos, mediasProntas, ercProntos, erbProntos = [],[0],[0],[0]
        cor, rects = [],[]
        cm = get_cmap('gist_rainbow')
        for i in range(N):
            cor.append(cm(1.*i/N))  # color will now be an RGBA tuple
        cor = iter(cor)
        dictItems = {'sequentialaleatory':[],'aleatorysequential':[],'sequentialsequential':[],'aleatoryaleatory':[]}
        for elementos in organizados.values():
            for elemento in elementos:
                item = ItemClass(elemento)
                item.elemento = elementos[elemento]
                dictItems[item.tipoDownload+item.tipoConsumo].append(item)
                dictItems[item.tipoDownload+item.tipoConsumo].sort(key = lambda x: int(x.download))
        for elementos in dictItems.values():
            for elemento in elementos:
                nomesProntos.append(str(elemento.tipoDownload) + "Download "+ ", "+ str(elemento.tipoConsumo)+" Consumption")
                nomesProntos = set(nomesProntos)
                nomesProntos = list(nomesProntos)
                media, (erc,erb) = elemento.elemento[-1]['confianca'][0]
                media, erc, erb
                mediasProntas.append(float("{0:.2f}".format(media)))
                ercProntos.append(media-erc)
                erbProntos.append(erb-media)
            legendasX = [0,10,30,50,70,100]
            rects.append(ax.errorbar(legendasX, mediasProntas, yerr=[erbProntos,ercProntos],color=cor.next(),fmt='--'))
            mediasProntas, ercProntos, erbProntos = [0],[0],[0]
                    
        # algo mais
        ax.set_ylabel('Quantidade de Downloads Finalizados')
        ax.set_xlabel('Taxa de Download')
        ax.set_title('Download Acumulado')
        ax.grid(True)
        ax.set_xticks(legendasX)
        ax.set_xticklabels(legendasX)
        ax.set_ylim(bottom=-10,top=7000)
        #ax.set_yscale('log')
        leg = ax.legend(rects,nomesProntos,loc='upper center', bbox_to_anchor=(0.5,-0.1))
        for t in leg.get_texts():
            t.set_fontsize('small')
        plt.savefig(os.path.join(self.caminho,nome), bbox_extra_artists=(leg,), bbox_inches='tight')
        ax.set_yscale('log')
        ax.set_ylabel('Quantidade de Downloads Finalizados (log)')
        plt.savefig(os.path.join(self.caminho,'log'+nome), bbox_extra_artists=(leg,), bbox_inches='tight')
        #fim da montagem
        
        #cairoplot.horizontal_bar_plot(os.path.join(self.caminho,nome),dados,self.largura,self.altura, y_labels = self.arquivos,
         #                       border = 20, display_values = True, rounded_corners = True, colors = [(0.5,0.2,0)]);
        
        
                                         
    def tempoConsumo(self,nome='tempoxNconsumo.svg'):
        '''
        Organiza dados de tempo x numero de consumos efetivados
        x=[tempo1,tempo2, ...]
        y=[nConsumo, nConsumo, ...]
        '''
        total = {};
        for arquivo in self.arquivos:
            self.aberto = open(arquivo,"r");
            tempo,quantidade =[],[];
            numero = 0
            tempo.append('0');
            for linha in self.aberto:
                linha = linha.rstrip();
                lista = linha.split(',');
                if (lista[0] == 'T'):
                    tempo.append(lista[1]);
                    if lista[1] > 1:
                        quantidade.append(numero);
                        numero = 0
                elif (lista[0] == 'C'):
                    while '' in lista:
                        lista.remove('');
                    if(len(lista) > 1):
                        indice = 3;
                        while(lista[indice]):
                            if (lista[indice] == '100'):
                                numero += 1;
                            try:
                                indice += 3;
                                lista[indice]
                            except:
                                break
            quantidade.append(numero);
            self.aberto.close();
            total[arquivo] = quantidade
        data = Series(total)
        
        cairoplot.dot_line_plot(os.path.join(self.caminho,nome),data,self.largura,self.altura,x_labels = tempo,
                                 axis = True, grid = True, x_title = "Tempo", y_title = "Nº de Consumo", series_legend=True);
            
    def tempoConsumoAcumulado(self,nome='tempoxNconsumoacum.svg'):
        '''
        Organiza dados de arquivo x numero de consumos efetivados
        x=[arquivo1,arquivo2, ...]
        y=[nConsumo, nConsumo, ...]
        '''
        total = {};
        dados = [];
        for arquivo in self.arquivos:
            self.aberto = open(arquivo,"r");
            quantidade =[];
            numero = 0
            for linha in self.aberto:
                linha = linha.rstrip();
                lista = linha.split(',');
                if (lista[0] == 'C'):
                    while '' in lista:
                        lista.remove('');
                    if(len(lista) > 1):
                        indice = 3;
                        while(lista[indice]):
                            if (lista[indice] == '100'):
                                numero += 1;
                            try:
                                indice += 3;
                                lista[indice]
                            except:
                                break
            quantidade.append(numero);
            self.aberto.close();
            dados.append(quantidade)
            total[arquivo] = quantidade

        mat = MatematicaClass(total)
        organizados, N = mat.confianca()
        N = 4
        fig = plt.figure()
        ax = fig.add_subplot(111)
        nomesProntos, mediasProntas, ercProntos, erbProntos = [],[0],[0],[0]
        cor, rects = [],[]
        cm = get_cmap('gist_rainbow')
        for i in range(N):
            cor.append(cm(1.*i/N))  # color will now be an RGBA tuple
        cor = iter(cor)
        dictItems = {'sequentialaleatory':[],'aleatorysequential':[],'sequentialsequential':[],'aleatoryaleatory':[]}
        for elementos in organizados.values():
            for elemento in elementos:
                item = ItemClass(elemento)
                item.elemento = elementos[elemento]
                dictItems[item.tipoDownload+item.tipoConsumo].append(item)
                dictItems[item.tipoDownload+item.tipoConsumo].sort(key = lambda x: int(x.download))
        for elementos in dictItems.values():
            for elemento in elementos:
                nomesProntos.append(str(elemento.tipoDownload) + "Download "+ ", "+ str(elemento.tipoConsumo)+" Consumption")
                nomesProntos = set(nomesProntos)
                nomesProntos = list(nomesProntos)
                media, (erc,erb) = elemento.elemento[-1]['confianca'][0]
                media, erc, erb
                mediasProntas.append(float("{0:.2f}".format(media)))
                ercProntos.append(media-erc)
                erbProntos.append(erb-media)
            legendasX = [0,10,30,50,70,100]
            rects.append(ax.errorbar(legendasX, mediasProntas, yerr=[erbProntos,ercProntos],color=cor.next(),fmt='--o'))
            mediasProntas, ercProntos, erbProntos = [0],[0],[0]       
        # algo mais
        ax.set_ylabel('Quantidade de Consumo Finalizados')
        ax.set_title('Consumo Acumulado')
        ax.set_xlabel('Taxa de Download')
        ax.grid(True)
        ax.set_xticks(legendasX)
        ax.set_xticklabels(legendasX)
        ax.set_ylim(bottom=-10,top=7000)
        #ax.set_yscale('log')
        leg = ax.legend(rects,nomesProntos,loc='upper center', bbox_to_anchor=(0.5,-0.1))
        for t in leg.get_texts():
            t.set_fontsize('small')
        plt.savefig(os.path.join(self.caminho,nome), bbox_extra_artists=(leg,), bbox_inches='tight')
        ax.set_yscale('log')
        ax.set_ylabel('Quantidade de Consumo Finalizados (log)')
        plt.savefig(os.path.join(self.caminho,'log'+nome), bbox_extra_artists=(leg,), bbox_inches='tight')
        
 
       # cairoplot.horizontal_bar_plot(os.path.join(self.caminho,'2'+nome),dados,self.largura,self.altura, y_labels = self.arquivos,
        #                        border = 20, display_values = True, rounded_corners = True, colors = [(0.5,0.2,0)]);
        


    def tempoPeersSemDownload(self,nome='tempoxNsemdownload.svg'):
        '''
        Organiza dados de tempo x numero de peers sem fazer download naquele tempo
        x=[tempo1,tempo2, ...]
        y=[nPeers, nPeers, ...]
        '''
        total = {};
        for arquivo in self.arquivos:
            self.aberto = open(arquivo,"r");
            tempo,quantidade =[],[];
            numero = 0
            tempo.append('0');
            for linha in self.aberto:
                linha = linha.rstrip();
                lista = linha.split(',');
                if (lista[0] == 'T'):
                    tempo.append(lista[1]);
                    if lista[1] > 1:
                        quantidade.append(numero);
                        numero = 0
                elif (lista[0] == 'W'):
                    while '' in lista:
                        lista.remove('');
                    if(lista[1] == '1'):
                        numero += 1;
                            
            quantidade.append(numero);
            self.aberto.close();
            total[arquivo] = quantidade
        data = Series(total)
        
        cairoplot.dot_line_plot(os.path.join(self.caminho,nome),data,self.largura,self.altura,x_labels = tempo,
                                 axis = True, grid = True, x_title = "Tempo", y_title = "Nº de Peers com Download Parado", series_legend=True);
            
    def tempoPeersSemDownloadAcumulado(self,nome='tempoxNsemdownloadacum.svg'):
        '''
        Organiza dados de arquivo x numero de peers sem fazer download acumulado
        x=[arquivo1,arquivo2, ...]
        y=[nPeers, nPeers, ...]
        '''
        total = {};
        dados = [];
        for arquivo in self.arquivos:
            self.aberto = open(arquivo,"r");
            quantidade =[];
            numero = 0
            for linha in self.aberto:
                linha = linha.rstrip();
                lista = linha.split(',');
                if (lista[0] == 'W'):
                    while '' in lista:
                        lista.remove('');
                    if(lista[1] == '1'):
                        numero += 1;
            quantidade.append(numero);
            self.aberto.close();
            dados.append(quantidade)
            total[arquivo] = quantidade

        mat = MatematicaClass(total)
        organizados, N = mat.confianca()
        N = 4
        fig = plt.figure()
        ax = fig.add_subplot(111)
        nomesProntos, mediasProntas, ercProntos, erbProntos = [],[0],[0],[0]
        cor, rects = [],[]
        cm = get_cmap('gist_rainbow')
        for i in range(N):
            cor.append(cm(1.*i/N))  # color will now be an RGBA tuple
        cor = iter(cor)
        dictItems = {'sequentialaleatory':[],'aleatorysequential':[],'sequentialsequential':[],'aleatoryaleatory':[]}
        for elementos in organizados.values():
            for elemento in elementos:
                item = ItemClass(elemento)
                item.elemento = elementos[elemento]
                dictItems[item.tipoDownload+item.tipoConsumo].append(item)
                dictItems[item.tipoDownload+item.tipoConsumo].sort(key = lambda x: int(x.download))
        for elementos in dictItems.values():
            for elemento in elementos:
                nomesProntos.append(str(elemento.tipoDownload) + "Download "+ ", "+ str(elemento.tipoConsumo)+" Consumption")
                nomesProntos = set(nomesProntos)
                nomesProntos = list(nomesProntos)
                media, (erc,erb) = elemento.elemento[-1]['confianca'][0]
                media, erc, erb
                mediasProntas.append(float("{0:.2f}".format(media)))
                ercProntos.append(media-erc)
                erbProntos.append(erb-media)
            legendasX = [0,10,30,50,70,100]
            rects.append(ax.errorbar(legendasX, mediasProntas, yerr=[erbProntos,ercProntos],color=cor.next(),fmt='--o'))
            mediasProntas, ercProntos, erbProntos = [0],[0],[0]    
        # algo mais
        ax.set_ylabel('Tempo de Peers sem Download')
        ax.set_title('Tempo Acumulado sem Download')
        ax.set_xlabel('Taxa de Download')
        ax.grid(True)
        ax.set_xticks(legendasX)
        ax.set_xticklabels(legendasX)
        ax.set_ylim(bottom=-10,top=7000)
        #ax.set_yscale('log')
        leg = ax.legend(rects,nomesProntos,loc='upper center', bbox_to_anchor=(0.5,-0.1))
        for t in leg.get_texts():
            t.set_fontsize('small')
        plt.savefig(os.path.join(self.caminho,nome), bbox_extra_artists=(leg,), bbox_inches='tight')
        ax.set_yscale('log')
        ax.set_ylabel('Tempo de Peers sem Download (log)')
        plt.savefig(os.path.join(self.caminho,'log'+nome), bbox_extra_artists=(leg,), bbox_inches='tight')
 
        #cairoplot.horizontal_bar_plot(os.path.join(self.caminho,'2'+nome),dados,self.largura,self.altura, y_labels = self.arquivos,
         #                       border = 20, display_values = True, rounded_corners = True, colors = [(0.5,0.2,0)]);
        

    def tempoPeersSemConsumo(self,nome='tempoxNsemconsumo.svg'):
        '''
        Organiza dados de tempo x numero de peers sem fazer consumo naquele tempo
        x=[tempo1,tempo2, ...]
        y=[nPeers, nPeers, ...]
        '''
        total = {};
        for arquivo in self.arquivos:
            self.aberto = open(arquivo,"r");
            tempo,quantidade =[],[];
            numero = 0
            tempo.append('0');
            for linha in self.aberto:
                linha = linha.rstrip();
                lista = linha.split(',');
                if (lista[0] == 'T'):
                    tempo.append(lista[1]);
                    if lista[1] > 1:
                        quantidade.append(numero);
                        numero = 0
                elif (lista[0] == 'S'):
                    while '' in lista:
                        lista.remove('');
                    if(lista[1] == '1'):
                        numero += 1;
                            
            quantidade.append(numero);
            self.aberto.close();
            total[arquivo] = quantidade
        data = Series(total)
        
        cairoplot.dot_line_plot(os.path.join(self.caminho,nome),data,self.largura,self.altura,x_labels = tempo,
                                 axis = True, grid = True, x_title = "Tempo", y_title = "Nº de Peers com Consumo Parado", series_legend=True);
            
    def tempoPeersSemConsumoAcumulado(self,nome='tempoxNsemconsumoacum.svg'):
        '''
        Organiza dados de arquivo x numero de peers sem fazer download acumulado
        x=[arquivo1,arquivo2, ...]
        y=[nPeers, nPeers, ...]
        '''
        
        total = {};
        dados = [];
        for arquivo in self.arquivos:
            self.aberto = open(arquivo,"r");
            quantidade =[];
            numero = 0
            for linha in self.aberto:
                linha = linha.rstrip();
                lista = linha.split(',');
                if (lista[0] == 'S'):
                    while '' in lista:
                        lista.remove('');
                    if(lista[1] == '1'):
                        numero += 1;
            quantidade.append(numero);
            self.aberto.close();
            dados.append(quantidade)
            total[arquivo] = quantidade

        mat = MatematicaClass(total)
        organizados, N = mat.confianca()
        N = 4
        fig = plt.figure()
        ax = fig.add_subplot(111)
        nomesProntos, mediasProntas, ercProntos, erbProntos = [],[0],[0],[0]
        cor, rects = [],[]
        cm = get_cmap('gist_rainbow')
        for i in range(N):
            cor.append(cm(1.*i/N))  # color will now be an RGBA tuple
        cor = iter(cor)
        dictItems = {'sequentialaleatory':[],'aleatorysequential':[],'sequentialsequential':[],'aleatoryaleatory':[]}
        for elementos in organizados.values():
            for elemento in elementos:
                item = ItemClass(elemento)
                item.elemento = elementos[elemento]
                dictItems[item.tipoDownload+item.tipoConsumo].append(item)
                dictItems[item.tipoDownload+item.tipoConsumo].sort(key = lambda x: int(x.download))
        for elementos in dictItems.values():
            for elemento in elementos:
                nomesProntos.append(str(elemento.tipoDownload) + "Download "+ ", "+ str(elemento.tipoConsumo)+" Consumption")
                nomesProntos = set(nomesProntos)
                nomesProntos = list(nomesProntos)
                media, (erc,erb) = elemento.elemento[-1]['confianca'][0]
                media, erc, erb
                mediasProntas.append(float("{0:.2f}".format(media)))
                ercProntos.append(media-erc)
                erbProntos.append(erb-media)
            legendasX = [0,10,30,50,70,100]
            rects.append(ax.errorbar(legendasX, mediasProntas, yerr=[erbProntos,ercProntos],color=cor.next(),fmt='--o'))
            mediasProntas, ercProntos, erbProntos = [0],[0],[0]       
        # algo mais
        ax.set_ylabel('Tempo de Peers sem Consumo')
        ax.set_title('Tempo Acumulado sem Consumo')
        ax.set_xlabel('Taxa de Download')
        ax.grid(True)
        ax.set_xticks(legendasX)
        ax.set_xticklabels(legendasX)
        ax.set_ylim(bottom=-10,top=7000)
        #ax.set_yscale('log')
        leg = ax.legend(rects,nomesProntos,loc='upper center', bbox_to_anchor=(0.5,-0.1))
        for t in leg.get_texts():
            t.set_fontsize('small')
        plt.savefig(os.path.join(self.caminho,nome), bbox_extra_artists=(leg,), bbox_inches='tight')
        ax.set_yscale('log')
        ax.set_ylabel('Tempo de Peers sem Consumo (log)')
        plt.savefig(os.path.join(self.caminho,'log'+nome), bbox_extra_artists=(leg,), bbox_inches='tight')
        
        
       # cairoplot.horizontal_bar_plot(os.path.join(self.caminho,'2'+nome),dados,self.largura,self.altura, y_labels = self.arquivos,
        #                        border = 20, display_values = True, rounded_corners = True, colors = [(0.5,0.2,0)]);
        
        
    def parcelaDownloadAcumulado(self,nome='parcelaxDownloadacum.svg'):
        '''
        Organiza dados de situacao (pareamento com download ou nao) x numero vezes
        x=[situacao1,situacao2, ...]
        y=[nVezes, nVezes, ...]
        '''
        total = {};
        for arquivo in self.arquivos:
            self.aberto = open(arquivo,"r");
            quantidadeS,quantidadeC =[],[];
            comPar,semPar = 0,0
            for linha in self.aberto:
                linha = linha.rstrip();
                lista = linha.split(',');
                if (lista[0] == 'W'):
                    while '' in lista:
                        lista.remove('');
                    if(lista[1] == '1'):
                        comPar += 1;
                    elif(lista[1] == '0'):
                        semPar +=1;
            quantidadeS.append(semPar);
            quantidadeC.append(comPar);
            self.aberto.close();
            total['SemPar'+arquivo] = quantidadeS
            total['ComPar'+arquivo] = quantidadeC
        data = Series(total)
        background = cairo.LinearGradient(300, 0, 300, 400)
        background.add_color_stop_rgb(0,0.4,0.4,0.4)
        background.add_color_stop_rgb(1.0,0.1,0.1,0.1)

     
        try:
            cairoplot.donut_plot(os.path.join(self.caminho,nome),data,self.largura,self.altura,
                                background = background, gradient = True, shadow = True, inner_radius = 0.3);
        except:
            pass


class ItemClass(object):
    '''
    Classe de item de grafico, aonde sao definidos os itens e seus atributos
    '''

    def __init__(self,nomeArquivo):
        '''
        Declara nome de arquivo para separar
        '''
        self.nomeArquivo = nomeArquivo
        self.separaAtributos()
        
    def separaAtributos(self):
        '''
        Metodo que separa atributos do arquivo
        '''
        self.tipoDownload = self.nomeArquivo[0:self.nomeArquivo.find("_")]
        self.peers = self.nomeArquivo[self.nomeArquivo.find("_Q")+2:self.nomeArquivo.find("_",self.nomeArquivo.find("_Q")+2)]
        self.playlist = self.nomeArquivo[self.nomeArquivo.find("_P")+2:self.nomeArquivo.find("_",self.nomeArquivo.find("_P")+2)]
        self.lista = self.nomeArquivo[self.nomeArquivo.find("_L")+2:self.nomeArquivo.find("_",self.nomeArquivo.find("_L")+2)]
        self.listaTotal = self.nomeArquivo[self.nomeArquivo.find("_S")+2:self.nomeArquivo.find("_",self.nomeArquivo.find("_S")+2)]
        self.consumo = self.nomeArquivo[self.nomeArquivo.find("_R")+2:self.nomeArquivo.find("_",self.nomeArquivo.find("_R")+2)]
        self.timeslot = self.nomeArquivo[self.nomeArquivo.find("_V")+2:self.nomeArquivo.find("_",self.nomeArquivo.find("_V")+2)]
        self.tipoConsumo = self.nomeArquivo[self.nomeArquivo.find("_Y")+2:self.nomeArquivo.find("_",self.nomeArquivo.find("_Y")+2)]        
        self.download = self.nomeArquivo[self.nomeArquivo.find("_X")+2:self.nomeArquivo.find("_",self.nomeArquivo.find("_X")+2)]
        self.delay = self.nomeArquivo[self.nomeArquivo.find("_D")+2:self.nomeArquivo.find(".txt")]

        
        
        