from tkinter import *
from tkinter import filedialog as dlg
from tkinter import messagebox as msg
from tkinter import ttk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import datetime as dt
import os
import matplotlib.dates as mdates
import pyscreenshot
from tksheet import Sheet
import csv
from math import floor
from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from math import floor
import time
from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
import pickle
from scipy import stats
from haversine import haversine, Unit
import folium
from folium.map import Popup
import webbrowser
import math
import sklearn.utils._typedefs

os.system("cls")

fundo = '#4F4F4F' #? Cor de fundo da tela
fun_b = '#3CB371' #? Cor de fundo dos botoes
fun_ap = '#9C444C'
fun_alt = '#C99418'
fun_meta_le = '#191970'








class Triangulaction:
    def __init__(self):
        self.coordenadas = list()

        local = r'E:\IC\Interface_Grafica\Dados_verificacao\Coordenadas.txt'
        arq = open(local)
        aux = list()
        for i in arq:
            aux.append(i)
        for i in range(len(aux)):
            aux[i] = str(aux[i]).strip('\n')   
            self.coordenadas.append(aux[i])
        
        dt_alv = list()
        dt_cidA = list()
        dt_cidB = list()
        dt_cidC = list()
        for i in range(0,4):
            dt_alv.append(self.coordenadas[i])
        for i in range(4,8):
            dt_cidA.append(self.coordenadas[i])
        for i in range(8,12):
            dt_cidB.append(self.coordenadas[i])
        for i in range(12,16):
            dt_cidC.append(self.coordenadas[i])

        self.tupla_tg = (float(dt_alv[1]), float(dt_alv[2]))
        self.tupla_cA = (float(dt_cidA[1]), float(dt_cidA[2]))
        self.tupla_cB = (float(dt_cidB[1]), float(dt_cidB[2]))
        self.tupla_cC = (float(dt_cidC[1]), float(dt_cidC[2]))
        self.h = [float(self.coordenadas[3]), float(self.coordenadas[7]), float(self.coordenadas[11]), float(self.coordenadas[15])]
        d1 = round(haversine(self.tupla_tg, self.tupla_cA, Unit.KILOMETERS), 4)
        d2 = round(haversine(self.tupla_tg, self.tupla_cB, Unit.KILOMETERS), 4)
        d3 = round(haversine(self.tupla_tg, self.tupla_cC, Unit.KILOMETERS), 4)
        
        self.d = [d1, d2, d3]
    
    def idw(self, foco): # Todo: 1 - Precipitação, 2 - Temperatura Máxima, 3 - Temperatura Miníma
        t = Tratamento()

        distancia = self.d

        self.idw_x = list()
        self.idw_y = list()
        self.idw_alv_y = list()
        if foco == 1:
            ind = 6
            a = 3
            data = t.normalizar_dados(t.retorna_arq('Dados comum'))
        elif foco == 2:
            ind = 7
            a = 4
            data = t.retorna_arq('Dados comum')
        elif foco == 3:
            ind = 8
            a = 5
            data = t.retorna_arq('Dados comum')

        aux = list()
        cont2 = 1


        self.mat_meta_idw = list()
        for i in range(len(data)):
            cont = 0
            soma = 0
            for j in range(ind,15,3):
                soma = soma + (float(data[i][j])/distancia[cont])
                cont += 1
            
            calc_idw = round(soma / (1/distancia[0] + 1/distancia[1] + 1/distancia[2]),4)
            aux = list()
            aux.append(float(data[i][0]))
            aux.append(float(data[i][1]))
            aux.append(float(data[i][2]))
            aux.append(calc_idw)

            self.mat_meta_idw.append(aux) #Matriz para o meta learning
            
            self.idw_x.append(cont2)
            self.idw_y.append(float(calc_idw))
            self.idw_alv_y.append(float(data[i][a]))

            cont2 += 1


        self.idw_erro_abs, self.idw_erro_rel = self.calcula_erros(self.idw_y, self.idw_alv_y)

    def get_idw(self):
        return self.idw_x, self.idw_y, self.idw_alv_y, self.idw_erro_abs, self.idw_erro_rel, self.mat_meta_idw
    
    def aa(self, foco):
        t = Tratamento()


        self.aa_x = list()
        self.aa_y = list()
        self.aa_alv_y = list()

        if foco == 1:
            ind = 6
            a = 3
            data = t.normalizar_dados(t.retorna_arq('Dados comum'))
        elif foco == 2:
            ind = 7
            a = 4
            data = t.retorna_arq('Dados comum')
        elif foco == 3:
            ind = 8
            a = 5
            data = t.retorna_arq('Dados comum')

        cont = 1
        self.mat_meta_aa = list()
        
        for i in range(len(data)): #Resolver depois para mais de 3 estações vizinhas
            soma = 0
            for j in range(ind, 15, 3):
                soma = soma + float(data[i][j])
            
            aa = (1/3) * soma
            aux = list()

            aux.append(float(data[i][0]))
            aux.append(float(data[i][1]))
            aux.append(float(data[i][2]))
            aux.append(aa)
            self.mat_meta_aa.append(aux)

            self.aa_x.append(cont)
            self.aa_y.append(aa)
            self.aa_alv_y.append(float(data[i][a]))

            cont += 1
        
        self.aa_erro_abs, self.aa_erro_rel = self.calcula_erros(self.aa_y, self.aa_alv_y)

    def get_aa(self):
        return self.aa_x, self.aa_y, self.aa_alv_y, self.aa_erro_abs, self.aa_erro_rel, self.mat_meta_aa

    def show_map(self):
        m = folium.Map(location=self.tupla_tg)
        folium.Marker(location=self.tupla_tg, popup=Popup('Target', show=True)).add_to(m)
        folium.Marker(location=self.tupla_cA, popup=Popup('Vizinha A', show=True)).add_to(m)
        folium.Marker(location=self.tupla_cB, popup=Popup('Vizinha B', show=True)).add_to(m)
        folium.Marker(location=self.tupla_cC, popup=Popup('Vizinha C', show=True)).add_to(m)
        m.save('map.html')
    
        webbrowser.open_new_tab('map.html')
    
    def oidw(self, foco):
        qtd_est = 4 #Quantidade de estações utilizadas


        month_a_tar = self.generate_mothly_ave(foco, 'target')
        month_a_vA = self.generate_mothly_ave(foco, 'VizA')
        month_a_vB = self.generate_mothly_ave(foco, 'VizB')
        month_a_vC = self.generate_mothly_ave(foco, 'VizC')

        ma = list()
        for i in range(len(month_a_tar)):
            aux = list()
            aux.append(month_a_tar[i])
            aux.append(month_a_vA[i])
            aux.append(month_a_vB[i])
            aux.append(month_a_vC[i])
            ma.append(aux)
        
        

        if foco == 1:
            ind = 6
        elif foco == 2:
            ind = 7
        elif foco == 3:
            ind = 8

        t = Tratamento()
        data = t.retorna_arq('Dados comum')
        
        final_oidw = list()
        soma_p1 = 0
        soma_p2 = 0
        cont_ma_linha = 0
        cont_ma_coluna = 1
        cont_est = 0
        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    cont_est = 0
                    cont_ma_coluna = 1
                    for j in range(ind, 15, 3):
                        soma_p1 = soma_p1 + ((float(data[i][j]) * ma[cont_ma_linha][0] * math.log(self.h[0])) / (self.d[cont_est] + ma[cont_ma_linha][cont_ma_coluna] * math.log(self.h[cont_ma_coluna])))
                        soma_p2 = (1/self.d[0] + 1/self.d[1] + 1/self.d[2])
                        cont_est += 1
                        cont_ma_coluna += 1
                    
                    final_oidw.append(soma_p1/soma_p2)
                    soma_p1 = 0
                    soma_p2 = 0
                    cont_ma_linha += 1
                else:
                    cont_est = 0
                    cont_ma_coluna = 1
                    for j in range(ind, 15, 3):
                        soma_p1 = soma_p1 + ((float(data[i][j]) * ma[cont_ma_linha][0] * math.log(self.h[0])) / (self.d[cont_est] + ma[cont_ma_linha][cont_ma_coluna] * math.log(self.h[cont_ma_coluna])))
                        soma_p2 = (1/self.d[0] + 1/self.d[1] + 1/self.d[2])
                        cont_est += 1
                        cont_ma_coluna += 1
            except IndexError:
                pass
        
        for i in final_oidw:
            print(i)
                
    def rw(self, foco):
        qtd_est = 3
        month_a_tar = self.generate_mothly_ave(foco, 'target')
        month_a_vA = self.generate_mothly_ave(foco, 'VizA')
        month_a_vB = self.generate_mothly_ave(foco, 'VizB')
        month_a_vC = self.generate_mothly_ave(foco, 'VizC')

        if foco == 1:
            ind = 6
        elif foco == 2:
            ind = 7
        elif foco == 3:
            ind = 8
            
        ma = list()
        self.idw_x = list()
        self.idw_y = list()
        self.idw_alv_y = list()
        for i in range(len(month_a_tar)):
            aux = list()
            aux.append(month_a_tar[i])
            aux.append(month_a_vA[i])
            aux.append(month_a_vB[i])
            aux.append(month_a_vC[i])
            ma.append(aux)   

        t = Tratamento()
        data = t.retorna_arq('Dados comum')
        
        cont_indc = 0

        
        soma = 0
        resultado = list()
        linha_ma = 0
        for i in range(len(data)):
            try:
                if i == self.ind_fim[cont_indc]:
                    soma = ((ma[linha_ma][0]/ma[linha_ma][1])*float(data[i][ind]) + (ma[linha_ma][0]/ma[linha_ma][2])*float(data[i][ind+3]) + (ma[linha_ma][0]/ma[linha_ma][3])*float(data[i][ind+6])) * (1/3)
                    resultado.append(soma)
                    #print(soma * (1/3))
                    soma = 0
                    linha_ma = linha_ma + 1
                    cont_indc += 1
                else:
                    soma = ((ma[linha_ma][0]/ma[linha_ma][1])*float(data[i][ind]) + (ma[linha_ma][0]/ma[linha_ma][2])*float(data[i][ind+3]) + (ma[linha_ma][0]/ma[linha_ma][3])*float(data[i][ind+6])) * (1/3)   
                    resultado.append(soma)
                    soma = 0
            except IndexError:
                soma = ((ma[linha_ma-1][0]/ma[linha_ma-1][1])*float(data[i][ind]) + (ma[linha_ma-1][0]/ma[linha_ma-1][2])*float(data[i][ind+3]) + (ma[linha_ma-1][0]/ma[linha_ma-1][3])*float(data[i][ind+6])) * (1/3)   
                resultado.append(soma)
                soma = 0
 
        self.rw_x = list()
        self.rw_y = list()
        self.rw_alv_y = list()
        self.mat_meta_rw = list()

        
        x = 0
        for i in range(len(data)):
            self.rw_x.append(x)
            self.rw_y.append(resultado[i])
            self.rw_alv_y.append(float(data[i][ind-3]))

            aux = list()
            aux.append(float(data[i][0]))
            aux.append(float(data[i][1]))
            aux.append(float(data[i][2]))
            aux.append(float(resultado[i]))
            self.mat_meta_rw.append(aux)
            

            x += 1
            
        self.rw_erro_abs, self.rw_erro_rel = self.calcula_erros(self.rw_y, self.rw_alv_y)
    
    def get_rw(self):
        return self.rw_x, self.rw_y, self.rw_alv_y, self.rw_erro_abs, self.rw_erro_rel, self.mat_meta_rw

    def generate_mothly_ave(self, foco, cidade):
        t = Tratamento()
        

        mon_ave = list()
        self.ind_fim = list()
        soma = 0
        cont = 2


        if cidade == 'target':
            if foco == 1:
                ind = 3 #precipitação na target
                data = t.normalizar_dados(t.retorna_arq('Dados comum'))
            elif foco == 2:
                ind = 4 #Temperatura maxima na target
                data = t.retorna_arq('Dados comum')
            elif foco == 3:
                ind = 5 #Temperatura minima na target
                data = t.retorna_arq('Dados comum')
        elif cidade == 'VizA':
            if foco == 1:
                ind = 6 
                data = t.normalizar_dados(t.retorna_arq('Dados comum'))
            elif foco == 2:
                ind = 7
                data = t.retorna_arq('Dados comum')
            elif foco == 3:
                ind = 8
                data = t.retorna_arq('Dados comum')
        elif cidade == 'vizB':
            if foco == 1:
                ind = 9
                data = t.normalizar_dados(t.retorna_arq('Dados comum'))
            elif foco == 2:
                ind = 10
                data = t.retorna_arq('Dados comum')
            elif foco == 3:
                ind = 11
                data = t.retorna_arq('Dados comum')
        else:
            if foco == 1:
                ind = 12
                data = t.normalizar_dados(t.retorna_arq('Dados comum'))
            elif foco == 2:
                ind = 13
                data = t.retorna_arq('Dados comum')
            elif foco == 3:
                ind = 14
                data = t.retorna_arq('Dados comum')

        

        #encontar o index da ultima data de cada mes
        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    self.ind_fim.append(i)
            except IndexError:
                pass
       
        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    soma = soma + float(data[i][ind])
                    cont = cont + 1
                    mon_ave.append(soma/cont)
                    soma = 0
                    cont = 1
                else:
                    soma = soma + float(data[i][ind])
                    cont = cont + 1

                
            except IndexError:
                pass
        return mon_ave

    def generate_correlation_coef(self, foco):
        t = Tratamento()
        nor = Treinamento()
        t.retorna_arq
        if foco == 1:
            ind = 3 #precipitação na target
            data = nor.normalizar(t.retorna_arq('Dados comum'))
        elif foco == 2:
            ind = 4 #Temperatura maxima na target
            data = t.retorna_arq('Dados comum')
        elif foco == 3:
            ind = 5 #Temperatura minima na target
            data = t.retorna_arq('Dados comum')


        coef_tg_A = list()
        coef_tg_B = list()
        coef_tg_C = list()
        dias = list()
        cont_d = 0 #Contador de dias
        aux1 = list()
        aux2 = list()
        aux3 = list()
        aux4 = list()

        dias_exc = list() #Guardar indicies onde em um mes tem menos de 2 dias de dados
        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    aux1.append(float(data[i][ind]))
                    aux2.append(float(data[i][ind+3]))
                    aux3.append(float(data[i][ind+6]))
                    aux4.append(float(data[i][ind+9]))
                    cont_d += 1
                    if cont_d >= 2:
                        dias.append(cont_d)
                        cont_d = 0

                        v1 = stats.pearsonr(aux1, aux2)
                        v2 = stats.pearsonr(aux1, aux3)
                        v3 = stats.pearsonr(aux1, aux4)
                        coef_tg_A.append(v1[0])
                        coef_tg_B.append(v2[0])
                        coef_tg_C.append(v3[0])

                        aux1 = list()
                        aux2 = list()
                        aux3 = list()
                        aux4 = list()
                    else:
                        dias_exc.append(i)
                else:
                    aux1.append(float(data[i][ind]))
                    aux2.append(float(data[i][ind+3]))
                    aux3.append(float(data[i][ind+6]))
                    aux4.append(float(data[i][ind+9]))
                    cont_d += 1
            except IndexError:
                aux1.append(float(data[i-1][ind]))
                aux2.append(float(data[i-1][ind+3]))
                aux3.append(float(data[i-1][ind+6]))
                aux4.append(float(data[i-1][ind+9]))
                cont_d += 1

        return  dias, coef_tg_A, coef_tg_B, coef_tg_C


    def onr(self, foco):
        qtd_est = 3

        
        d, cA, cB, cC = self.generate_correlation_coef(foco)

        if foco == 1:
            ind = 6
        elif foco == 2:
            ind = 7
        elif foco == 3:
            ind = 8

        t = Tratamento()
        data = t.retorna_arq('Dados comum')
        
        self.onr_y = list()
        cont_cor = 0
        resultado = list()

        for i in range(len(data)):
            try:
                if data[i][1] != data[i+1][1]:
                    soma1 = math.pow(cA[cont_cor], 2*((d[cont_cor]-2)/(1-cA[cont_cor]))) * float(data[i][ind])
                    soma1 = soma1 + math.pow(cB[cont_cor], 2*((d[cont_cor]-2)/(1-cB[cont_cor]))) * float(data[i][ind+3])
                    soma1 = soma1 + math.pow(cC[cont_cor], 2*((d[cont_cor]-2)/(1-cC[cont_cor]))) * float(data[i][ind+6])

                    soma2 = math.pow(cA[cont_cor], 2*((d[cont_cor]-2)/(1-cA[cont_cor]))) + math.pow(cB[cont_cor], 2*((d[cont_cor]-2)/(1-cB[cont_cor]))) +math.pow(cC[cont_cor], 2*((d[cont_cor]-2)/(1-cC[cont_cor])))
                    resultado.append(soma1/soma2)
                    cont_cor += 1
                    soma1 = 0
                    soma2 = 0
                    
                else:
                
                    soma1 = math.pow(cA[cont_cor], 2*((d[cont_cor]-2)/(1-cA[cont_cor]))) * float(data[i][ind])
                    soma1 = soma1 + math.pow(cB[cont_cor], 2*((d[cont_cor]-2)/(1-cB[cont_cor]))) * float(data[i][ind+3])
                    soma1 = soma1 + math.pow(cC[cont_cor], 2*((d[cont_cor]-2)/(1-cC[cont_cor]))) * float(data[i][ind+6])

                    soma2 = math.pow(cA[cont_cor], 2*((d[cont_cor]-2)/(1-cA[cont_cor]))) + math.pow(cB[cont_cor], 2*((d[cont_cor]-2)/(1-cB[cont_cor]))) +math.pow(cC[cont_cor], 2*((d[cont_cor]-2)/(1-cC[cont_cor])))
                    resultado.append(soma1/soma2)
                    
                    soma1 = 0
                    soma2 = 0

            except IndexError:
                soma1 = math.pow(cA[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cA[cont_cor-1]))) * float(data[i][ind])
                soma1 = soma1 + math.pow(cB[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cB[cont_cor-1]))) * float(data[i][ind+3])
                soma1 = soma1 + math.pow(cC[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cC[cont_cor-1]))) * float(data[i][ind+6])

                soma2 = math.pow(cA[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cA[cont_cor-1]))) + math.pow(cB[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cB[cont_cor-1]))) +math.pow(cC[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cC[cont_cor-1])))
                resultado.append(soma1/soma2)
                soma1 = 0
                soma2 = 0

            except ValueError:
                soma1 = math.pow(cA[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cA[cont_cor-1]))) * float(data[i][ind])
                soma1 = soma1 + math.pow(cB[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cB[cont_cor-1]))) * float(data[i][ind+3])
                soma1 = soma1 + math.pow(cC[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cC[cont_cor-1]))) * float(data[i][ind+6])

                soma2 = math.pow(cA[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cA[cont_cor-1]))) + math.pow(cB[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cB[cont_cor-1]))) +math.pow(cC[cont_cor-1], 2*((d[cont_cor-1]-2)/(1-cC[cont_cor-1])))
                resultado.append(soma1/soma2)
                soma1 = 0
                soma2 = 0
                
        self.onr_x = list()
        self.onr_alv_y = list()
        self.mat_meta_onr = list()
        
        x = 0
        for i in range(len(data)):
            self.onr_x.append(i)
            self.onr_alv_y.append(float(data[i][ind-3]))
            self.onr_y.append(resultado[i])

            aux = list()
            aux.append(float(data[i][0]))
            aux.append(float(data[i][1]))
            aux.append(float(data[i][2]))
            aux.append(float(self.onr_y[i]))
            self.mat_meta_onr.append(aux)

            x = i
        self.onr_erro_abs, self.onr_erro_rel = self.calcula_erros(self.onr_y, self.onr_alv_y)
        
    def get_onr(self):
        return self.onr_x, self.onr_y, self.onr_alv_y, self.onr_erro_abs, self.onr_erro_rel, self.mat_meta_onr
 
    def calcula_erros(self, real, aprox):
        t = Treinamento()
        
        exato = t.normalizar(real)
        aproximado = t.normalizar(aprox)
             
        soma_ea = 0
        soma_er = 0
        for i in range(len(exato)):
            ea = abs(exato[i] - aproximado[i])
            er = ea / exato[i]

            soma_ea = soma_ea + ea
            soma_er = soma_er + er
        
        erro_abs = soma_ea / len(exato)
        erro_rela = soma_er / len(exato)

        return erro_abs, erro_rela

