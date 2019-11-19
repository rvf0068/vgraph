﻿# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 20:24:20 2019

@author: Ulises
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QLabel, QToolBar, QAction, QApplication, QLineEdit, QCheckBox ,
                              QWidget, QComboBox, QSplitter, QPushButton, QVBoxLayout, QStatusBar, QFormLayout, QMenuBar)
from PyQt5.QtCore import Qt
from modules.Dialog import Dialog
from modules.cutSignals import CutSignals
from modules.visibility_graph import visibility_graph
from modules.Plot import Plot
from modules.Cliques import Cliques
from modules.Distance_Measures import Distance_measures
from modules.Chordal import Chordal
from modules.Grade_Max import Grade_Max

import sys
import os
from math import modf
from numpy import asarray 
from pandas import read_csv
from networkx import make_max_clique_graph
import pyqtgraph as pg
from time import time


class Principal(QMainWindow):
    
    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)    
    
    def cutSignal_boton(self):
        self.cut_signal = CutSignals()
        self.cut_signal.show()
    def visibility_graph_button(self):
        tiempo_ini = time()
        
        names = str.split(self.rutas[0],"/")
        t=len(names)
        self.nombre = names[t-1]
        names = str.split(self.rutas[0],self.nombre)   
        
        visibility_graphs = []
        if(self.int_max_clique == 1):
            maxclique_graphs = []
        for i in range(len(self.rutas)):
            P = visibility_graph(self.rutas[i],self.list2.currentIndex())
            Plot(P,self.rutas[i],self.list1.currentIndex(),'_visibility_graph.png')
            visibility_graphs.append(P)
            if(self.int_max_clique == 1):
                p = make_max_clique_graph(P)
                Plot(p,self.rutas[i],self.list1.currentIndex(),'_maxclique_graph.png')
                maxclique_graphs.append(p)
       
        if(self.int_1 == 1):
            Cliques(P = visibility_graphs, tipo ='visibility graph', ruta = names[0])
     
        if(self.int_2 == 1):
            Distance_measures(P = visibility_graphs, tipo ='visibility graph', ruta = names[0])
        
        if(self.int_3 == 1):
            Chordal(P = visibility_graphs, tipo ='visibility graph', ruta = names[0])
        
        if(self.int_4 == 1):
            Grade_Max(P = visibility_graphs, tipo ='visibility graph', ruta = names[0])
            
        if(self.int_max_clique == 1):
            if(self.int_1 == 1):
                Cliques(P = maxclique_graphs, tipo ='maxclique graph', ruta = names[0])
         
            if(self.int_2 == 1):
                Distance_measures(P = maxclique_graphs, tipo ='maxclique graph', ruta = names[0])
            
            if(self.int_3 == 1):
                Chordal(P = maxclique_graphs, tipo ='maxclique graph', ruta = names[0])
            
            if(self.int_4 == 1):
                Grade_Max(P = maxclique_graphs, tipo ='maxclique graph', ruta = names[0])
            
            
        self.dialogo_done = Dialog('Done!',self.resource_path('Icons/done.png'))
        self.dialogo_done.show()
        tiempo_fin = time()
        tiempo_total = modf(round(tiempo_fin - tiempo_ini,3)/60)
        self.lbl_time.setText(str(int(tiempo_total[1]))+':'+str(int(tiempo_total[0]*60)))
        
#%%
    def cargarSenial(self):
        self.aux = False
        self.list3.clear()
        self.plot1.clear()
        self.nombreSenial = QFileDialog.getOpenFileNames(None, 'Open file(s)', '/home')
        self.rutas = self.nombreSenial[0]
        self.dialog = Dialog(str(len(self.rutas))+' File(s) loaded','Icons/open.png')
        self.dialog.show()
        self.list3.addItem('')
        for i in range(len(self.rutas)):
            names=str.split(self.rutas[i],"/")
            t=len(names)
            nombre = names[t-1]
            self.list3.addItem(nombre)
            
        if(len(self.rutas)==0):
            self.btn1.setEnabled(False)
            self.lbl_num_files.setStyleSheet("color : red; ")
            self.lbl_num_files.setText("Files loaded: "+str(len(self.rutas)))
        else:
            self.btn1.setEnabled(True)
            self.lbl_num_files.setStyleSheet("color : blue; ")
            self.lbl_num_files.setText("Files loaded: "+str(len(self.rutas)))
        self.aux = True
