from triangulacao import Triangulaction
from tratar import Tratamento
from ml import Treinamento
from math import floor

from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from operator import itemgetter, attrgetter
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