class Treinamento:
    def ArvoreDecisao(self, cidade, indic, divisao, cri, spli, max_d, min_s, max_f,  max_l, n_testes, min_sam_spl, min_wei, minim, ccp, save):
        tempo_inicial = time.time()
        if indic == 3:
            indicador = 'Precipitação'
        elif indic == 4:
            indicador = 'Temperatura máxima'
        else:
            indicador = 'Temperatura miníma'


        param = [cri, spli, max_d, min_s, max_f,  max_l, min_sam_spl, min_wei, minim, ccp]
        nome_p = ['criterion: ', 'splitter: ', 'max_depth: ', 'min_samples_leaf: ', 'max_features: ', 'max_leaf_nodes: ', 'min_samples_split: ', 'min_weight_fraction_leaf: ', 'min_impurity_decrease: ', 'ccp_alpha: ']
        arq = open(r'E:\IC\Interface_Grafica\Dados_verificacao\ArvoreD_comp.txt', 'a')

        arq.write("-------------------------------------------------------------\n")
        arq.write("---- Erros Obtidos a partir da ML Arvore de Decisão ----\n\n")
        hora = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        arq.write("Horário dos teste: " + hora + "\n")
        arq.write("Porção para treinamento: " + str(divisao) + '%\nIndicador climático: ' + indicador + '\n\n')
        arq.write("Parâmetros usados:\n")
        for i in range(len(param)):
            arq.write("  -> " + nome_p[i] + str(param[i]) + "\n")
        
        arq.write("\n\n---- Resultados Obtidos ----\n\n")


        m_trei, r_trei, m_vali, r_vali = self.prepara_matriz(cidade, divisao, indic, 0)
        
        soma_er_nteste = 0 #* Soma dos erros relativos dos n testes
        soma_ea_nteste = 0 #* Soma dos erros absolutos dos n testes
        
        
       
        eixo_y_exato = list()
        eixo_y_predict = list()
        eixo_x = list()
        cont = 1
        cont2 = 1
        for j in range(n_testes):
            aprendiz = tree.DecisionTreeRegressor(criterion=cri, splitter=spli, max_depth=max_d, min_samples_leaf=min_s, max_features=max_f, max_leaf_nodes=max_l, min_samples_split=min_sam_spl, min_weight_fraction_leaf=min_wei, min_impurity_decrease=minim, ccp_alpha=ccp)
            aprendiz = aprendiz.fit(m_trei, r_trei)

            soma_ea = 0 #* Soma dos erros absolutos
            soma_er = 0 #* Soma dos erros relativos

            for i in range(len(m_vali)):
                valor_exato = r_vali[i]
                valor_aprox = aprendiz.predict([m_vali[i]])[0]
                if j != (n_testes):
                    eixo_y_exato.append(valor_exato)
                    eixo_y_predict.append(valor_aprox)
                    eixo_x.append(cont)
                    cont += 1
                
                Erro_absoluto = valor_exato - valor_aprox

                if Erro_absoluto < 0:
                    Erro_absoluto = Erro_absoluto * (-1)
                
                Erro_relativo = (Erro_absoluto/valor_exato)

                soma_ea = soma_ea + Erro_absoluto
                soma_er = soma_er + Erro_relativo
            
            soma_er_nteste = soma_er_nteste + soma_er/len(m_vali)
            soma_ea_nteste = soma_ea_nteste + soma_ea/len(m_vali)
            
            arq.write("Teste n° " + str(cont2) + " -> Erro Relativo: " + str(round((soma_er/len(m_vali)), 6)) + " || Erro Absoluto: " + str(round((soma_ea/len(m_vali)), 6)) + "\n")
            cont2 += 1

        pontuacao = round((((soma_er_nteste/n_testes)*100) - 100)* (-1),2)
        erro = (eixo_y_exato[i] - eixo_y_predict[i])
        if erro < 0:
            erro = erro * (-1)
                

        maior_ea = erro
        exat_maior = eixo_y_exato[0]
        pre_maior = eixo_y_predict[0]

        menor_ea = erro
        exat_menor = eixo_y_exato[0]
        pre_menor = eixo_y_predict[0]

        for i in range(1, len(eixo_x)):
            erro = (eixo_y_exato[i] - eixo_y_predict[i])
            if erro < 0:
                erro = erro * (-1)

            if erro > maior_ea:
                maior_ea = erro
                exat_maior = eixo_y_exato[i]
                pre_maior = eixo_y_predict[i]
            
            if (erro) < menor_ea and (erro) > 0:
                menor_ea = erro
                exat_menor = eixo_y_exato[i]
                pre_menor = eixo_y_predict[i]
        
        media_ea = soma_ea_nteste/n_testes
        media_er = soma_er_nteste/n_testes

        if save == 1:
            pickle.dump(aprendiz, open(r'E:\IC\Interface_Grafica\Dados_verificacao\modelo_ad.sav', 'wb'))


        arq.write("\nmedia do Erro absoluto: " + str(media_ea) + " || média do Erro relativo: " + str(media_er) + "\n")
        tempo_final = time.time()
        tempo_total = str(tempo_final - tempo_inicial)
        arq.write("\nTempo de execução: " + tempo_total + " s\n")
        arq.write("-------------------------------------------------------------\n\n")
        arq.close()
        return pontuacao, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x
          
    def RedeNeural(self, cidade, indic, divisao, n_teste, activ, solv, alp, batc, learnrat, learnratini, powrt, maxiter,shuf, tol_v, verb, warmst, moment, nestr, early, valid, b1, b2, niter, maxf, save):
        tempo_inicial = time.time()
        if indic == 3:
            indicador = 'Precipitação'
        elif indic == 4:
            indicador = 'Temperatura máxima'
        else:
            indicador = 'Temperatura miníma'

        param = [activ, solv, alp, batc, learnrat, learnratini, powrt, maxiter,shuf, tol_v, verb, warmst, moment, nestr, early, valid, b1, b2, niter, maxf]
        nome_p = ['activation: ', 'solver: ', 'alpha: ', 'batch_size: ', 'learning_rate: ', 'learning_rate_init: ', 'power_t: ', 'max_iter: ', 'shuffle: ', 'tol: ', 'verbose: ', 'warm_start: ', 'momentum: ', 'nesterovs_momentum: ', 'early_stopping: ', 'validation_fraction: ', 'beta_1: ', 'beta_1: ', 'n_iter_no_change: ', 'max_fun: ']
        arq = open(r'E:\IC\Interface_Grafica\Dados_verificacao\RedeNeural_comp.txt', 'a')
        arq.write("-------------------------------------------------------------\n")
        arq.write("---- Erros Obtidos a partir da ML Redes Neurais ----\n\n")
        hora = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        arq.write("Horário dos teste: " + hora + "\n")
        arq.write("Porção para treinamento: " + str(divisao) + '%\nIndicador climático: ' + indicador + '\n\n')
        arq.write("Parâmetros usados:\n")
        for i in range(len(param)):
            arq.write("  -> " + nome_p[i] + str(param[i]) + "\n")
        
        arq.write("\n\n---- Resultados Obtidos ----\n\n")       
        
        
        m_trei, r_trei, m_vali, r_vali = self.prepara_matriz(cidade, divisao, indic, 0)
        soma_er_nteste = 0
        soma_ea_nteste = 0

        eixo_y_exato = list()
        eixo_y_predict = list()
        eixo_x = list()
        cont = 1
        cont2 = 1

        for j in range(n_teste):
            aprendiz = MLPRegressor(activation=activ, solver=solv, alpha=alp, batch_size=batc, learning_rate=learnrat, learning_rate_init=learnratini, power_t=powrt, max_iter=maxiter, shuffle=shuf, tol=tol_v, verbose=verb, warm_start=warmst, momentum=moment, nesterovs_momentum=nestr, early_stopping=early, validation_fraction=valid, beta_1=b1, beta_2=b2,n_iter_no_change=niter,max_fun=maxf)
            aprendiz = aprendiz.fit(m_trei, r_trei)

            soma_ea = 0
            soma_er = 0

            for i in range(len(m_vali)):
                valor_exato = r_vali[i]
                valor_aprox = aprendiz.predict([m_vali[i]])[0]

                if j != (n_teste): #Quando chegar no final, adicionar todos os valores finais em suas respctivas variaveis
                    eixo_y_exato.append(valor_exato)
                    eixo_y_predict.append(valor_aprox)
                    eixo_x.append(cont)
                    cont += 1
            
                Erro_absoluto = abs(valor_exato - valor_aprox)
                Erro_relativo = Erro_absoluto/valor_exato

                soma_ea = soma_ea + Erro_absoluto
                soma_er = soma_er + Erro_relativo

            soma_ea_nteste = soma_ea_nteste + soma_ea/len(m_vali)
            soma_er_nteste = soma_er_nteste + soma_er/len(m_vali)
            
            arq.write("Teste n° " + str(cont2) + " -> Erro Relativo: " + str(round((soma_er/len(m_vali)), 6)) + " || Erro Absoluto: " + str(round((soma_ea/len(m_vali)), 6)) + "\n")
            cont2 += 1
        pontuacao = round((((soma_er_nteste/n_teste)*100) - 100)* (-1),2)
        erro = abs(eixo_y_exato[i] - eixo_y_predict[i])
        

        maior_ea = erro
        exat_maior = eixo_y_exato[0]
        pre_maior = eixo_y_predict[0]

        menor_ea = erro
        exat_menor = eixo_y_exato[0]
        pre_menor = eixo_y_predict[0]

        for i in range(1, len(eixo_x)):
            erro = (eixo_y_exato[i] - eixo_y_predict[i])
            if erro < 0:
                erro = erro * (-1)

            if erro > maior_ea:
                maior_ea = erro
                exat_maior = eixo_y_exato[i]
                pre_maior = eixo_y_predict[i]
                
            if (erro) < menor_ea and (erro) > 0:
                menor_ea = erro
                exat_menor = eixo_y_exato[i]
                pre_menor = eixo_y_predict[i]
            
        media_ea = soma_ea_nteste/n_teste
        media_er = soma_er_nteste/n_teste

        if save == 1:
            pickle.dump(aprendiz, open(r'E:\IC\Interface_Grafica\Dados_verificacao\modelo_rn.sav', 'wb'))

        arq.write("\nmedia do Erro absoluto: " + str(media_ea) + " || média do Erro relativo: " + str(media_er) + "\n")
        tempo_final = time.time()
        tempo_total = str(tempo_final - tempo_inicial)
        arq.write("\nTempo de execução: " + tempo_total + " s\n")
        arq.write("-------------------------------------------------------------\n\n")
        arq.close()
        return pontuacao, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x
            
    def KNeighbors(self, cidade, indic, divisao, n_teste, n_nei, algor, leaf_s, p_val, n_jo, save):
            m_trei, r_trei, m_vali, r_vali = self.prepara_matriz(cidade, divisao, indic, 0)
            soma_er_nteste = 0
            soma_ea_nteste = 0

            eixo_y_exato = list()
            eixo_y_predict = list()
            eixo_x = list()
            cont = 1
            cont2 = 1

            if indic == 3:
                indicador = 'Precipitação'
            elif indic == 4:
                indicador = 'Temperatura máxima'
            else:
                indicador = 'Temperatura miníma'

            param = [n_nei, algor, leaf_s, p_val, n_jo]
            nome_p = ['n_neighbors: ', 'algorithm: ', 'leaf_size: ', 'p: ', 'n_jobs: ']
            arq = open(r'E:\IC\Interface_Grafica\Dados_verificacao\KNeighbors_comp.txt', 'a')

            arq.write("-------------------------------------------------------------\n")
            arq.write("---- Erros Obtidos a partir da ML KNeighbors ----\n\n")
            hora = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            arq.write("Horário dos teste: " + hora + "\n")
            arq.write("Porção para treinamento: " + str(divisao) + '%\nIndicador climático: ' + indicador + '\n\n')
            arq.write("Parâmetros usados:\n")
            for i in range(len(param)):
                arq.write("  -> " + nome_p[i] + str(param[i]) + "\n")
            
            arq.write("\n\n---- Resultados Obtidos ----\n\n")

            for j in range(n_teste):
                aprendiz = KNeighborsRegressor(n_neighbors=n_nei, algorithm=algor, leaf_size=leaf_s, p=p_val, n_jobs=n_jo)
                aprendiz = aprendiz.fit(m_trei, r_trei)

                soma_ea = 0
                soma_er = 0

                for i in range(len(m_vali)):
                    valor_exato = r_vali[i]
                    valor_aprox = aprendiz.predict([m_vali[i]])[0]

                    if j != (n_teste): #Quando chegar no final, adicionar todos os valores finais em suas respctivas variaveis
                        eixo_y_exato.append(valor_exato)
                        eixo_y_predict.append(valor_aprox)
                        eixo_x.append(cont)
                        cont += 1
                
                    Erro_absoluto = abs(valor_exato - valor_aprox)
                    Erro_relativo = Erro_absoluto/valor_exato

                    soma_ea = soma_ea + Erro_absoluto
                    soma_er = soma_er + Erro_relativo

                soma_ea_nteste = soma_ea_nteste + soma_ea/len(m_vali)
                soma_er_nteste = soma_er_nteste + soma_er/len(m_vali)

                arq.write("Teste n° " + str(cont2) + " -> Erro Relativo: " + str(round((soma_er/len(m_vali)), 6)) + " || Erro Absoluto: " + str(round((soma_ea/len(m_vali)), 6)) + "\n")
                cont2 += 1

            pontuacao = round((((soma_er_nteste/n_teste)*100) - 100)* (-1),2)
            erro = abs(eixo_y_exato[i] - eixo_y_predict[i])
            

            maior_ea = erro
            exat_maior = eixo_y_exato[0]
            pre_maior = eixo_y_predict[0]

            menor_ea = erro
            exat_menor = eixo_y_exato[0]
            pre_menor = eixo_y_predict[0]

            for i in range(1, len(eixo_x)):
                erro = (eixo_y_exato[i] - eixo_y_predict[i])
                if erro < 0:
                    erro = erro * (-1)

                if erro > maior_ea:
                    maior_ea = erro
                    exat_maior = eixo_y_exato[i]
                    pre_maior = eixo_y_predict[i]
                    
                if (erro) < menor_ea and (erro) > 0:
                    menor_ea = erro
                    exat_menor = eixo_y_exato[i]
                    pre_menor = eixo_y_predict[i]
                
            media_ea = soma_ea_nteste/n_teste
            media_er = soma_er_nteste/n_teste

            if save == 1:
                pickle.dump(aprendiz, open(r'E:\IC\Interface_Grafica\Dados_verificacao\modelo_kn.sav', 'wb'))

            arq.write("media do Erro absoluto: " + str(media_ea) + " || média do Erro relativo: " + str(media_er) + "\n")
            arq.write("-------------------------------------------------------------\n\n")
            arq.close()
            return pontuacao, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x

    def SVR(self, cidade, indic, divisao, n_teste, ker, degr, gam, coe, t, c, eps, shr, cache, verb, maxi, save):
                m_trei, r_trei, m_vali, r_vali = self.prepara_matriz(cidade, divisao, indic, 0)
                soma_er_nteste = 0
                soma_ea_nteste = 0

                eixo_y_exato = list()
                eixo_y_predict = list()
                eixo_x = list()
                cont = 1
                cont2 = 1

                if indic == 3:
                    indicador = 'Precipitação'
                elif indic == 4:
                    indicador = 'Temperatura máxima'
                else:
                    indicador = 'Temperatura miníma'
                param = [ker, degr, gam, coe, t, c, eps, shr, cache, verb, maxi]
                nome_p = ['kernel: ', 'degree: ', 'gamma: ', 'coef0: ', 'tol: ', 'C: ', 'epsilon: ', 'shrinking: ', 'cache_size: ', 'verbose: ', 'max_iter: ']
                arq = open(r'E:\IC\Interface_Grafica\Dados_verificacao\SupportVectorMachine_comp.txt', 'a')

                arq.write("-------------------------------------------------------------\n")
                arq.write("---- Erros Obtidos a partir da ML Support Vector Machine ----\n\n")
                hora = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                arq.write("Horário dos teste: " + hora + "\n")
                arq.write("Porção para treinamento: " + str(divisao) + '%\nIndicador climático: ' + indicador + '\n\n')
                arq.write("Parâmetros usados:\n")
                for i in range(len(param)):
                    arq.write("  -> " + nome_p[i] + str(param[i]) + "\n")
                
                arq.write("\n\n---- Resultados Obtidos ----\n\n")


                for j in range(n_teste):
                    aprendiz = SVR(kernel=ker, degree=degr, gamma=gam, coef0=coe, tol=t, C=c, epsilon=eps, shrinking=shr, cache_size=cache, verbose=verb, max_iter=maxi)
                    aprendiz = aprendiz.fit(m_trei, r_trei)

                    soma_ea = 0
                    soma_er = 0

                    for i in range(len(m_vali)):
                        valor_exato = r_vali[i]
                        valor_aprox = aprendiz.predict([m_vali[i]])[0]

                        if j != (n_teste): #Quando chegar no final, adicionar todos os valores finais em suas respctivas variaveis
                            eixo_y_exato.append(valor_exato)
                            eixo_y_predict.append(valor_aprox)
                            eixo_x.append(cont)
                            cont += 1
                    
                        Erro_absoluto = abs(valor_exato - valor_aprox)
                        Erro_relativo = Erro_absoluto/valor_exato

                        soma_ea = soma_ea + Erro_absoluto
                        soma_er = soma_er + Erro_relativo

                    soma_ea_nteste = soma_ea_nteste + soma_ea/len(m_vali)
                    soma_er_nteste = soma_er_nteste + soma_er/len(m_vali)

                    arq.write("Teste n° " + str(cont2) + " -> Erro Relativo: " + str(round((soma_er/len(m_vali)), 6)) + " || Erro Absoluto: " + str(round((soma_ea/len(m_vali)), 6)) + "\n")
                    cont2 += 1

                pontuacao = round((((soma_er_nteste/n_teste)*100) - 100)* (-1),2)
                erro = abs(eixo_y_exato[i] - eixo_y_predict[i])
                

                maior_ea = erro
                exat_maior = eixo_y_exato[0]
                pre_maior = eixo_y_predict[0]

                menor_ea = erro
                exat_menor = eixo_y_exato[0]
                pre_menor = eixo_y_predict[0]

                for i in range(1, len(eixo_x)):
                    erro = (eixo_y_exato[i] - eixo_y_predict[i])
                    if erro < 0:
                        erro = erro * (-1)

                    if erro > maior_ea:
                        maior_ea = erro
                        exat_maior = eixo_y_exato[i]
                        pre_maior = eixo_y_predict[i]
                        
                    if (erro) < menor_ea and (erro) > 0:
                        menor_ea = erro
                        exat_menor = eixo_y_exato[i]
                        pre_menor = eixo_y_predict[i]
                    
                media_ea = soma_ea_nteste/n_teste
                media_er = soma_er_nteste/n_teste

                if save == 1:
                    pickle.dump(aprendiz, open(r'E:\IC\Interface_Grafica\Dados_verificacao\modelo_svr.sav', 'wb'))
                arq.write("media do Erro absoluto: " + str(media_ea) + " || média do Erro relativo: " + str(media_er) + "\n")
                arq.write("-------------------------------------------------------------\n\n")
                arq.close()
                return pontuacao, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x

    def prepara_matriz(self, local, divi, indicador, qtd_in):
        norm = Tratamento()

        matriz = list()
        aux1 = list()
        resultado = list()
        arq = open(local)
        for i in arq:
            buff = list()
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            i = i.split(',') 
            buff.append(int(i[2])) #dia
            buff.append(int(i[1])) #mes
            buff.append(int(i[0])) #ano
            buff.append(float(i[indicador])) #Indicador selecionado pelo usuário
            aux1.append(buff)
        mat_n = norm.normalizar_dados(aux1)


        buff.clear()
        
        for i in range(len(mat_n)):
            buff = list()
            try:
                for j in range(5):
                    buff.append(mat_n[i+j][0])
                    buff.append(mat_n[i+j][1])
                    buff.append(mat_n[i+j][2])
                    buff.append(mat_n[i+j][3])
                if len(buff) == 20:
                    matriz.append(buff[:19])
                    resultado.append(buff[19])
            except IndexError:
                pass
        arq.close()
        tam = floor(len(matriz)*(divi/100))
        matriz_treinamento = list()
        resultado_treinamento = list()
        matriz_validacao = list()
        resultado_validacao = list()

        for i in range(len(matriz)):
            if i <= tam:
                matriz_treinamento.append(matriz[i])
                resultado_treinamento.append(resultado[i])
            else:
                matriz_validacao.append(matriz[i])
                resultado_validacao.append(resultado[i])
        mat_trein_n = list()
        res_tre_n = list()
        mat_val_n = list()
        res_val_n = list()
        '''if indicador == 3:
            mat_trein_n = norm.normalizar_dados(matriz_treinamento)
            res_tre_n = norm.normalizar_dados(resultado_treinamento)
            mat_val_n = norm.normalizar_dados(matriz_validacao)
            res_val_n = norm.normalizar_dados(resultado_validacao)
            return mat_trein_n, res_tre_n, mat_val_n, res_val_n
        else:'''
        return matriz_treinamento, resultado_treinamento, matriz_validacao, resultado_validacao 



    def prepara_matriz2(self, local, divisao, indicadores, foco, normalizar): #Indicadores estão em forma de lista (no max 2 de 3) [3(chuva) e/ou 4(tmax) e/ou 5(tmin)]  || O foco vai ser qual indicador que o usuario quer que as máquinas façam o predict

        matriz = list()
        resultado = list()
        arq = open(local)

        for i in arq:
            buff = list()
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            i = i.split(',') 
            buff.append(int(i[2])) #dia
            buff.append(int(i[1])) #mes
            buff.append(int(i[0])) #ano
            if indicadores != []:
                for j in indicadores:
                    buff.append(float(i[j]))
            resultado.append(float(i[foco]))
            matriz.append(buff) 
        arq.close()

        tam = floor(len(matriz)*(divisao/100))
        matriz_treinamento = list()
        resultado_treinamento = list()
        matriz_validacao = list()
        resultado_validacao = list()

        if normalizar == 1:
            resultado_n = self.normalizar(resultado)
            matriz_n = self.normalizar(matriz)

            for i in range(len(matriz)):
                if i <= tam:
                    matriz_treinamento.append(matriz_n[i])
                    resultado_treinamento.append(resultado_n[i])
                else:
                    matriz_validacao.append(matriz_n[i])
                    resultado_validacao.append(resultado_n[i])
        else:
            for i in range(len(matriz)):
                if i <= tam:
                    matriz_treinamento.append(matriz[i])
                    resultado_treinamento.append(resultado[i])
                else:
                    matriz_validacao.append(matriz_n[i])
                    resultado_validacao.append(resultado[i])

        return matriz_treinamento, resultado_treinamento, matriz_validacao, resultado_validacao 

            

    def normalizar(self, data):

        try: #Se for uma matriz (mais de uma coluna)
            max_min = list()  #Lista de max e min de cada coluna
            aux = list()
            t = len(data[0])  #Obter a quantidade de colunas da "matriz"

            for i in range(t): #Um laço começa pelas colunas e vai percorrendo as linhas
                aux.clear()
                for j in range(len(data)):
                    aux.append(float(data[j][i]))
                max_min.append(max(aux))  #Coloca o max e depois o min de cada columa
                max_min.append(min(aux))

            dadosn = list()

            for i in range(len(data)):
                cont = 0
                buff = list()
                for j in range(t):
                    maior = max_min[cont]
                    menor = max_min[cont + 1]
                    dado = ((float(data[i][j]) - float(menor)) / (float(maior) - float(menor))) * 0.6 + 0.2
                    buff.append(dado)
                    cont = cont + 2
                dadosn.append(buff)

            
                     
        except TypeError: #Se for so um vetor (uma so coluna/linha)
            dadosn = list()
            maior = max(data)
            menor = min(data)
            for i in range(len(data)):
                dado = ((float(data[i]) - float(menor)) / (float(maior) - float(menor))) * 0.6 + 0.2
                dadosn.append(dado)

        return dadosn