#%%
    def state_check_1(self):
        if(self.int_1 == 0):
            self.int_1 = 1
        elif(self.int_1 ==1):
            self.int_1 = 0         
    def state_check_2(self):
        if(self.int_2 == 0):
            self.int_2 = 1
        elif(self.int_2 ==1):
            self.int_2 = 0
    def state_check_3(self):
        if(self.int_3 == 0):
            self.int_3 = 1
        elif(self.int_3 ==1):
            self.int_3 = 0
    def state_check_4(self):
        if(self.int_4 == 0):
            self.int_4 = 1
        elif(self.int_4 ==1):
            self.int_4 = 0
    def state_check_max_clique(self, state):
        if(state == Qt.Checked): 
            self.int_max_clique = 1 
        else: 
            self.int_max_clique = 0
    def plots(self):
        if(self.aux == True):
            self.plot1.clear()
            i= self.list3.currentIndex()-1
            if(len(self.rutas)!=0):            
                data = read_csv(self.rutas[i],sep='\t', header=None)
                lineas= data.shape[1]
                if(lineas == 1):
                    self.y = asarray(data[0])
                elif(lineas == 2):
                    self.y = asarray(data[1])
                self.plot1.setLabel('bottom',color='k', **{'font-size':'12pt'})
                self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
                # Y1 axis   
                self.plot1.setLabel('left',color='k', **{'font-size':'12pt'})
                self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
                names=str.split(self.rutas[i],"/")
                t=len(names)
                nombre= names[t-1]
                self.plot1.setTitle(nombre)
                self.plot1.plot(self.y,pen='k')
            
