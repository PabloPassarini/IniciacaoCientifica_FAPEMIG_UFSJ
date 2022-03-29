from cgi import test
from math import floor
import time
from sklearn import tree
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from tratar import Tratamento
import pickle





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