class MetaL:
    def prepara_input(self, indicador, janela):
        if indicador == 1:
            foco = 3
        elif indicador == 2:
            foco = 4
        else: 
            foco = 5

        trat = Tratamento()
        dt = trat.retorna_arq('Dados comum')

        mat = list()
        for i in range(len(dt)): #Vai fazer uma matriz com ano mes dia foco
            aux = list()
            aux.append(float(dt[i][0]))
            aux.append(float(dt[i][1]))
            aux.append(float(dt[i][2]))
            aux.append(float(dt[i][foco]))
            mat.append(aux)

        norma = Treinamento()
        mat_n = norma.normalizar(mat) #Vai normalizar os dados de cada coluna e de cada linha
        if janela == 'Sim':
            matriz_t, matriz_r = self.janela_deslizante(mat_n) #Vai fazer as matrizes para o input no formato de janela deslizante
        else:
            matriz_t, matriz_r = self.input_comum(mat_n)
        m1_40_t = list()
        m1_40_r = list()
        m2_40_t = list() #Para o aprediz lv0 fazer os predicts, que serão um dos inputs do meta
        m2_40_r = list()
        m3_20_t = list()
        m3_20_r = list()

        tamanho = len(matriz_t)
        t1 = floor(tamanho * 0.4)
        t2 = t1 * 2

        for i in range(tamanho): #Vai separa as porções de dados
            if i <= t1:
                m1_40_t.append(matriz_t[i])
                m1_40_r.append(matriz_r[i])
            elif i > t1 and i <=t2:
                m2_40_t.append(matriz_t[i])
                m2_40_r.append(matriz_r[i])
            else:
                m3_20_t.append(matriz_t[i])
                m3_20_r.append(matriz_r[i])
        
        return m1_40_t, m1_40_r, m2_40_t, m2_40_r, m3_20_t, m3_20_r
         
    def janela_deslizante(self, data):
        matriz = list()
        resultado = list()
        buff = list()
        for i in range(len(data)):
            buff = list()
            try:
                for j in range(5):
                    buff.append(data[i+j][0])
                    buff.append(data[i+j][1])
                    buff.append(data[i+j][2])
                    buff.append(data[i+j][3])
                if len(buff) == 20:
                    matriz.append(buff[:19])
                    resultado.append(buff[19])
            except IndexError:
                pass
        return matriz, resultado

    def input_comum(self, data):
        matriz = list()
        resultado = list()
        
        for i in range(len(data)):
            buff = list()
            buff.append(data[i][0])
            buff.append(data[i][1])
            buff.append(data[i][2])
            matriz.append(buff)

            resultado.append(data[i][3])

        return matriz, resultado
    
    def base_learn(self, mach, pre, n_test, mat_in_tr, mat_res_tr, mat_in_valid, mat_res_valid, mat_in_p2, mat_res_p2, janela):
        if pre == 0:
            if mach == 'Decision Trees':
                aprendiz_lv0 = tree.DecisionTreeRegressor()
            elif mach == 'Neural network':
                aprendiz_lv0 = MLPRegressor()
            elif mach == 'Nearest Neighbors':
                aprendiz_lv0 = KNeighborsRegressor()
            elif mach == 'Support Vector':
                aprendiz_lv0 = SVR()

        soma_er_nteste = 0
        soma_ea_nteste = 0
        
        soma_r2 = 0
        for i in range(n_test):
            aprendiz_lv0 = aprendiz_lv0.fit(mat_in_tr, mat_res_tr)
            soma_ea = 0
            soma_er = 0
            soma_r2 = soma_r2 + aprendiz_lv0.score(mat_in_valid, mat_res_valid)
            for j in range(len(mat_in_valid)):
                valor_ex = float(mat_res_valid[j])
                valor_aprox = float(aprendiz_lv0.predict([(mat_in_valid[j])])[0])
                Erro_abs = abs(valor_ex - valor_aprox)
                Erro_rel = Erro_abs / valor_ex

                soma_ea = soma_ea + Erro_abs
                soma_er = soma_er + Erro_rel
            
            soma_ea_nteste = soma_ea_nteste + soma_ea/len(mat_in_valid)
            soma_er_nteste = soma_er_nteste + soma_er/len(mat_in_valid)

        media_ea = soma_ea_nteste / n_test
        media_er = soma_er_nteste / n_test
        porc_erro = media_ea * 100
        r2 = soma_r2 / n_test

        #Preparando os dados do aprendiz lv0 para o aprendiz lv1
        mat_p2 = list()
        if janela == 'Sim':        
            
            for i in range(len(mat_in_p2)):
                aux = list()
                valor = float(aprendiz_lv0.predict([(mat_in_p2[i])])[0])
                aux.append(mat_in_p2[i][16])
                aux.append(mat_in_p2[i][17])
                aux.append(mat_in_p2[i][18])
                aux.append(valor)
                mat_p2.append(aux)
        else:
            for i in range(len(mat_in_p2)):
                aux = list()
                valor = float(aprendiz_lv0.predict([(mat_in_p2[i])])[0])
                aux.append(mat_in_p2[i][0])
                aux.append(mat_in_p2[i][1])
                aux.append(mat_in_p2[i][2])
                aux.append(valor)
                mat_p2.append(aux)
        return mat_p2, media_ea, media_er, porc_erro, r2


    def triangula(self, metodo, foco):
        t = Triangulaction()
        nor = Treinamento()
        if metodo == 'Inverse Distance Weighted':
            t.idw(foco)
            matriz_triang = nor.normalizar(t.get_idw()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = t.get_idw()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)
        elif metodo == 'Arithmetic Average':
            t.aa(foco)
            matriz_triang = nor.normalizar(t.get_aa()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = t.get_aa()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)
        elif metodo == 'Regional Weight':
            t.rw(foco)
            matriz_triang = nor.normalizar(t.get_rw()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = t.get_rw()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)
        elif metodo == 'Optimized Normal Ratio':
            t.onr(foco)
            matriz_triang = nor.normalizar(t.get_onr()[5])
            x,y,alv_y, erro_abs, erro_rel, mat_ext = t.get_onr()
            erro_abs, erro_rel = self.calcula_erro_tri(alv_y, y)

        tamanho = len(matriz_triang)
        t1 = floor(tamanho * 0.4)
        t2 = t1 * 2

        matriz_final_data = list()
        matriz_final_dado = list()
        
        for i in range(len(matriz_triang)):
            if i > t1 and i <= t2:
                aux = list()
                aux.append(matriz_triang[i][0])
                aux.append(matriz_triang[i][1])
                aux.append(matriz_triang[i][2])
                matriz_final_data.append(aux)
                matriz_final_dado.append(matriz_triang[i][3])
                

        return matriz_final_data, matriz_final_dado, erro_abs, erro_rel
        
        
    def calcula_erro_tri(self, x, y):
        t = Treinamento()
        mat1 = t.normalizar(x)
        mat2 = t.normalizar(y)
        
        soma_ea = 0
        soma_er = 0
        for i in range(len(mat1)):
            ea = abs(float(mat1[i]) - float(mat2[i]))
            er = ea / float(mat1[i])

            soma_ea = soma_ea + ea
            soma_er = soma_er + er

        ea = soma_ea / len(mat1)
        er = soma_er / len(mat2)
        return ea, er


    def meta_learning_personalizado(self, indicador, base_l, metodo_tri, meta_l, pre1, pre2, n_test, janela):
        m1_40_t, m1_40_r, m2_40_t, m2_40_r, m3_20_t, m3_20_r = self.prepara_input(indicador, janela)
        if base_l != 'Nenhum':
            matriz_input, base_ea, base_er, base_porc, base_r2 = self.base_learn(base_l, 0, n_test, m1_40_t, m1_40_r, m3_20_t, m3_20_r, m2_40_t, m2_40_r, janela)
            del matriz_input[:2]
        if metodo_tri != 'Nenhum':
            seila, matriz_trian, tria_ea, tria_er = self.triangula(metodo_tri, indicador)
            
            del matriz_trian[:4]
        
        matriz_datas, a, b, c = self.triangula('Arithmetic Average', indicador)
        del matriz_datas[:4]
        
        
        del m2_40_r[:2]
        
        matriz_f = list()
        result_f = list()
        for i in range(len(matriz_datas)):
            aux = list()
            if base_l == 'Nenhum' :
                aux.append(matriz_datas[i][0])
                aux.append(matriz_datas[i][1])
                aux.append(matriz_datas[i][2])
                aux.append(matriz_trian[i])
            elif metodo_tri == 'Nenhum':
                aux.append(matriz_datas[i][0])
                aux.append(matriz_datas[i][1])
                aux.append(matriz_datas[i][2])
                aux.append(matriz_input[i][3])
            else:
                aux.append(matriz_datas[i][0])
                aux.append(matriz_datas[i][1])
                aux.append(matriz_datas[i][2])
                aux.append(matriz_trian[i])
                aux.append(matriz_input[i][3])
            matriz_f.append(aux)

        if pre2 == 0:
            if meta_l == 'Decision Trees':
                aprendiz_lv1 = tree.DecisionTreeRegressor()
            elif meta_l == 'Neural network':
                aprendiz_lv1 = MLPRegressor()
            elif meta_l == 'Nearest Neighbors':
                aprendiz_lv1 = KNeighborsRegressor()
            elif meta_l == 'Support Vector':
                aprendiz_lv1 = SVR()

        
        t = len(matriz_f)
        divi = t - floor(t*0.2)
        x_apre = list()
        y_apre = list()

        x_test = list()
        y_test = list()
        
        for i in range(t):
            if i <= divi:
                x_apre.append(matriz_f[i])
                y_apre.append(m2_40_r[i])
            else:
                x_test.append(matriz_f[i])
                y_test.append(m2_40_r[i])
        soma = 0
        soma_er_nteste = 0
        soma_ea_nteste = 0
        x_meta = list()
        y_meta = list()
        y_alvo = list()

        x = 0
        for i in range(n_test):
            aprendiz_lv1 = aprendiz_lv1.fit(x_apre, y_apre)
            val = aprendiz_lv1.score(x_test, y_test)
            soma = soma + val #Calcular o R2

            soma_ea = 0
            soma_er = 0
            for j in range(len(x_test)):
                valor_ex = float(y_test[j])
                valor_aprox = float(aprendiz_lv1.predict([(x_test[j])])[0])

                y_meta.append(valor_aprox)
                y_alvo.append(valor_ex)
                x_meta.append(x)
                x += 1

                Erro_abs = abs(valor_ex - valor_aprox)
                Erro_rel = Erro_abs / valor_ex

                soma_ea = soma_ea + Erro_abs
                soma_er = soma_er + Erro_rel
            
            soma_ea_nteste = soma_ea_nteste + soma_ea/len(x_test)
            soma_er_nteste = soma_er_nteste + soma_er/len(x_test)
        meta_ea = soma_ea_nteste / n_test
        meta_er = soma_er_nteste / n_test
        meta_porc_erro = meta_ea * 100
        meta_r2 = soma / n_test
        
        if base_l == 'Nenhum':
            return meta_ea, meta_er, meta_porc_erro, meta_r2, x_meta, y_meta, y_alvo, 0, 0, 0, 0, tria_ea, tria_er
        elif metodo_tri == 'Nenhum':
            return meta_ea, meta_er, meta_porc_erro, meta_r2, x_meta, y_meta, y_alvo, base_ea, base_er, base_porc, base_r2, 0, 0
        else:
            return meta_ea, meta_er, meta_porc_erro, meta_r2, x_meta, y_meta, y_alvo, base_ea, base_er, base_porc, base_r2, tria_ea, tria_er
    
    def meta_learning_combina(self,  foco, pre1, pre2, n_test, janela):
        machine_l = ['Nenhum','Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector']
        triangulacao = ['Nenhum', 'Arithmetic Average', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']
        meta_l = ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector']
        
        todos_mod = list()
        ranking_mod = list()

        if foco == 'Precipitação':
            indicador = 1
        elif foco == 'Temperatura máxima':
            indicador = 2
        else:
             indicador = 3

        m1_40_t, m1_40_r, m2_40_t, m2_40_r, m3_20_t, m3_20_r = self.prepara_input(indicador, janela)

        arq = open(r'E:\IC\Interface_Grafica\Dados_verificacao\meta_comb.txt', 'w')
        arq2 = open(r'E:\IC\Interface_Grafica\Dados_verificacao\meta_res.csv', 'w')
        arq3 = open(r'E:\IC\Interface_Grafica\Dados_verificacao\meta_best_results.csv', 'w')

        arq2.write("Modelo;Machine Learning;Triangulação;Meta Learning;Erro Absoluto;Erro Relativo;Erro(%);R2;\n")
        arq3.write("Modelo;Erro(%);\n")
        Modelos = dict()
        cont_model = 1
        teste = repr("Modelo").center(8) + ' || ' + repr('Base-Learning').center(30) + ' || ' +  repr('Triangulation').center(30) + ' || ' + repr('Meta-Learning').center(30) + ' || ' +  repr("Erro(%)").center(20)
        
        for i in range(len(machine_l)):
            for j in range(len(triangulacao)):
                for k in range(len(meta_l)):
                    if machine_l[i] == 'Nenhum' and triangulacao[j] == 'Nenhum':
                        k += 1
                    else:
                        if machine_l[i] != 'Nenhum':
                            matriz_input, base_ea, base_er, base_porc, base_r2 = self.base_learn(machine_l[i], 0, n_test, m1_40_t, m1_40_r, m3_20_t, m3_20_r, m2_40_t, m2_40_r, janela)
                            del matriz_input[:2]
                        if triangulacao[j] != 'Nenhum':
                            seila, matriz_trian, tria_ea, tria_er = self.triangula(triangulacao[j], indicador)
                            del matriz_trian[:4]
                        
                        matriz_datas, a, b, c = self.triangula('Arithmetic Average', indicador)
                        del matriz_datas[:4]
                        del m2_40_r[:2]

                        matriz_f = list()
                        result_f = list()
                        for l in range(len(matriz_datas)):
                            aux = list()
                            if machine_l[i] == 'Nenhum' and triangulacao[j] != 'Nenhum':
                                aux.append(matriz_datas[l][0])
                                aux.append(matriz_datas[l][1])
                                aux.append(matriz_datas[l][2])
                                aux.append(matriz_trian[l])
                            if triangulacao[j] == 'Nenhum' and machine_l[i] != 'Nenhum':
                                aux.append(matriz_datas[l][0])
                                aux.append(matriz_datas[l][1])
                                aux.append(matriz_datas[l][2])
                                aux.append(matriz_input[l][3])
                            if triangulacao[j] != 'Nenhum' and machine_l[i] != 'Nenhum':
                                aux.append(matriz_datas[l][0])
                                aux.append(matriz_datas[l][1])
                                aux.append(matriz_datas[l][2])
                                aux.append(matriz_trian[l])
                                aux.append(matriz_input[l][3])
                            matriz_f.append(aux)

                        if pre2 == 0:
                            if meta_l[k] == 'Decision Trees':
                                aprendiz_lv1 = tree.DecisionTreeRegressor()
                            elif meta_l[k] == 'Neural network':
                                aprendiz_lv1 = MLPRegressor()
                            elif meta_l[k] == 'Nearest Neighbors':
                                aprendiz_lv1 = KNeighborsRegressor()
                            elif meta_l[k] == 'Support Vector':
                                aprendiz_lv1 = SVR()

                        
                        t = len(m2_40_r)
                        divi = t - floor(t*0.2)
                        x_apre = list()
                        y_apre = list()

                        x_test = list()
                        y_test = list()
                        
                        for n in range(t):
                            if n <= divi:
                                x_apre.append(matriz_f[n])
                                y_apre.append(m2_40_r[n])
                            else:
                                x_test.append(matriz_f[n])
                                y_test.append(m2_40_r[n])
                        soma = 0
                        soma_er_nteste = 0
                        soma_ea_nteste = 0
                        x_meta = list()
                        y_meta = list()
                        y_alvo = list()

                        x = 0
                        for l in range(n_test):
                            aprendiz_lv1 = aprendiz_lv1.fit(x_apre, y_apre)
                            val = aprendiz_lv1.score(x_test, y_test)
                            soma = soma + val #Calcular o R2

                            soma_ea = 0
                            soma_er = 0
                            for m in range(len(x_test)):
                                valor_ex = float(y_test[m])
                                valor_aprox = float(aprendiz_lv1.predict([(x_test[m])])[0])

                                y_meta.append(valor_aprox)
                                y_alvo.append(valor_ex)
                                x_meta.append(x)
                                x += 1

                                Erro_abs = abs(valor_ex - valor_aprox)
                                Erro_rel = Erro_abs / valor_ex

                                soma_ea = soma_ea + Erro_abs
                                soma_er = soma_er + Erro_rel
                            
                            soma_ea_nteste = soma_ea_nteste + soma_ea/len(x_test)
                            soma_er_nteste = soma_er_nteste + soma_er/len(x_test)
                        meta_ea = soma_ea_nteste / n_test
                        meta_er = soma_er_nteste / n_test
                        meta_porc_erro = meta_ea * 100
                        meta_r2 = soma / n_test

                        texto = str(cont_model) + " -> Machine Learning: " + machine_l[i] + "  ||  Triangulação: " + triangulacao[j] + "  || Meta Learning: " + meta_l[k] + "  |Resultados para " + str(n_test)+ " testes| --> Erro Absoluto: " + str(meta_ea) + "  |  Erro Relativo: " + str(meta_er) + "  |  Erro(%): " + str(meta_porc_erro) + "  |  R2: " + str(meta_r2)
                        arq.write(texto + "\n")
                        
                        teste = repr(cont_model).center(8) + ' || ' + repr(machine_l[i]).center(30) + ' || ' + repr(triangulacao[j]).center(30) + ' || ' + repr(meta_l[k]).center(30) + ' || ' + repr(meta_porc_erro).center(20)
                        #print(teste)
                        
                        
                        texto = str(cont_model) + ";" + machine_l[i] + ";" + triangulacao[j] + ";" + meta_l[k] + ";" + str(meta_ea).replace('.', ',') + ";" + str(meta_er).replace('.', ',') + ";" + str(meta_porc_erro).replace('.', ',') + ";" + str(meta_r2).replace('.', ',') + ";"   
                        arq2.write(texto + "\n")

                        Modelos[str(cont_model)] = meta_porc_erro
                        

                        aux = list()
                        aux.append(cont_model)      #0
                        aux.append(machine_l[i])    #1
                        aux.append(triangulacao[j]) #2
                        aux.append(meta_l[k])       #3
                        aux.append(n_test)          #4
                        aux.append(round(meta_ea, 4)) #5
                        aux.append(round(meta_er, 4)) #6
                        aux.append(round(meta_porc_erro, 4)) #7
                        aux.append(round(meta_r2, 4)) #8
                        todos_mod.append(aux)

                        cont_model += 1
        for z in sorted(Modelos, key=Modelos.get):
            arq3.write(str(z) + ";" + str(Modelos[z]).replace('.', ',') + ";\n")
            aux = list()
            aux.append(str(z))
            aux.append(str(Modelos[z]).replace('.', ','))
            ranking_mod.append(aux)             
        arq.close()
        arq2.close()
        arq3.close()

        return todos_mod, ranking_mod

class Tratamento:
    global alvo
    global vizinhaA
    global vizinhaB
    global vizinhaC
    global download
    alvo = vizinhaA = vizinhaB = vizinhaC = download = ''
    def __init__(self):
        self.alvo = alvo
        self.vizinhaA = vizinhaA
        self.vizinhaB = vizinhaB
        self.vizinhaC = vizinhaC
        self.download = download
        
    # def __init__(self, alvo, vizinhaA, vizinhaB, vizinhaC, download):
    
    
    def get_data_trada(self): #! Funçao para retornar os dados tratados
        diretorio = [self.alvo, self.vizinhaA, self.vizinhaB, self.vizinhaC]
       
        temp = [str(self.download) + "/alvo_limpa.txt", str(self.download) + "/vizinhaA_limpa.txt", str(self.download) + "/vizinhaB_limpa.txt", str(self.download) + "/vizinhaC_limpa.txt"]
        arq1 = open("end.txt", "w")
        arq1.write(str(self.download) + "/alvo_limpa.txt\n" + str(self.download) + "/vizinhaA_limpa.txt\n" + str(self.download) + "/vizinhaB_limpa.txt\n" + str(self.download) + "/vizinhaC_limpa.txt")
        arq1.close()
        cont = 0
        comum_alvo = comum_vizA = comum_vizB = comum_vizC = list()

        for dir in diretorio:
            aux = list()
            with open(dir) as arq: #* Abrindo os arquivos .csv e armazenando numa lista
                reader = csv.reader(arq)
                for line in reader:
                    aux.append(line)
        
            del aux[len(aux)-1]      #? Remove a ultima linha em branco do arquivo, da pra fazer isso manualmente, mas caso o usuario trabalhe com inumeros arquivos, remover a ultima linha de cada arquivo pode ser um trabalho massante 
            del aux[0:11]            #? Remove o cabeçalho do arquivo .csv
            
            for i in range(len(aux)): #* removendo caracteres e colunas desnecessários
                aux[i] = str(aux[i]).strip('[')     
                aux[i] = str(aux[i]).strip(']')
                aux[i] = str(aux[i]).strip("'")
                aux[i] = str(aux[i]).split(';')

                del aux[i][9] #* Removendo a ultima coluna, que está vazia '' 
                #* Deixando apenas as colunas de data, precipitação, temp max e temp min
                del aux[i][1:3]
                del aux[i][3]
                del aux[i][4:6]

            final = list()  #* Lista final 

            for i in range(len(aux)): #* Removendo todas as linhas que possuem o valor null em seu parametros
                condicao = 0
                for j in range(1,4):
                    if aux[i][j] == 'null':
                        condicao = 1

                if condicao == 0:
                    final.append(aux[i])    


            for i in range(len(final)): #* Passando a data de AAAA-MM-DD para AAAA, MM, DD
                aux.clear()
                for j in range(4):
                    aux.append(final[i][j])
                data = aux[0]
                data = str(data).split('-')

                final[i].insert(0, int(data[0]))
                final[i].insert(1, int(data[1]))
                final[i].insert(2, int(data[2]))
                del final[i][3]


            new_arq = open(temp[cont], 'w')    #TODO: Salvando os dados em arquivos .txt
            for i in final:
                if cont == 0:
                    comum_alvo.append(i)
                elif cont == 1:
                    comum_vizA.append(i)
                elif cont == 2:
                    comum_vizB.append(i)
                else:
                    comum_vizC.append(i)

                i = str(i).strip("[")
                i = str(i).strip("]")
                new_arq.write(str(i)+"\n")
            new_arq.close()
            cont += 1

        self.get_coordinates()
        
        self.dadosc()
        
    def dadosc(self):
        #subprocess.call(r'E:\IC\Interface_Grafica\codes\dadosc.py', shell=True)
        cid1, t1 = self.prepara_dadosc(str(self.download) + "/alvo_limpa.txt")
        cid2, t2 = self.prepara_dadosc(str(self.download) + "/vizinhaA_limpa.txt")
        cid3, t3 = self.prepara_dadosc(str(self.download) + "/vizinhaB_limpa.txt")
        cid4, t4 = self.prepara_dadosc(str(self.download) + "/vizinhaC_limpa.txt")
        ano_ini = max([cid1[0][0], cid2[0][0], cid3[0][0], cid4[0][0]])
        fim = min(len(cid1), len(cid2), len(cid3), len(cid4))
        
        for i in range(len(cid1)):
            if ano_ini == cid1[i][0]:
                ind1 = i
                break
        for i in range(len(cid2)):
            if ano_ini == cid2[i][0]:
                ind2 = i
                break
        for i in range(len(cid3)):
            if ano_ini == cid3[i][0]:
                ind3 = i
                break
        for i in range(len(cid4)):
            if ano_ini == cid4[i][0]:
                ind4 = i
                break

        final = list()
        aux = list()

        arq1 = open('end.txt', 'a')
        arq1.write('\n' + str(self.download) + '/dadoscomum.csv\n' + str(self.download) + '/buff.txt\n')
        arq1.close()

        arq = open(str(self.download) + '/dadoscomum.csv', 'w')

        arq_b = open(str(self.download) + '/buff.txt', 'w')
        total = 0
        for i in range(fim):
            ano1 = cid1[ind1+i][0]
            mes1 = cid1[ind1+i][1]
            dia1 = cid1[ind1+i][2]
            cond1 = 0
            for j in range(fim):
                ano2 = cid2[ind2+j][0]
                mes2 = cid2[ind2+j][1]
                dia2 = cid2[ind2+j][2]

                if (ano1 == ano2) and (mes1 == mes2) and (dia1 == dia2):
                    for k in range(fim):
                        ano3 = cid3[ind3+k][0]
                        mes3 = cid3[ind3+k][1]
                        dia3 = cid3[ind3+k][2] 
                        if (ano2 == ano3) and (mes2 == mes3) and (dia2 == dia3):
                                for z in range(fim):
                                    ano4 = cid4[ind4+z][0]
                                    mes4 = cid4[ind4+z][1]
                                    dia4 = cid4[ind4+z][2]
                                    if (ano3 == ano4) and (mes3 == mes4) and (dia3 == dia4):
                                        aux.clear()
                                        
                                        """  -> Adicionando os dados numa lista <-  """
                                        buff = ''   
                                        buff = str(ano1) + " " + str(mes1) + " " + str(dia1) + " " + cid1[ind1+i][3] + " " + cid1[ind1+i][4] + " " + cid1[ind1+i][5] + " " + cid2[ind2+j][3] + " " + cid2[ind2+j][4] + " " + cid2[ind2+j][5] + " " + cid3[ind3+k][3] + " " + cid3[ind3+k][4] + " " + cid3[ind3+k][5] + " " + cid4[ind4+z][3] + " " + cid4[ind4+z][4] + " " + cid4[ind4+z][5]  
                                        buff = str(buff).split()
                                        final.append(buff)
                                        
                                        """  -> Adicinando os dados num arquivo .csv <-  """
                                        buff = ''
                                        buff = str(ano1) + ";" + str(mes1) + ";" + str(dia1) + ";" + cid1[ind1+i][3] + ";" + cid1[ind1+i][4] + ";" + cid1[ind1+i][5] + ";" + cid2[ind2+j][3] + ";" + cid2[ind2+j][4] + ";" + cid2[ind2+j][5] + ";" + cid3[ind3+k][3] + ";" + cid3[ind3+k][4] + ";" + cid3[ind3+k][5] + ";" + cid4[ind4+z][3] + ";" + cid4[ind4+z][4] + ";" + cid4[ind4+z][5] + ";\n"
                                        arq.write(buff)
                                        total += 1
                                        cond1 = 1
                                        break
                                    
                                    
                                
                        if (cond1 == 1):
                            break
                
                if(cond1 == 1):
                    break
        arq_b.write(str(total) + " " + str(t1) + " " + str(t2) + " " + str(t3) + " " + str(t4))
        arq.close()
        arq_b.close()
        
        


    def prepara_dadosc(self, dir):
        arq = open(dir)
        lista = list()

        t=0
        for i in arq:
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            i = i.split(',')    
            lista.append(i)
            t += 1
        return lista, t


    def retorna_arq(self, op):
        arq = open('end.txt') 
        a = arq.readlines()
        print(a[0].replace("\n", ''))
        arq.close()
        if op == 'Cidade alvo':
            di = a[0].replace("\n", '')
        elif op == 'Vizinha A':
            di = a[1].replace("\n", '')
        elif op == 'Vizinha B':
            di = a[2].replace("\n", '')
        elif op == 'Vizinha C':
            di = a[3].replace("\n", '')
        elif op == 'Dados comum':
            di = a[4].replace("\n", '')
            
        

        
        lista = list()
        
        arq = open(di)
        
        for i in arq:
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            if op == 'Dados comum':
                i = i.split(';')
                del i[len(i)-1]
            else:
                i = i.split(',')  
            lista.append(i)
        arq.close()
        return lista
    
    def get_range(self, op):
        controle = 0
        arq = open('end.txt') 
        a = arq.readlines()
        print(a[0].replace("\n", ''))
        arq.close()
        if op == 'Cidade alvo':
            di = a[0].replace("\n", '')
        elif op == 'Vizinha A':
            di = a[1].replace("\n", '')
        elif op == 'Vizinha B':
            di = a[2].replace("\n", '')
        elif op == 'Vizinha C':
            di = a[3].replace("\n", '')
        elif op == 'Dados comum':
            di = a[4].replace("\n", '')
            controle = 1
            
        arq = open(di)
        aux = list()
    
        for i in arq:
            i = i.strip()
            i = i.replace("'",'')
            i = i.replace(" ",'')
            if controle == 1:
                i = i.split(';')
                del i[len(i)-1]
            else:
                i = i.split(',')
            aux.append(int(i[0]))
        arq.close()
        anos = list()
        buff = aux[0]
    
        anos.append(buff)
        
        for i in range(1,len(aux)): 
            try:
                if aux[i-1] != aux[i]:
                    buff = aux[i]
                    anos.append(buff)
            except IndexError:
                pass
        return anos

    def get_qtd(self):
        arq = open('end.txt') 
        a = arq.readlines()
        arq = open(a[5].replace("\n", ''))
        
        a = arq.readline()
        a = a.split()
        ut = int(a[0])
        Tar = int(a[1])
        vA = int(a[2])
        vB = int(a[3])
        vC = int(a[4])
        arq.close()
        return ut, Tar,vA, vB, vC

    def normalizar_dados(self, mat):
        max_min = list()
        aux = list()
        t = len(mat[0])
        for i in range(t):
            aux.clear()
            for j in range(len(mat)):
                aux.append(mat[j][i])
            max_min.append(max(aux))
            max_min.append(min(aux))

        dadosn =list()
        
    
        for i in range(len(mat)):
            cont = 0
            buff = list()
            for j in range(t):
                if cont <= 36:
                    maior = max_min[cont]
                    menor = max_min[cont + 1]
                    dado = ((float(mat[i][j]) - float(menor)) / (float(maior) - float(menor))) * 0.6 + 0.2
                    buff.append(dado)
                    cont = cont + 2
            dadosn.append(buff)
        
        
        return dadosn

    def get_coordinates(self): # ? Função para obter as coordenadas de cada cidade
        coordenadas = list()
        aux = list()
        locais = [self.alvo, self.vizinhaA, self.vizinhaB, self.vizinhaC]

        for i in locais:
            aux.clear()
            with open(i) as arq:
                reader = csv.reader(arq)
                for j in reader:
                    aux.append(j)
            
            del aux[10:]

            estacao = str(aux[0]).split(':')
            estacao = estacao[1].strip(']')
            estacao = (estacao.strip("'")).strip()

            latitude = str(aux[2]).split(':')
            latitude = latitude[1].strip(']')
            latitude = (latitude.strip("'")).strip()

            longitude = str(aux[3]).split(':')
            longitude = longitude[1].strip(']')
            longitude = (longitude.strip("'")).strip()

            altitude = str(aux[4]).split(':')
            altitude = altitude[1].strip(']')
            altitude = (altitude.strip("'")).strip()

            coordenadas.append(estacao)
            coordenadas.append(latitude)
            coordenadas.append(longitude)
            coordenadas.append(altitude)
        aux = str(self.download) + '/Coordenadas.txt'
        arq = open(aux, 'w')
        for i in coordenadas:
            arq.write(i)
            arq.write('\n')

        arq.close()    

class Selecionar_Arquivos_win(Toplevel):
    def tratar(self):
        datat = Tratamento() #* Criando um objeto que tem como atributos os endereços dos arquivos
        datat.alvo = self.dir_alvo.get()
        datat.vizinhaA = self.dir_vA.get()
        datat.vizinhaB = self.dir_vB.get()
        datat.vizinhaC = self.dir_vC.get()
        datat.download = self.dir_save.get()
        print(self.dir_save.get())
        datat.get_data_trada()
        msg.showinfo(title="Sucesso!", message="Arquivos Selecionados com sucesso!")
        Toplevel.destroy(self)
    def __init__(self, master=None):

        
        def procura_arq(entry_txt):
            path = dlg.askopenfilename()
            entry_txt.set(path)

        def escolhe_pasta(entry_txt):
            path = dlg.askdirectory()
            entry_txt.set(path)

        

        Toplevel.__init__(self, master=master)

        self.title('Selecionar arquivos')
        self.geometry("500x370")
        self.configure(background=fundo)


        Label(self, text='SELECIONAR ARQUIVOS', font='Arial 18 bold', fg='white',bg=fundo).place(x=110, y=10)

        self.dir_alvo = StringVar()
        Label(self, text="Cidade Alvo:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=50)   
        Entry(self, textvariable= self.dir_alvo, font='Arial 12', width=45).place(x=20, y=75)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_alvo)).place(x=440, y=73)

        self.dir_vA = StringVar()
        Label(self, text="Cidade vizinha A:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)   
        Entry(self, textvariable= self.dir_vA, font='Arial 12', width=45).place(x=20, y=125)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_vA)).place(x=440, y=123)

        self.dir_vB = StringVar()
        Label(self, text="Cidade vizinha B:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=150)   
        Entry(self, textvariable=self.dir_vB, font='Arial 12', width=45).place(x=20, y=175)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_vB)).place(x=440, y=173)

        self.dir_vC = StringVar()
        Label(self, text="Cidade vizinha C:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=200)   
        Entry(self, textvariable=self.dir_vC, font='Arial 12', width=45).place(x=20, y=225)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_vC)).place(x=440, y=223)

        self.dir_save = StringVar()
        Label(self, text="Local para salvar os dados tratados:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=250)
        teste = Entry(self, textvariable=self.dir_save, font='Arial 12', width=45).place(x=20, y=275)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: escolhe_pasta(self.dir_save)).place(x=440, y=273)

        #Todo: Para Agilizar os testes
        self.dir_alvo.set('E:/IC/Dados/TriangulacaoBH/BELOHORIZONTE.csv')
        self.dir_vA.set('E:/IC/Dados/TriangulacaoBH/FLORESTAL.csv')
        self.dir_vB.set('E:/IC/Dados/TriangulacaoBH/IBIRITE.csv')
        self.dir_vC.set('E:/IC/Dados/TriangulacaoBH/SETELAGOAS.csv')
        self.dir_save.set('E:/IC/Interface_Grafica/Dados_verificacao')

        Button(self, text='Prosseguir', font='Arial 12 bold', fg='white', bg=fun_b, width=45, command=self.tratar).place(x=21, y=320)