#%% 
    def __init__(self):
        super().__init__()
        pg.setConfigOption('background', 'w')
        self.setWindowTitle('NetWX')
        self.setWindowIcon(QIcon('Icons\icono2.png'))
        self.resize(1225, 700)
        contain=QSplitter(Qt.Horizontal)
        #################################################################
        ##     Definición de variables globales
        #################################################################
        self.rutas = ''
        self.nombreSenial=''
        self.x=[]
        self.y=[]
        self.int_1    = 0
        self.int_2    = 0
        self.int_3    = 0
        self.int_4    = 0
        self.int_max_clique = 0
        self.aux = 0
        #################################################################
        ##     Barra de Herramientas
        #################################################################
        self.barra_estado = QStatusBar()
        self.setStatusBar(self.barra_estado)
        
        barra_herr = QToolBar("Toolbar")
        self.addToolBar(barra_herr)
        
        barra_menu = QMenuBar()
        self.setMenuBar(barra_menu)
        
        menu_archivo = barra_menu.addMenu('&File')
        menu_algorithms = barra_menu.addMenu('&Algorithms')
  
        abrir_action = QAction(QIcon('Icons/open.png'), 'Open File(s)', self)
        abrir_action.setToolTip('Open File(s)')
        abrir_action.setStatusTip('Open File(s)')
        abrir_action.triggered.connect(self.cargarSenial)
        barra_herr.addAction(abrir_action)
        menu_archivo.addAction(abrir_action)
        
        cortar_action = QAction(QIcon('Icons/cut.png'), 'Cut Signal', self)
        cortar_action.setToolTip('Cut Signal')
        cortar_action.setStatusTip('Cut Signal')
        cortar_action.triggered.connect(self.cutSignal_boton)
        barra_herr.addAction(cortar_action)
        menu_archivo.addAction(cortar_action)
        
        self.chordal_action = QAction('Chordal',self ,checkable=True)
        self.chordal_action.triggered.connect(self.state_check_3)
        self.chordal_action.setToolTip('Algorithms for chordal graphs.')
        self.chordal_action.setStatusTip('Algorithms for chordal graphs.')
        menu_algorithms.addAction(self.chordal_action)
        
        self.cliques_action = QAction('Clique',self ,checkable=True)
        self.cliques_action.triggered.connect(self.state_check_1)
        self.cliques_action.setToolTip('Functions for finding and manipulating cliques.')
        self.cliques_action.setStatusTip('Functions for finding and manipulating cliques.')
        menu_algorithms.addAction(self.cliques_action)
        
        self.distance_measures_action = QAction('Distance Measures',self ,checkable=True)
        self.distance_measures_action.triggered.connect(self.state_check_2)
        self.distance_measures_action.setToolTip('Graph diameter, radius, eccentricity and other properties')
        self.distance_measures_action.setStatusTip('Graph diameter, radius, eccentricity and other properties')
        menu_algorithms.addAction(self.distance_measures_action)
        
        self.grade_max_action = QAction('Maximum Dregree',self ,checkable=True)
        self.grade_max_action.triggered.connect(self.state_check_4)
        self.grade_max_action.setToolTip('Graph Maximum dregree')
        self.grade_max_action.setStatusTip('Graph Maximum dregree')
        menu_algorithms.addAction(self.grade_max_action)
        
        #################################################################
        ##     Definición de elementos contenedores
        #################################################################
        graficos = QVBoxLayout()
        botones = QVBoxLayout()
        results  = QFormLayout()
        #################################################################
        ##     Elementos del layout botones
        #################################################################
        lbl2 = QLabel("Sampling frequency:")
        lbl2.setStyleSheet("font-size: 20px")
        
        self.txt1 = QLineEdit("")
        self.txt1.setEnabled(True)
        self.txt1.setStyleSheet("font-size: 20px")
                
        lbl_lista1 = QLabel("Graph layout:")
        lbl_lista1.setStyleSheet("font-size: 20px")
        
        self.list1 = QComboBox()
        self.list1.addItem("None")
        self.list1.addItem("Circular layout")
        self.list1.addItem("Kamada kawai layout")
        
        self.list2 = QComboBox()
        self.list2.addItem("100%")
        self.list2.addItem("10%")
        self.list2.addItem("7%")
        self.list2.addItem("5%")
        self.list2.addItem("1%")
        
        self.list3 = QComboBox()
        self.list3.currentIndexChanged.connect(self.plots)
        
        lbl_check1 = QLabel("Make maxclique graph")
        lbl_check1.setStyleSheet("font-size: 20px")
        
        self.check1 = QCheckBox()
        self.check1.stateChanged.connect(self.state_check_max_clique) 
        
        self.lbl_num_files = QLabel("Files loaded: ")
        self.lbl_num_files.setStyleSheet("font-size: 20px")
        
        lbl_file = QLabel("File: ")
        lbl_file.setStyleSheet("font-size: 20px")
        
        lbl_time = QLabel("Exe. time: ")
        lbl_time.setStyleSheet("font-size: 20px")
        
        self.lbl_time = QLabel()
        self.lbl_time.setStyleSheet("font-size: 20px")
        
        self.btn1 = QPushButton('Visibility graph')
        self.btn1.clicked.connect(self.visibility_graph_button)
        self.btn1.setStyleSheet("font-size: 20px")
        self.btn1.setEnabled(False)
        #################################################################
        ##     Elementos del layout graficos
        #################################################################
        self.plot1=pg.PlotWidget()
        self.plot1.setLabel('bottom',color='k', **{'font-size':'18pt'})
        self.plot1.getAxis('bottom').setPen(pg.mkPen(color='k', width=1))
        self.plot1.setLabel('left',color='k', **{'font-size':'18pt'})
        self.plot1.getAxis('left').setPen(pg.mkPen(color='k', width=1))
        self.plot1.showGrid(1,1,0.2)
        graficos.addWidget(self.plot1)
        #################################################################
        ##     Colocar elementos en layout botones
        #################################################################
        
        results.addRow(self.lbl_num_files)
        results.addRow(lbl_file,self.list3)
        results.addRow(lbl2, self.list2)
        results.addRow(lbl_lista1,self.list1)
        results.addRow(lbl_check1,self.check1)
        results.addRow(lbl_time,self.lbl_time)
        botones.addLayout(results) 
        botones.addWidget(self.btn1)
        #################################################################
        ##     Colocar elementos en la ventana
        #################################################################
        bot = QWidget()
        bot.setLayout(botones)
        gra = QWidget()
        gra.setLayout(graficos)

        contain.addWidget(gra)
        contain.addWidget(bot)

        self.setCentralWidget(contain)
        self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Principal()
    sys.exit(app.exec_())
        
        
        