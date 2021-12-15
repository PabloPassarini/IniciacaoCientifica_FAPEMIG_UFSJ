from math import floor
from sklearn import tree
class Treinamento:
    def ArvoreDecisao(self, cidade, indic, divisao, cri, spli, max_d, min_s, max_f,  max_l, n_testes):
        m_trei, r_trei, m_vali, r_vali = self.prepara_matriz(cidade, divisao, indic, 0)
        soma_er_nteste = 0 #* Soma dos erros relativos dos n testes
        soma_ea_nteste = 0 #* Soma dos erros absolutos dos n testes

        eixo_y_exato = list()
        eixo_y_predict = list()
        eixo_x = list()
        cont = 1
        for j in range(n_testes):
            aprendiz = tree.DecisionTreeRegressor(criterion=cri, splitter=spli, max_depth=max_d, min_samples_leaf=min_s, max_features=max_f, max_leaf_nodes=max_l)
            aprendiz = aprendiz.fit(m_trei, r_trei)

            soma_ea = 0 #* Soma dos erros absolutos
            soma_er = 0 #* Soma dos erros relativos

            for i in range(len(m_vali)):
                valor_exato = r_vali[i]
                valor_aprox = aprendiz.predict([m_vali[i]])[0]
                if j == (n_testes-1):
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

            pontuacao = round((((soma_er_nteste/30)*100) - 100)* (-1),2)
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


        return pontuacao, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x
        

    
    def prepara_matriz(self, local, divi, indicador, qtd_in):
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
        
        buff.clear()
        
        for i in range(len(aux1)):
            buff = list()
            try:
                for j in range(5):
                    buff.append(aux1[i+j][0])
                    buff.append(aux1[i+j][1])
                    buff.append(aux1[i+j][2])
                    buff.append(aux1[i+j][3])
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
        return matriz_treinamento, resultado_treinamento, matriz_validacao, resultado_validacao
