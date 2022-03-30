from triangulacao import Triangulaction
from tratar import Tratamento
from ml import Treinamento
from math import floor
from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

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
    
    def base_learn(self, mach, pre, n_test, mat_in_tr, mat_res_tr, mat_in_valid, mat_res_valid, mat_in_p2, mat_res_p2):
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

        mat_valid_meta = list() #Lista com os predicts do aprendiz de level 0 para a validação no meta learning
        for i in range(len(mat_in_valid)):
            valor = float(aprendiz_lv0.predict([(mat_in_valid[i])])[0])
            mat_valid_meta.append(valor) #Somente o valor do predict
        
        mat_input_meta = list() #Lista com a data (5o dia) + o predict do aprendiz de level 0
        for i in range(len(mat_in_p2)):
            aux = list()
            valor = float(aprendiz_lv0.predict([(mat_in_p2[i])])[0])
            aux.append(mat_in_p2[i][16])
            aux.append(mat_in_p2[i][17])
            aux.append(mat_in_p2[i][18])
            aux.append(valor)  
            mat_input_meta.append(aux)

        return media_ea, media_er, porc_erro, r2, mat_valid_meta, mat_input_meta

        