class Aprendizado_Marquina(Toplevel):
    def int_float(self, val):
        try:
            return int(val)
        except ValueError:
            return float(val)

    def valid_maxf(self, val):
        if val.isdigit() == True:
            val = int(val)
        elif val.isalnum() == True and val.isdigit() == False:
            val = str(val)
        elif val.isalnum() == False and val.isdigit() == False and val.isalpha() == False:
            val = float(val)
        
        return val

    def salvar_paramt(self):
        img = pyscreenshot.grab(bbox=(0,25,1920,1040))
        img.show()
        img.save(r'C:\Users\pablo\Desktop\teste.png')

    def data_prev(self, pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x):
        self.laf_res = LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)

        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)

        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_predict, label='Predict', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def gerar_preview_dt(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        


        if self.data_s.get() == 'Cidade alvo':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt'
        elif self.data_s.get() == 'Vizinha A':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaA_limpa.txt'
        elif self.data_s.get() == 'Vizinha B':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaB_limpa.txt'
        elif self.data_s.get() == 'Vizinha C':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaC_limpa.txt'

        indicador = self.ind_s.get()
        divisao = int(self.por_trei.get())
        criterio = self.criterion_v.get()
        splitter = self.splitter_v.get()
        maxd = int(self.maxd_v.get())             #* Max_depth
        minsams = self.int_float(self.minsam_s_v.get())    #* Min_samples_split
        minsaml = self.int_float(self.minsam_l_v.get())    #* Min_samples_leaf
        minwei = float(self.minweifra_l_v.get())
        maxfe = self.valid_maxf(self.maxfeat_v.get())
        maxleaf = int(self.maxleaf_n.get())
        
        minim = float(self.minimp_dec.get())
        ccp = float(self.ccp_alp_v.get())
        n_tes = int(self.num_teste.get())

        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.ArvoreDecisao(cidade, indicador, divisao, criterio, splitter, maxd, minsaml, maxfe, maxleaf, n_tes, minsams, minwei, minim, ccp, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def gerar_preview_nn(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        if self.data_s.get() == 'Cidade alvo':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt'
        elif self.data_s.get() == 'Vizinha A':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaA_limpa.txt'
        elif self.data_s.get() == 'Vizinha B':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaB_limpa.txt'
        elif self.data_s.get() == 'Vizinha C':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaC_limpa.txt'
        
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5
    
        divisao = int(self.por_trei.get())

        activ = self.activation_v.get()
        solv = self.solver_v.get()
        alph = float(self.alpha_v.get())
        batc = self.batch_size_v.get()
        learn_r = self.learning_rate_v.get()
        learn_r_ini = float(self.learning_rate_init_v.get())
        powt = float(self.power_t_v.get())
        maxit = int(self.max_iter_v.get())
        shuf = self.shuffle_v.get()
        tol = float(self.tol_v.get())
        verb = self.verbose_v.get()
        warms = self.warm_start_v.get()
        moment = float(self.momentum_v.get())
        neste = self.nesterovs_momentum_v.get()
        earlyst = self.early_stopping_v.get()
        valid = float(self.validation_fraction_v.get())
        b1 = float(self.beta_1_v.get())
        b2 = float(self.beta_2_v.get())
        niter = int(self.n_iter_no_change_v.get())
        maxfun = int(self.max_fun_v.get())
        n_teste = int(self.num_teste.get())
        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.RedeNeural(cidade, indicador, divisao, n_teste, activ, solv, alph, batc, learn_r, learn_r_ini, powt, maxit, shuf, tol, verb, warms, moment, neste, earlyst, valid, b1, b2, niter, maxfun, salvar_m)

        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
    
    def gerar_preview_svm(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        if self.data_s.get() == 'Cidade alvo':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt'
        elif self.data_s.get() == 'Vizinha A':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaA_limpa.txt'
        elif self.data_s.get() == 'Vizinha B':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaB_limpa.txt'
        elif self.data_s.get() == 'Vizinha C':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaC_limpa.txt'
        
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5
    
        divisao = int(self.por_trei.get())
        n_teste = int(self.num_teste.get())
        kern = self.kernel_v.get()
        degre = self.degree_v.get()
        gam = self.gamma_v.get()
        coef = float(self.coef0_v.get())
        t = float(self.tol_v.get())
        c = float(self.c_v.get())
        eps = float(self.epsilon_v.get())
        shr = self.shrinking_v.get()
        cach = float(self.cache_size_v.get())
        verb = self.verbose_v.get()
        maxi = int(self.maxiter_v.get())


        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.SVR(cidade, indicador, divisao, n_teste, kern, degre, gam, coef, t, c, eps, shr, cach, verb, maxi, salvar_m)

        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
        
    def gerar_preview_Kn(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        if self.data_s.get() == 'Cidade alvo':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt'
        elif self.data_s.get() == 'Vizinha A':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaA_limpa.txt'
        elif self.data_s.get() == 'Vizinha B':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaB_limpa.txt'
        elif self.data_s.get() == 'Vizinha C':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaC_limpa.txt'

        n_tes = int(self.num_teste.get())
        divisao = int(self.por_trei.get())
        n_neig = self.n_neighbors_v.get()
        algor = self.algorithm_v.get()
        leaf_s = self.leaf_size_v.get()
        pv = self.p_v.get()
        n_job = self.n_jobs_v.get()

        if n_job.isdigit() == True:
            n_job = int(n_job)
            
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.KNeighbors(cidade, indicador, divisao, n_tes, n_neig, algor, leaf_s, pv, n_job, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def gera_param(self):
        opcao = self.ml_selected.get()
        if opcao == 'Decision Trees':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_p = LabelFrame(self, text='Parâmetros', width=600, height=395, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=100)

            self.criterion_v = StringVar()
            lista_cri = ["squared_error", "friedman_mse", "absolute_error", "poisson"]
            self.criterion_v.set("squared_error")
            Label(self, text='Criterion:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_cri, textvariable=self.criterion_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

            self.splitter_v = StringVar()
            lista_spl = ["best", "random"]
            self.splitter_v.set("best")
            Label(self, text='Splitter:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            ttk.Combobox(self, values=lista_spl, textvariable=self.splitter_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)
            

            self.maxd_v = StringVar()
            self.maxd_v.set("10")
            Label(self, text="Max_deph (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            self.ent_maxd = Entry(self, textvariable=self.maxd_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

            self.minsam_s_v = IntVar()
            self.minsam_s_v.set(2)
            Label(self, text="Min_samples_split (int/float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            self.minsam_s = Entry(self, textvariable=self.minsam_s_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)
            
            self.minsam_l_v = IntVar()
            self.minsam_l_v.set(50)
            Label(self, text="Min_samples_leaf (int/float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            self.ent_minsam_l = Entry(self, textvariable=self.minsam_l_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

            self.minweifra_l_v = StringVar()
            self.minweifra_l_v.set("0.0")
            Label(self, text="Min_weight_fraction_leaf (float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            self.ent_minweifra_l = Entry(self, textvariable=self.minweifra_l_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)
            
            self.maxfeat_v = StringVar()
            self.maxfeat_v.set("auto")
            Label(self, text="Max_features :", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Label(self, text="Valores para Max_features:", font='Arial 12 bold', fg=fun_alt, bg=fundo).place(x=340, y=300)
            Label(self, text="int / float / 'auto' / 'sqrt' / 'log2'", font='Arial 12 bold', fg=fun_alt, bg=fundo).place(x=340, y=325)
            self.ent_maxfeat_v = Entry(self, textvariable=self.maxfeat_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

            self.maxleaf_n = StringVar()
            self.maxleaf_n.set("10")
            Label(self, text="Max_leaf_nodes (int)", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            self.ent_maxleaf_n = Entry(self, textvariable=self.maxleaf_n, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

            self.minimp_dec = StringVar()
            self.minimp_dec.set("0.0")
            Label(self, text="Min_impurity_decrease (float (.))", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            self.ent_minimp_dec = Entry(self, textvariable=self.minimp_dec, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

            self.ccp_alp_v = StringVar()
            self.ccp_alp_v.set("0.0")
            Label(self, text="Ccp_alpha (value>0.0 float):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            self.ent_ccp_alp = Entry(self, textvariable=self.ccp_alp_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

            self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=500)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=520)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=520)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=580)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=580)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)

           
            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_dt).place(x=50, y=685)
            #Button(self, text='Salvar Paramt.', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.salvar_paramt).place(x=340, y=685)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=685)
        elif opcao == 'Neural network':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=625, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)

            self.activation_v = StringVar()
            lista_act = ['identity', 'logistic', 'tanh', 'relu']
            self.activation_v.set('relu')
            Label(self, text='Activation:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_act, textvariable=self.activation_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)
            
            self.solver_v = StringVar()
            lista_sol = ['lbfgs', 'sgd', 'adam']
            self.solver_v.set('adam')
            Label(self, text='Solver:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            ttk.Combobox(self, values=lista_sol, textvariable=self.solver_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

            self.alpha_v = StringVar()
            self.alpha_v.set('0.0001')
            Label(self, text='Alpha:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.alpha_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

            self.batch_size_v = StringVar()
            self.batch_size_v.set('auto')
            Label(self, text='Batch_size (int / "auto"):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.batch_size_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

            self.learning_rate_v = StringVar()
            lista_learn = ['constant', 'invscaling', 'adaptive']
            self.learning_rate_v.set('constant')
            Label(self, text="Learning_rate:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            ttk.Combobox(self, values=lista_learn, textvariable=self.learning_rate_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=265)

            self.learning_rate_init_v = StringVar()
            self.learning_rate_init_v.set('0.001')
            Label(self, text='Learning_rate_init (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            Entry(self, textvariable=self.learning_rate_init_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)

            self.power_t_v = StringVar()
            self.power_t_v.set('0.5')
            Label(self, text='Power_t (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Entry(self, textvariable=self.power_t_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

            self.max_iter_v = StringVar()
            self.max_iter_v.set('200')
            Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=300)
            Entry(self, textvariable=self.max_iter_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=325)


            self.shuffle_v = BooleanVar()
            self.shuffle_v.set(True)
            Label(self, text='Shuffle (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            Entry(self, textvariable=self.shuffle_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

            self.tol_v = StringVar()
            self.tol_v.set('0.0001')
            Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            Entry(self, textvariable=self.tol_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

            self.verbose_v = BooleanVar()
            self.verbose_v.set(False)
            Label(self, text='Verbose (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            Entry(self, textvariable=self.verbose_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

            self.warm_start_v = BooleanVar()
            self.warm_start_v.set(False)
            Label(self, text='Warm_start (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=420)
            Entry(self, textvariable=self.warm_start_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=445)

            self.momentum_v = StringVar()
            self.momentum_v.set('0.9')
            Label(self, text='Momentum (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=480)
            Entry(self, textvariable=self.momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=505)

            self.nesterovs_momentum_v = BooleanVar()
            self.nesterovs_momentum_v.set(True)
            Label(self, text='Nesterovs_momentum:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=480)
            Entry(self, textvariable=self.nesterovs_momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=505)

            self.early_stopping_v = BooleanVar()
            self.early_stopping_v.set(False)
            Label(self, text='Early_stopping:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=540)
            Entry(self, textvariable=self.early_stopping_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=565)

            self.validation_fraction_v = StringVar()
            self.validation_fraction_v.set('0.1')
            Label(self, text='Validation_fraction (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=540)
            Entry(self, textvariable=self.validation_fraction_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=565)

            self.beta_1_v = StringVar()
            self.beta_1_v.set('0.9')
            Label(self, text='Beta_1 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=600)
            Entry(self, textvariable=self.beta_1_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=625)

            self.beta_2_v = StringVar()
            self.beta_2_v.set('0.999')
            Label(self, text='Beta_2 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=600)
            Entry(self, textvariable=self.beta_2_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=625)

            self.n_iter_no_change_v = StringVar()
            self.n_iter_no_change_v.set('10')
            Label(self, text='N_iter_no_change (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=660)
            Entry(self, textvariable=self.n_iter_no_change_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=685)

            self.max_fun_v = StringVar()
            self.max_fun_v.set('15000')
            Label(self, text='max_fun (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=660)
            Entry(self, textvariable=self.max_fun_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=685)

            '''   data   '''
            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=730)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=750)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=775)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=750)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=775)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=810)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=835)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=810)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=835)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_nn).place(x=50, y=915)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=915)
        elif opcao == 'Nearest Neighbors':

           w = Canvas(self, width=615, height=900, background=fundo, border=0)
           w.place(x=10, y=95)
           

           self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100) 

           self.n_neighbors_v = IntVar()
           self.n_neighbors_v.set(5)
           Label(self, text='N_neighbors (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
           Entry(self, textvariable=self.n_neighbors_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=145)

           self.algorithm_v = StringVar()
           lista_alg = ['auto', 'ball_tree', 'kd_tree', 'brute']
           self.algorithm_v.set('auto')
           Label(self, text='Algorithm:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
           ttk.Combobox(self, values=lista_alg, textvariable=self.algorithm_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

           self.leaf_size_v = IntVar()
           self.leaf_size_v.set(30)
           Label(self, text='Leaf_size (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
           Entry(self, textvariable=self.leaf_size_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

           self.p_v = IntVar()
           self.p_v.set(2)
           Label(self, text='P (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
           Entry(self, textvariable=self.p_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

           self.n_jobs_v = StringVar()
           self.n_jobs_v.set('5')
           Label(self, text='N_jobs (int / "None"):', font='Aria 12 bold', fg='white', bg=fundo).place(x=50, y=240)
           Entry(self, textvariable=self.n_jobs_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

           self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=320)

           self.data_s = StringVar()
           self.data_s.set('Cidade alvo')
           lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
           Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=340)
           self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

           self.ind_s = StringVar()
           self.ind_s.set('Temperatura máxima')
           lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
           Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=340)
           ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

           self.por_trei = IntVar()
           self.por_trei.set(70)
           Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=400)
           Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)

           self.num_teste = IntVar()
           self.num_teste.set(5)
           Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=400)
           self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

           Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_Kn).place(x=50, y=505)
           self.save_model = IntVar()
           Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505) 
        elif opcao == 'Support Vector':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=385, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)
            
            self.kernel_v = StringVar()
            lista_ker = ['linear', 'poly', 'rbf', 'sigmoid']
            self.kernel_v.set('rbf')
            Label(self, text='Kernel:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_ker, textvariable=self.kernel_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

            self.degree_v = IntVar()
            self.degree_v.set(3)
            Label(self, text='Degree (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            Entry(self, textvariable=self.degree_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145) 

            self.gamma_v = StringVar()
            self.gamma_v.set('scale')
            Label(self, text='Gamma ("scale", "auto", float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.gamma_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

            self.coef0_v = StringVar()
            self.coef0_v.set('0.0')
            Label(self, text='Coef0 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.coef0_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

            self.tol_v = StringVar()
            self.tol_v.set('0.001')
            Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            Entry(self, textvariable=self.tol_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)

            self.c_v = StringVar()
            self.c_v.set('1.0')
            Label(self, text='C (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            Entry(self, textvariable=self.c_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=265)

            self.epsilon_v = StringVar()
            self.epsilon_v.set('0.1')
            Label(self, text='Epsilon (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Entry(self, textvariable=self.epsilon_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=325)   

            self.shrinking_v = BooleanVar()
            self.shrinking_v.set(True)
            Label(self, text='Shrinking (Bool):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=300)
            Entry(self, textvariable=self.shrinking_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=325)

            self.cache_size_v = StringVar()
            self.cache_size_v.set('200')
            Label(self, text='Cache_size (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            Entry(self, textvariable=self.cache_size_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=385)   

            self.verbose_v = BooleanVar()
            self.verbose_v.set(False)
            Label(self, text='Verbose (Bool):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            Entry(self, textvariable=self.verbose_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=385)

            self.maxiter_v = IntVar()
            self.maxiter_v.set(-1)
            Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            Entry(self, textvariable=self.maxiter_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=445)

            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=500)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=520)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=520)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=580)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=580)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=680)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=680)
        elif opcao == 'Gaussian Process':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)
            
            self.alpha_gp = StringVar()
            self.alpha_gp.set('0.0000000001')
            Label(self, text='Alpha (float): ', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            Entry(self, textvariable=self.alpha_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=145)
            
            self.n_restarts_op = IntVar()
            self.n_restarts_op.set(0)
            Label(self, text='N_restart_optimizer (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            Entry(self, textvariable=self.n_restarts_op, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145)

            self.normalize_y_gp = BooleanVar()
            self.normalize_y_gp.set(0)
            Label(self, text='Normalize_y (Bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.normalize_y_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

            self.copy_X_train = BooleanVar()
            self.copy_X_train.set(0)
            Label(self, text='Copy_X_train (Bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.copy_X_train, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

            self.rand_state_gp = StringVar()
            self.rand_state_gp.set('None')
            Label(self, text='Random_state ("None" / int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            Entry(self, textvariable=self.rand_state_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)
            

            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=320)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=340)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=340)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=400)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=400)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=505)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505)

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Aprendizado de máquina')
        self.state("zoomed")
        self.configure(background=fundo)

        Label(self, text='APRENDIZADO DE MÁQUINA', font='Arial 14 bold', fg='white', bg=fundo).place(x=200, y=20)

        self.ml_selected = StringVar()
        self.ml_selected.set('Decision Trees')
        lista_ml = ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml, textvariable=self.ml_selected, width=28, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=60)
        Button(self, text='Escolher Machine Learning', font='Arial 11 bold', fg='white', bg=fun_ap, width=30, command=self.gera_param).place(x=340, y=59)

class Triangulaction_techniques(Toplevel):
    def ver_est(self):
        trian = Triangulaction()
        trian.show_map()

    def preview_idw(self):
        LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        trian = Triangulaction()
        ind = self.ind_s.get()
        if ind == 'Precipitação':
            foco = 1
        elif ind == 'Temperatura máxima':
            foco = 2
        else:
            foco = 3

        trian.idw(foco)

        eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_idw()
        
        pts = round(abs((media_er*100)-100) ,2)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)
        '''
        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)
        '''
        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_tri, label='IDW', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def preview_aa(self):
        LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        trian = Triangulaction()
        ind = self.ind_s.get()
        if ind == 'Precipitação':
            foco = 1
        elif ind == 'Temperatura máxima':
            foco = 2
        else:
            foco = 3

        trian.aa(foco)

        eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_aa()
        
        pts = round(abs((media_er*100)-100) ,2)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)
        '''
        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)
        '''
        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_tri, label='AA', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def preview_rw(self):
        LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        trian = Triangulaction()
        ind = self.ind_s.get()
        if ind == 'Precipitação':
            foco = 1
        elif ind == 'Temperatura máxima':
            foco = 2
        else:
            foco = 3

        trian.rw(foco)

        eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_rw()
        
        pts = round(abs((media_er*100)-100) ,2)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)
        '''
        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)
        '''
        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_tri, label='RW', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def preview_onr(self):
        LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        trian = Triangulaction()
        ind = self.ind_s.get()
        if ind == 'Precipitação':
            foco = 1
        elif ind == 'Temperatura máxima':
            foco = 2
        else:
            foco = 3

        trian.onr(foco)

        eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_onr()
        
        pts = round(abs((media_er*100)-100) ,2)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)
        '''
        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)
        '''
        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_tri, label='ONR', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()



    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Técnicas de Triangulação')
        self.state("zoomed")
        self.configure(background=fundo)

        Label(self, text='TÉCNICAS DE TRIANGULAÇÃO', font='Arial 14 bold', fg='white', bg=fundo).place(x=180, y=20)

        Button(self, text='Visualizar Estações', font='Arial 11 bold', fg='white', bg=fun_alt, width=55, command=self.ver_est).place(x=70, y=80)

        Label(self, text='Indicador climático:', font='Arial 13 bold', fg='white', bg=fundo).place(x=70, y=140)
        self.ind_s = StringVar()
        self.ind_s.set('Temperatura máxima')
        lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=40, font='Arial 11', justify=CENTER, state='readonly').place(x=230, y=140)


        LabelFrame(self, text='Métodos de Triangulação', width=600, height=250, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=200)

        Button(self, text='Arithmetic Average',font='Arial 11 bold', fg='white', bg=fun_alt, width=58, command=self.preview_aa).place(x=55, y=240)
        Button(self, text='Inverse Distance Weighted',font='Arial 11 bold', fg='white', bg=fun_alt, width=58, command=self.preview_idw).place(x=55, y=280)
        Button(self, text='Optimized Inverse Distance Weighted',font='Arial 11 bold', fg='white', bg=fun_alt, width=58).place(x=55, y=320)
        Button(self, text='Regional Weight',font='Arial 11 bold', fg='white', bg=fun_alt, width=58, command=self.preview_rw).place(x=55, y=360)
        Button(self, text='Optimized Normal Ratio',font='Arial 11 bold', fg='white', bg=fun_alt, width=58, command=self.preview_onr).place(x=55, y=400)

class MetaLearning(Toplevel):
    def gerar_teste_perso(self):
        base = self.ml_lv0_p.get()
        tria = self.ml_tr0_p.get()
        meta = self.ml_lv1.get()
        ind = self.ind_meta_perso.get()
        n_teste = int(self.num_teste_mtp.get())
        pre0 = int(self.pre_para_lv0.get())
        pre1 = int(self.pre_para_lv1.get())
        janela = self.type_input.get()
        if ind == 'Precipitação':
            foco = 1
        elif ind == 'Temperatura máxima':
            foco = 2
        elif ind == 'Temperatura mínima':
            foco = 3
        mp = MetaL()
        meta_ea, meta_er, meta_porc_erro, meta_r2, x_meta, y_meta, y_alvo, base_ea, base_er, base_porc, base_r2, tria_ea, tria_er = mp.meta_learning_personalizado(foco, base, tria, meta, 0, 0, n_teste, janela)
        
        
        LabelFrame(self, text='PREVIEW DOS RESULTADOS:', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=640, y=60)

        texto = "ERRO ABSOLUTO:    Machine Learning: " + str(round(base_ea, 4)) + "   ||   Triangulação: " + str(round(tria_ea,4)) + "   ||   Meta Learning: " + str(round(meta_ea,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=90)
        
        texto = "ERRO RELATIVO:      Machine Learning: " + str(round(base_er, 4)) + "   ||   Triangulação: " + str(round(tria_er,4)) + "   ||   Meta Learning: " + str(round(meta_er,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=130)
        
        texto = "ERRO(%):                     Machine Learning: " + str(round(base_porc, 4)) + "   ||   Triangulação: " + str(round(tria_ea*100,4)) +  "   ||   Meta Learning: " + str(round(meta_porc_erro,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=170)
        
        texto = "R2:                                  Machine Learning: " + str(round(base_r2, 4)) +  "   ||   Meta Learning: " + str(round(meta_r2,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=210)

        figura = Figure(figsize=(12.3, 7.5), dpi=100)
        plot1 = figura.add_subplot(2,2,1)
        x_ea = ["MacL", 'Trian', 'Meta']
        y_ea = [base_ea, tria_ea, meta_ea]
        plot1.bar(x_ea, y_ea)
        plot1.set_ylabel("Erro Absoluto")
        
        plot2 = figura.add_subplot(2,2,2)
        x_er = ["MacL", 'Trian', 'Meta']
        y_er = [base_er, tria_er, meta_er]
        plot2.bar(x_er, y_er)
        plot2.set_ylabel("Erro Relativo")

        plot3 = figura.add_subplot(2,2,3)
        x_por = ["MacL", 'Trian','Meta']
        y_por = [base_porc, tria_ea*100,meta_porc_erro]
        plot3.bar(x_por, y_por)
        plot3.set_ylabel("Erro (%)")

        plot4 = figura.add_subplot(2,2,4)
        x_r2 = ["MacL", 'Meta']
        y_r2 = [base_r2, meta_r2]
        plot4.bar(x_r2, y_r2)
        plot4.set_ylabel("R2")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=650, y=250)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def gerar_teste_global(self):
      
        foco = self.ind_meta_comb.get()
        num_t = int(self.num_teste_mtc.get())
        janela = 'Sim'
        
        mc = MetaL()
        
        todos, ranking = mc.meta_learning_combina(foco, 0, 0, num_t, janela)
        
        
        LabelFrame(self, text='RESULTADOS:', width=1260, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=640,y=60)

        Label(self, text='Modelos gerados:', font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=90)
                
        dados_todos = list()
        for i in range(len(todos)):
            buff = list()
            buff.append(todos[i][0])
            buff.append(todos[i][1])
            buff.append(todos[i][2])
            buff.append(todos[i][3])
            buff.append(todos[i][5])
            buff.append(todos[i][6])
            buff.append(todos[i][7])
            dados_todos.append(buff)

        self.tabela_todos = Sheet(self, data=dados_todos, headers=['Modelo','Base Learning', 'Triangulation', 'Meta Learning', 'Erro Absoluto', 'Erro Relativo', 'Erro(%)'], width=890, height=500)
        self.tabela_todos.enable_bindings()
        self.tabela_todos.place(x=660, y=120)
        

        Label(self, text='Ranking dos modelos:', font='Arial 12 bold', fg='white', bg=fundo).place(x=1580, y=90)

        dados_ranking = list()
        x = list()
        y = list()
        for i in range(len(ranking)):
            buff = list()
            buff.append(ranking[i][0])
            buff.append(round(float(ranking[i][1].replace(',', '.')), 4))  
            dados_ranking.append(buff)

            if i <= 15:
                x.append(str(ranking[i][0]))
                y.append(float(ranking[i][1].replace(',', '.')))

        
        self.tabela_ranking = Sheet(self, data=dados_ranking, headers=['Modelo', 'Erro'], width=270, height=500, column_width=115)
        self.tabela_ranking.enable_bindings()
        self.tabela_ranking.place(x=1580, y=120)   

        figura = Figure(figsize=(12, 3.3), dpi=100)
        plot = figura.add_subplot(1,1,1)

        plot.bar(x, y)
        plot.set_ylabel('Erro(%)')
        plot.set_xlabel("Modelos")
        plot.grid(True)
        
        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=660, y=650)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
     
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Meta Learning')
        self.state("zoomed")
        self.configure(background=fundo)

        Label(self, text='META-LEARNING', font='Arial 14 bold', fg='white', bg=fundo).place(x=240, y=20)

        LabelFrame(self, text='TESTE PERSONALIZADO:', width=600, height=450, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=60)

        Label(self, text='Base-Learning (Level 0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=90)
        self.ml_lv0_p = StringVar()
        self.ml_lv0_p.set('Decision Trees')
        lista_ml0 =  ['Nenhum','Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml0, textvariable=self.ml_lv0_p, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=120)

        Label(self, text='Triangulation (Level 0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=190)
        self.ml_tr0_p = StringVar()
        self.ml_tr0_p.set('Arithmetic Average')
        lista_tr0 =  ['Nenhum', 'Arithmetic Average', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']
        ttk.Combobox(self, values=lista_tr0, textvariable=self.ml_tr0_p, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=220)

        Label(self, text='Meta-Learning (Level 1):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=145)
        self.ml_lv1 = StringVar()
        self.ml_lv1.set('Decision Trees')
        lista_ml1 =  ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml1, textvariable=self.ml_lv1, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=340, y=175)

        Label(self, text='Indicador climático:', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=270)
        self.ind_meta_perso = StringVar()
        self.ind_meta_perso.set('Temperatura máxima')
        lista_ind_meta_p = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        ttk.Combobox(self, values=lista_ind_meta_p, textvariable=self.ind_meta_perso, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=300)

        self.num_teste_mtp = IntVar()
        self.num_teste_mtp.set(1)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=270)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste_mtp, width=29, font='Arial 12', justify=CENTER).place(x=340, y=300)

        Label(self, text='Deseja usar alguma ML pré-parametrizada?', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=340)
        self.pre_para_lv0 = IntVar()
        self.pre_para_lv1 = IntVar()
        Checkbutton(self, text='Level 0', variable=self.pre_para_lv0, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=40, y=360)
        Checkbutton(self, text='Level 1', variable=self.pre_para_lv1, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=180, y=360)
        
        Label(self, text='Deseja utilizar a janela deslizante?', font='Arial 12 bold', fg='White', bg=fundo).place(x=40, y=400)
        self.type_input = StringVar()
        self.type_input.set('Sim')
        lista_type_input = ['Sim', 'Não']
        ttk.Combobox(self, values=lista_type_input, textvariable=self.type_input, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=430)
        
        Button(self, text='Gerar Preview', font='Arial 11 bold', bg=fun_meta_le, fg='white', width=62, command=self.gerar_teste_perso).place(x=40, y=470)

        '''Teste global'''
        LabelFrame(self, text='TESTE GLOBAL:', width=600, height=210, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=520)
        
        Label(self, text='Quais MLs você deseja utilizar?', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=550)

        self.pre_nn_comb = IntVar()
        self.pre_dt_comb = IntVar()
        self.pre_nneig_comb = IntVar()
        self.pre_sv_comb = IntVar()
        self.pre_gp_comb = IntVar()
        Checkbutton(self, text='NN', variable=self.pre_nn_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=40, y=580)
        Checkbutton(self, text='DT', variable=self.pre_dt_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=140, y=580)
        Checkbutton(self, text='NNeig.', variable=self.pre_nneig_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=240, y=580)
        Checkbutton(self, text='SV', variable=self.pre_sv_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=580)
        Checkbutton(self, text='GP', variable=self.pre_gp_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=440, y=580)
        
        Label(self, text='Indicador climático:', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=620)
        self.ind_meta_comb = StringVar()
        self.ind_meta_comb.set('Temperatura máxima')
        lista_ind_meta_p = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        ttk.Combobox(self, values=lista_ind_meta_p, textvariable=self.ind_meta_comb, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=650)

        self.num_teste_mtc = IntVar()
        self.num_teste_mtc.set(1)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=620)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste_mtc, width=29, font='Arial 12', justify=CENTER).place(x=340, y=650)
        
        Button(self, text='Gerar Preview TG', font='Arial 11 bold', bg=fun_meta_le, fg='white', width=62, command=self.gerar_teste_global).place(x=40, y=690)

        #Aviso
        LabelFrame(self, text='ATENÇÃO:', width=600, height=120, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=740)
        Label(self, text='Dependendo da combinação feita no "Teste Personalizado" ou no "TESTE ', font='Arial 12 bold', fg='#FF8C00', bg=fundo).place(x=40, y=770)
        Label(self, text='GLOBAL", pode demorar alguns minutos, devido ao processamento.', font='Arial 12 bold', fg='#FF8C00', bg=fundo).place(x=40, y=790)
        Label(self, text='Fique à vontade para utilizar seu computador para fazer outras coisas.', font='Arial 12 bold', fg='#FF8C00', bg=fundo).place(x=40, y=820)

class Principal(Frame):
    def open_sa(self): #* sa = Selecionar Arquivos
        window = Selecionar_Arquivos_win()
        window.mainloop()

    def open_apr(self): 
        window = Aprendizado_Marquina()
        window.mainloop()
    
    def get_col(self):
        if self.num_enf.get() == "Precipitação":
            y_name = "Precipitação (mm)"
            col = 3
        elif self.num_enf.get() == "Temperatura máxima":
            col = 4
            y_name = "Temperatura (°C)"
        elif self.num_enf.get() == "Temperatura mínima":
            y_name = "Temperatura (°C)"
            col = 5
        return y_name, col

    def graficos_comum(self):
        my_data = Tratamento()
        data_ana = my_data.retorna_arq(self.num.get())
        
        self.gera_range()

        nome_y, col = self.get_col()

        eixo_x = list()
        if self.num.get() == 'Dados comum':
            eixo_y1 = list()
            eixo_y2 = list()
            eixo_y3 = list()
            eixo_y4 = list()
            util, tar,t_va, t_vb, t_vc = my_data.get_qtd()
            eixo_y_bar = [util, tar,t_va, t_vb, t_vc]
            eixo_x_bar = ['Comum', 'Alvo','Total vA', 'Total vB', 'Total vC']
        else:
            eixo_y = list()

        dados_lb = list()
        for i in data_ana:
            dados_lb.append(i)

            ano = str(i[0])
            mes = str(i[1])
            dia = str(i[2])
            text_data = mes + '/' + dia + '/' + ano
            eixo_x.append(dt.datetime.strptime(text_data,"%m/%d/%Y").date())

            if self.num.get() == 'Dados comum':
                eixo_y1.append(float(i[col]))
                eixo_y2.append(float(i[col+3]))
                eixo_y3.append(float(i[col+6]))
                eixo_y4.append(float(i[col+9]))
            else:
                eixo_y.append(float(i[col]))
        
        self.caixad_var.set(dados_lb)

        fig = Figure(figsize=(13,9.5), dpi=100)
        

        if self.num.get() == 'Dados comum':
            plot1 = fig.add_subplot(321)
            plot2 = fig.add_subplot(322)
            plot3 = fig.add_subplot(323)
            plot4 = fig.add_subplot(324)
            plot5 = fig.add_subplot(325)
            plot6 = fig.add_subplot(326)
            plot1.plot(eixo_x, eixo_y1, label="Alvo")
            plot2.plot(eixo_x, eixo_y2, label="Viz A", color="red")
            plot3.plot(eixo_x, eixo_y3, label="Viz B", color='green')
            plot4.plot(eixo_x, eixo_y4, label="Viz C", color='orange')
            plot5.scatter(eixo_x, eixo_y1, s=2, alpha=1, color='blue')
            plot5.scatter(eixo_x, eixo_y2, s=2, alpha=1, color='red')
            plot5.scatter(eixo_x, eixo_y3, s=2, alpha=1, color='green')
            plot5.scatter(eixo_x, eixo_y4, s=2, alpha=1, color='orange')
            plot6.bar(eixo_x_bar, eixo_y_bar)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot2.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot3.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot4.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot5.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot1.legend()
            plot2.legend()
            plot3.legend()
            plot4.legend()
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot3.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot4.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot5.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot1.grid(True)
            plot2.grid(True)
            plot3.grid(True)
            plot4.grid(True)
            plot5.grid(True)
            plot1.set_ylabel(nome_y)
            plot2.set_ylabel(nome_y)
            plot3.set_ylabel(nome_y)
            plot4.set_ylabel(nome_y)
            plot5.set_ylabel(nome_y)
            plot6.set_ylabel('Qtd. de dados')
            
        else:
            plot1 = fig.add_subplot(111)
            plot1.plot(eixo_x, eixo_y)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
                   
            plot1.grid(True)       
            plot1.set_ylabel(nome_y)
            plot1.set_title(self.num_enf.get())
        canvas = FigureCanvasTkAgg(fig, master=self.master)
            
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=600, y=57)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
        
    def graficos_range(self):
        my_data = Tratamento()
        data_ana = my_data.retorna_arq(self.num.get())
        
        nome_y, col = self.get_col()

        ano_inicio = int(self.var_ini.get())
        ano_final = int(self.var_fim.get())
        if ano_final < ano_inicio:
            msg.showerror(title='Invalid', message='O range inserido é inválido')
            return
        if self.num_enf.get() == 'Dados comum':
            self.grafico_dc(ano_inicio,ano_final)
            return
        
        eixo_x = list()
        if self.num.get() == 'Dados comum':
            eixo_y1 = list()
            eixo_y2 = list()
            eixo_y3 = list()
            eixo_y4 = list()
            util, tar,t_va, t_vb, t_vc = my_data.get_qtd()
            eixo_y_bar = [util, tar,t_va, t_vb, t_vc]
            eixo_x_bar = ['Comum', 'Alvo','Total vA', 'Total vB', 'Total vC']
        else:
            eixo_y = list()

        dados_lb = list()

        for i in data_ana:
            if int(i[0]) >= ano_inicio and int(i[0]) <= ano_final:
                dados_lb.append(i)

                ano = str(i[0])
                
                mes = str(i[1])
                dia = str(i[2])
                text_data = mes + '/' + dia + '/' + ano
                eixo_x.append(dt.datetime.strptime(text_data,"%m/%d/%Y").date())

                if self.num.get() == 'Dados comum':
                    eixo_y1.append(float(i[col]))
                    eixo_y2.append(float(i[col+3]))
                    eixo_y3.append(float(i[col+6]))
                    eixo_y4.append(float(i[col+9]))
                else:
                    eixo_y.append(float(i[col]))
        
        self.caixad_var.set(dados_lb)
        fig = Figure(figsize=(13,9.5), dpi=100)
        

        if self.num.get() == 'Dados comum':
            plot1 = fig.add_subplot(321)
            plot2 = fig.add_subplot(322)
            plot3 = fig.add_subplot(323)
            plot4 = fig.add_subplot(324)
            plot5 = fig.add_subplot(325)
            plot6 = fig.add_subplot(326)
            plot1.plot(eixo_x, eixo_y1, label="Alvo")
            plot2.plot(eixo_x, eixo_y2, label="Viz A", color="red")
            plot3.plot(eixo_x, eixo_y3, label="Viz B", color='green')
            plot4.plot(eixo_x, eixo_y4, label="Viz C", color='orange')
            plot5.scatter(eixo_x, eixo_y1, s=2, alpha=1, color='blue')
            plot5.scatter(eixo_x, eixo_y2, s=2, alpha=0.6, color='red')
            plot5.scatter(eixo_x, eixo_y3, s=2, alpha=0.6, color='green')
            plot5.scatter(eixo_x, eixo_y4, s=2, alpha=0.6, color='orange')
            plot6.bar(eixo_x_bar, eixo_y_bar)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot2.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot3.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot4.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot5.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot1.legend()
            plot2.legend()
            plot3.legend()
            plot4.legend()
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot3.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot4.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot5.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot1.grid(True)
            plot2.grid(True)
            plot3.grid(True)
            plot4.grid(True)
            plot5.grid(True)
            plot1.set_ylabel(nome_y)
            plot2.set_ylabel(nome_y)
            plot3.set_ylabel(nome_y)
            plot4.set_ylabel(nome_y)
            plot5.set_ylabel(nome_y)
            plot6.set_ylabel('Qtd. de dados')
            
        else:
            plot1 = fig.add_subplot(111)
            plot1.plot(eixo_x, eixo_y)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')   
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))   
                
            plot1.grid(True)
            plot1.set_ylabel(nome_y)
            plot1.set_title(self.num_enf.get())
        canvas = FigureCanvasTkAgg(fig, master=self.master)
            
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=600, y=57)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
    
    def gera_range(self):
        teste = Tratamento()
        self.var_ini = StringVar()
        self.anos = teste.get_range(self.num.get())
        Label(self, text='Início:', font='Arial 10 bold', fg='white', bg=fundo).place(x=40, y=190)
        self.com_ini = ttk.Combobox(self, values=self.anos, textvariable=self.var_ini, font='Arial 12', justify=CENTER, state='readonly', width=15).place(x=40, y=210)

        self.var_fim = StringVar()
        Label(self, text='Final:', font='Arial 10 bold', fg='white', bg=fundo).place(x=210, y=190)
        self.com_fim = ttk.Combobox(self, values=self.anos, textvariable=self.var_fim, font='Arial 12', justify=CENTER, state='readonly', width=15).place(x=210, y=210)
        
        Button(self, text='Definir Range', font='Arial 10 bold', fg='white', bg=fun_b, width=23, command=self.graficos_range).place(x=380, y=209)

        print(self.var_fim.get())
            
    def open_tri(self):
        window = Triangulaction_techniques()
        window.mainloop()

    def open_meta_learning(self):
        window = MetaLearning()
        window.mainloop()

    def __init__(self, *args, **kwargs):
        
        Frame.__init__(self, master=None, bg=fundo)
        
        self.master.title("IC_FAPEMIG - IG V1.1")
        self.master.state("zoomed")

        Label(self, text='TRATAMENTO DE DADOS', font='Arial 14 bold', fg='white', bg=fundo).place(x=190, y=20)
        self.btn_select = Button(self, text="Selecionar arquivos .csv", font='Arial 12 bold ', fg='white',bg=fun_b, width=52, command=self.open_sa)
        self.btn_select.place(x=40, y=60)

        Label(self, text='VIZUALIZAR DADOS', font='Arial 14 bold', fg='white', bg=fundo).place(x=215, y=100)
        
        self.num = StringVar()
        caixa = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C', 'Dados comum']
        Label(self, text="Dado:", font='Arial 10 bold', bg=fundo, fg='white').place(x=40, y=140)
        self.combo = ttk.Combobox(self, values=caixa, textvariable=self.num, width=15, font='Arial 12', justify=CENTER, state='readonly').place(x=40, y=160)
        

        self.num_enf = StringVar()
        enfoque = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        Label(self, text='Parâmetro:', font='Arial 10 bold', bg=fundo, fg='white').place(x=210, y=140)
        self.com_enf = ttk.Combobox(self, values=enfoque, textvariable=self.num_enf, width=15, font='Arial 12', justify=CENTER, state='readonly').place(x=210, y=160)
    
        Button(self, text='Selecionar', font='Arial 10 bold', fg='white', bg=fun_b, width=23, command=self.graficos_comum).place(x=380, y=159)

        self.caixad_var = StringVar()
        self.caixa_data = Listbox(self, width=75, height=15 ,listvariable=self.caixad_var, font='Arial 10').place(x=40, y=250)

        Button(self, text='Aprendizado de Máquina', font='Arial 12 bold', fg='white', bg=fun_ap, width=52, command=self.open_apr).place(x=40, y=520)
        self.pack(fill='both', expand=True)

        Button(self, text='Triangulação', font='Arial 12 bold', fg='white', bg=fun_alt,width=52, command=self.open_tri).place(x=40, y=560)

        Button(self, text='Meta-Learning', font='Arial 12 bold', fg='white', bg=fun_meta_le, width=52, command=self.open_meta_learning).place(x=40, y=600)
        
if __name__ == '__main__':
    mainwindow = Principal()
    mainwindow.mainloop()   