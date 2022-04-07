from matplotlib import projections
from triangulacao import Triangulaction
from tratar import Tratamento
from ml import Treinamento
from math import floor
from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
import os
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
        #               (base_l, 0, n_test, m1_40_t, m1_40_r, m3_20_t, m3_20_r, m2_40_t, m2_40_r)
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
            aux = list()
            aux.append(mat_in_valid[i][16])
            aux.append(mat_in_valid[i][17])
            aux.append(mat_in_valid[i][18])
            aux.append(valor)
            mat_valid_meta.append(aux) #Somente o valor do predict
            
        
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

    def triangula_data(self, metodo, foco):
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
        
        tam = len(matriz_triang)
        t1 = floor(tam * 0.4)
        t2 = t1 * 2

        m1_40 = list() #Não precisa, pois não vai ser utilizada em nenhuma "inputação"
        m1_r  = list()
        m2_40 = list() #Vai ser utilizada para o input do meta learning
        m2_r  = list()
        m3_20 = list() #Vai ser utilizada para a validação do meta learning
        m3_r  = list()
        for i in range(tam):
            if i <= t1:   #Fazendo pra caso um dia precise
                
                aux = list()
                aux.append(matriz_triang[i][0])
                aux.append(matriz_triang[i][1])
                aux.append(matriz_triang[i][2])
                aux.append(matriz_triang[i][3])
                m1_40.append(aux)
                m1_r.append(alv_y[i])
            elif i > t1 and i <= t2:
                aux = list()
                aux.append(matriz_triang[i][0])
                aux.append(matriz_triang[i][1])
                aux.append(matriz_triang[i][2])
                aux.append(matriz_triang[i][3])
                m2_40.append(aux)
                m2_r.append(alv_y[i])
            else:
                aux = list()
                aux.append(matriz_triang[i][0])
                aux.append(matriz_triang[i][1])
                aux.append(matriz_triang[i][2])
                aux.append(matriz_triang[i][3])
                m3_20.append(aux)
                m3_r.append(alv_y[i])

        return m1_40, m2_40, m3_20, m1_r, m2_r, m3_r, erro_abs, erro_rel
    
    def prepara_input_comb_meta(self, mat_input_meta, m2_tri, m2_40_r, m2_r, mat_valid_meta, m3_tri, m3_20_r, m3_r):
        matriz_x_meta = list()
        matriz_y_meta = list()
        
        t = len(mat_input_meta)
        if len(m2_tri) < t:
            t = len(m2_tri)
        
        for i in range(t): #Dados para a inputação do Meta Learning
            matriz_x_meta.append(mat_input_meta[i])
            matriz_x_meta.append(m2_tri[i])

            matriz_y_meta.append(m2_40_r[i])
            matriz_y_meta.append(m2_r[i])

        matriz_x_valida_meta = list()
        matriz_y_valida_meta = list()

        t = len(mat_valid_meta)
        if len(m3_tri) < t:
            t = len(m3_tri)

        for i in range(t): #Dados para a validação do Meta Learning
            matriz_x_valida_meta.append(mat_valid_meta[i])
            matriz_x_valida_meta.append(m3_tri[i])

            matriz_y_valida_meta.append(m3_20_r[i])
            matriz_y_valida_meta.append(m3_r[i])
        
        return matriz_x_meta, matriz_y_meta, matriz_x_valida_meta, matriz_y_valida_meta

    def meta_learning_personalizado(self, indicador, base_l, metodo_tri, meta_l, pre1, pre2, n_test, janela):
        m1_40_t, m1_40_r, m2_40_t, m2_40_r, m3_20_t, m3_20_r = self.prepara_input(indicador, janela)
        
        if base_l != 'Nenhum':
            media_ea, media_er, porc_erro, r2, mat_valid_meta, mat_input_meta = self.base_learn(base_l, 0, n_test, m1_40_t, m1_40_r, m3_20_t, m3_20_r, m2_40_t, m2_40_r)
            
        if metodo_tri != 'Nenhum':
            m1_tri, m2_tri, m3_tri, m1_r, m2_r, m3_r, tria_ea, tria_er = self.triangula_data(metodo_tri, indicador)

        # Matriz de treinamento (x) = mat_input_meta [ano, mes, dia, predict]  || Matriz de respostas (y): m2_40_r [valor real]
        # Matriz de validação (x) = mat_valid_meta [ano, mes, dia predict]     || Matriz de respostas (y): m3_20_r [valor real]
        
        matriz_x_meta, matriz_y_meta, matriz_x_valida_meta, matriz_y_valida_meta = self.prepara_input_comb_meta(mat_input_meta, m2_tri, m2_40_r, m2_r, mat_valid_meta, m3_tri, m3_20_r, m3_r)



        if pre2 == 0:
            if meta_l == 'Decision Trees':
                aprendiz_lv1 = tree.DecisionTreeRegressor()
            elif meta_l == 'Neural network':
                aprendiz_lv1 = MLPRegressor()
            elif meta_l == 'Nearest Neighbors':
                aprendiz_lv1 = KNeighborsRegressor()
            elif meta_l == 'Support Vector':
                aprendiz_lv1 = SVR()
        
        soma_r2 = 0
        soma_er_nteste = 0
        soma_ea_nteste = 0
        
        for i in range(n_test):
            aprendiz_lv1 = aprendiz_lv1.fit(matriz_x_meta, matriz_y_meta)
            val = aprendiz_lv1.score(matriz_x_valida_meta, matriz_y_valida_meta)
            soma_r2 += val
            soma_ea = 0
            soma_er = 0
            for j in range(len(matriz_x_valida_meta)):
                valor_ex = matriz_y_valida_meta[j]
                
                valor_aprox = float(aprendiz_lv1.predict([(matriz_x_valida_meta[j])])[0])

                Erro_abs = abs(valor_ex - valor_aprox)
                Erro_rel = Erro_abs / valor_ex

                soma_ea = soma_ea + Erro_abs
                soma_er = soma_er + Erro_rel
            
            soma_ea_nteste = soma_ea_nteste + soma_ea/len(matriz_x_valida_meta)
            soma_er_nteste = soma_er_nteste + soma_er/len(matriz_x_valida_meta)
        meta_ea = soma_ea_nteste / n_test
        meta_er = soma_er_nteste / n_test
        meta_porc_erro = meta_ea * 100
        meta_r2 = soma_r2 / n_test
        
    def meta_learning_combina(self,  foco, pre1, pre2, n_test, janela):
        machine_l = ['Nenhum', 'Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector']
        triangulacao = ['Arithmetic Average', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']
        meta_l = ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector']
        
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
        
        todos_mod = list()
        ranking_mod = list()
        Modelos = dict()
        cont_model = 1
        for i in range(len(machine_l)):
                for j in range(len(triangulacao)):
                    for k in range(len(meta_l)):
                        if machine_l[i] == 'Nenhum' and triangulacao[j] == 'Nenhum':
                            k += 1
                        else:
                            if machine_l[i] != 'Nenhum':
                                media_ea, media_er, porc_erro, r2, mat_valid_meta, mat_input_meta = self.base_learn(machine_l[i], 0, n_test, m1_40_t, m1_40_r, m3_20_t, m3_20_r, m2_40_t, m2_40_r)
                            if triangulacao[j] != 'Nenhum':
                                m1_tri, m2_tri, m3_tri, m1_r, m2_r, m3_r, tria_ea, tria_er = self.triangula_data(triangulacao[j], indicador)

                            matriz_x_meta = list()
                            matriz_y_meta = list()
                            matriz_x_valida = list()
                            matriz_y_valida = list()
                            try:
                                t = len(mat_input_meta)
                                if len(m2_tri) < t:
                                    t = len(m2_tri)
                            except UnboundLocalError:
                                t = len(m2_tri)
                            for l in range(t):
                                if machine_l[i] == 'Nenhum' and triangulacao[j] != 'Nenhum':
                                    matriz_x_meta.append(m2_tri[l])
                                    matriz_y_meta.append(m2_r[l])
                                if triangulacao[j] == 'Nenhum' and machine_l[i] != 'Nenhum':
                                    matriz_x_meta.append(mat_input_meta[l])
                                    matriz_y_meta.append(m2_40_r[l])
                                if triangulacao[j] != 'Nenhum' and machine_l[i] != 'Nenhum':
                                    matriz_x_meta.append(mat_input_meta[l])
                                    matriz_x_meta.append(m2_tri[l])
                                    matriz_y_meta.append(m2_40_r[l])
                                    matriz_y_meta.append(m2_r[l])
                            try:
                                t = len(mat_valid_meta)
                                if len(m3_tri) < t:
                                    t = len(m3_tri)
                            except UnboundLocalError:
                                t = len(m3_tri)
                            for l in range(t):
                                if machine_l[i] == 'Nenhum' and triangulacao[j] != 'Nenhum':
                                    matriz_x_valida.append(m3_tri[l])
                                    matriz_y_valida.append(m3_r[l])
                                if triangulacao[j] == 'Nenhum' and machine_l[i] != 'Nenhum':
                                    matriz_x_valida.append(mat_valid_meta[l])
                                    matriz_y_valida.append(m3_20_r[l])
                                if triangulacao[j] != 'Nenhum' and machine_l[i] != 'Nenhum':
                                    matriz_x_valida.append(mat_valid_meta[l])
                                    matriz_x_valida.append(m3_tri[l])
                                    matriz_y_valida.append(m3_20_r[l])
                                    matriz_y_valida.append(m3_r[l])
                            
                            if pre2 == 0:
                                if meta_l[k] == 'Decision Trees':
                                    aprendiz_lv1 = tree.DecisionTreeRegressor()
                                elif meta_l[k] == 'Neural network':
                                    aprendiz_lv1 = MLPRegressor()
                                elif meta_l[k] == 'Nearest Neighbors':
                                    aprendiz_lv1 = KNeighborsRegressor()
                                elif meta_l[k] == 'Support Vector':
                                    aprendiz_lv1 = SVR()

                            soma = 0
                            soma_er_nteste = 0
                            soma_ea_nteste = 0
                           
                            
                            for l in range(n_test):
                                aprendiz_lv1 = aprendiz_lv1.fit(matriz_x_meta, matriz_y_meta)
                                val = aprendiz_lv1.score(matriz_x_valida, matriz_y_valida)
                                soma += val

                                soma_ea = 0
                                soma_er = 0

                                for m in range(len(matriz_x_valida)):
                                    valor_ex = matriz_y_valida[m]
                                    valor_aprox = float(aprendiz_lv1.predict([(matriz_x_valida[m])])[0])

                                    Erro_abs = abs(valor_ex - valor_aprox)
                                Erro_rel = Erro_abs / valor_ex

                                soma_ea = soma_ea + Erro_abs
                                soma_er = soma_er + Erro_rel
                            
                            soma_ea_nteste = soma_ea_nteste + soma_ea/len(matriz_x_valida)
                            soma_er_nteste = soma_er_nteste + soma_er/len(matriz_x_valida)
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
        for i in todos_mod:
            print(i)     
                            


os.system('cls')
m = MetaL()
m1_40_t, m1_40_r, m2_40_t, m2_40_r, m3_20_t, m3_20_r = m.prepara_input(1, 'Sim')
media_ea, media_er, porc_erro, r2, mat_valid_meta, mat_input_meta = m.base_learn('Neural network', 0, 5, m1_40_t, m1_40_r, m3_20_t, m3_20_r, m2_40_t, m2_40_r)
m.meta_learning_personalizado(1, 'Neural network', 'Arithmetic Average', 'Neural network', 0, 0, 5, 'Sim')
m.meta_learning_combina('Temperatura máxima', 0,0,1,'Sim')