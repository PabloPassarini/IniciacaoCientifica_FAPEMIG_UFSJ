from re import X
from scipy import stats
from lib2to3.pgen2.pgen import generate_grammar
from haversine import haversine, Unit
from tratar import Tratamento
from ml import Treinamento
import folium
from folium.map import Popup
import webbrowser
import math
import numpy as np
class Triangulaction:
    def __init__(self):
        self.coordenadas = list()
        cod_trat = Tratamento()
        local = cod_trat.get_local_cord()
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
        media = (d1 + d2 + d3) / 3
        print("Cidade A: {}km  ||  Cidade B: {}km  || Cidade C: {}km  || Média: {}km".format(d1,d2,d3, media))
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
        print(data[0])
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
        '''
        exato = t.normalizar(real)
        aproximado = t.normalizar(aprox)
        ''' 
        exato = real  
        aproximado = aprox  
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
     