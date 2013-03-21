'''
Created on 11/10/2012

@author: diogo
'''

from controller import MainController, ResultadoController
import sys

if __name__ == '__main__':
    #This controller make the simulation
    if (len(sys.argv[1:]) > 1):
        MainController.MainController(sys.argv[1:]);
    else:
    #this controller make the graphs
        ResultadoController.ResultadoController();