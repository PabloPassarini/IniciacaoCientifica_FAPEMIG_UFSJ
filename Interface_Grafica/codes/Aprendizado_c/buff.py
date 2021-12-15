from sklearn import tree
import os, time
from math import floor

os.system('cls')

def prepara_matriz(local, indicador, qtd_in):
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
    tam = floor(len(matriz)*0.7)
    matriz70 = list()
    resultado70 = list()
    matriz30 = list()
    resultado30 = list()
    for i in range(len(matriz)):
        if i <= tam:
            matriz70.append(matriz[i])
            resultado70.append(resultado[i])
        else:
            matriz30.append(matriz[i])
            resultado30.append(resultado[i])
    return matriz, resultado, matriz70, resultado70, matriz30, resultado30


def Aprendiz1(x7, y7, x3, y3,testes):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor()
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz 1: ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->Criterion: squared_erro  ||  ->Spliter: best\n"
    return texto

def Aprendiz2(x7, y7, x3, y3, testes):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor(criterion="friedman_mse")
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz 2: ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->Criterion: friedman_mse  ||  ->Spliter: best\n"
    return texto

def Aprendiz3(x7, y7, x3, y3,testes):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor(criterion="poisson")
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz 3: ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->Criterion: poisson  ||  ->Spliter: best\n"
    return texto

def Aprendiz4(x7, y7, x3, y3,testes):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor(criterion="absolute_error")
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz 4: ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->Criterion: absolute_error  ||  ->Spliter: best\n"
    return texto

def Aprendiz5(x7, y7, x3, y3,testes):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor(splitter='random')
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz 5: ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->Criterion: squared_erro  ||  ->Spliter: random\n"
    return texto

def Aprendiz6(x7, y7, x3, y3,testes):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor(criterion="friedman_mse", splitter='random')
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz 6: ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->Criterion: friedman_mse  ||  ->Spliter: random\n"
    return texto

def Aprendiz7(x7, y7, x3, y3,testes, md, n):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor(criterion="friedman_mse", splitter='random', max_depth=md)
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz " + str(n) +": ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->criterion=friedman_mse  ||  ->Spliter: best || maxmax_depth: "+ str(md) +"\n"
    return texto

def Aprendiz8(x7, y7, x3, y3,testes, min_S, n):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor(criterion="friedman_mse", splitter='random', max_depth=10, min_samples_leaf=min_S)
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz "+ str(n)  +": ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->criterion=friedman_mse  ||  ->Spliter: best || maxmax_depth: 10  || min_samples_leaf="+ str(min_S) +"\n"
    return texto

def Aprendiz9(x7, y7, x3, y3,testes, min_S, n):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor(splitter='random', max_depth=10, min_samples_leaf=min_S, max_features='auto', criterion="friedman_mse")
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz "+ str(n)  +": ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->criterion=friedman_mse  ||  ->Spliter: best || maxmax_depth: 10  || min_samples_leaf="+ str(min_S) +"  ||  max_features='auto'\n"
    return texto

def Aprendiz10(x7, y7, x3, y3,testes, min_S, n):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor(splitter='random', max_depth=10, min_samples_leaf=min_S, max_features='log2', criterion="friedman_mse")
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz "+ str(n)  +": ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->criterion=friedman_mse  ||  ->Spliter: best || maxmax_depth: 10  || min_samples_leaf="+ str(min_S) +"  ||  max_features='log2'\n"
    return texto


def Aprendiz11(x7, y7, x3, y3,testes, min_S, n):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor(splitter='random', max_depth=10, min_samples_leaf=min_S, max_features='sqrt', criterion="friedman_mse")
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz "+ str(n)  +": ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->criterion=friedman_mse  ||  ->Spliter: best || maxmax_depth: 10  || min_samples_leaf="+ str(min_S) +"  ||  max_features='sqrt'\n"
    return texto

def Aprendiz12(x7, y7, x3, y3,testes, min_S, n, max_l):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(testes):
        clf = tree.DecisionTreeRegressor(splitter='random', max_depth=10, min_samples_leaf=min_S, max_features=None, max_leaf_nodes=max_l, criterion="friedman_mse")
        clf = clf.fit(x7, y7)

        soma_ea = 0
        soma_er = 0

        for i in range(len(x3)):
            exato = y3[i]
            aprox = clf.predict([x3[i]])[0]

            Ea = exato - aprox
            if Ea < 0:
                Ea = Ea * (-1)
            Er = (Ea/exato) 
            soma_ea = soma_ea + Ea
            soma_er = soma_er + Er
        
        soma_30_ea = soma_30_ea + soma_ea/len(x3)
        soma_30_er = soma_30_er + soma_er/len(x3)

        
    texto = "Aprendiz "+ str(n)  +": ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:" + str(round(soma_30_er/30,4)) + " || ->criterion=friedman_mse  ||  ->Spliter: best || maxmax_depth: 10  || min_samples_leaf="+ str(min_S) +"  ||  max_features=None (default)  || max_leaf_nodes=" + str(max_l)+ "\n"
    return texto

start_time = time.time()
cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt'
erros = r'E:\IC\Interface_Grafica\Dados_verificacao\erros_arvoreD2.txt'
prec = 3
tmax = 4
tmin = 5
x, y, x7, y7, x3, y3 = prepara_matriz(cidade,tmax,4)

arq_e = open(erros, 'w')

arq_e.write(Aprendiz1(x7,y7,x3,y3,30))
arq_e.write(Aprendiz2(x7,y7,x3,y3,30))
arq_e.write(Aprendiz3(x7,y7,x3,y3,30))
#arq_e.write(Aprendiz4(x7,y7,x3,y3,30)) demora mt e os resultados não são os dos melhores
arq_e.write(Aprendiz5(x7,y7,x3,y3,30))
arq_e.write(Aprendiz6(x7,y7,x3,y3,30))
arq_e.write(Aprendiz7(x7,y7,x3,y3,30, 10, 7))
arq_e.write(Aprendiz7(x7,y7,x3,y3,30, 20, 8))
arq_e.write(Aprendiz7(x7,y7,x3,y3,30, 30, 9))
arq_e.write(Aprendiz7(x7,y7,x3,y3,30, 40, 10))
arq_e.write(Aprendiz7(x7,y7,x3,y3,30, 50, 11))
arq_e.write(Aprendiz7(x7,y7,x3,y3,30, 100, 12))
arq_e.write(Aprendiz7(x7,y7,x3,y3,30, 200, 13))
arq_e.write(Aprendiz7(x7,y7,x3,y3,30, 300, 14))
arq_e.write(Aprendiz7(x7,y7,x3,y3,30, 400, 15))
arq_e.write(Aprendiz7(x7,y7,x3,y3,30, 500, 16))
arq_e.write(Aprendiz8(x7,y7,x3,y3,30, 50, 17))
arq_e.write(Aprendiz8(x7,y7,x3,y3,30, 100, 18))
arq_e.write(Aprendiz9(x7,y7,x3,y3,30, 50, 19))
arq_e.write(Aprendiz10(x7,y7,x3,y3,30, 50, 20))
arq_e.write(Aprendiz11(x7,y7,x3,y3,30, 50, 21))
arq_e.write("\n")
arq_e.write(Aprendiz12(x7,y7,x3,y3,30, 50, 21, 5))
arq_e.write(Aprendiz12(x7,y7,x3,y3,30, 50, 22, 10))
arq_e.write(Aprendiz12(x7,y7,x3,y3,30, 50, 23, 15))
arq_e.write(Aprendiz12(x7,y7,x3,y3,30, 50, 24, 20))
arq_e.write(Aprendiz12(x7,y7,x3,y3,30, 50, 25, 30))
arq_e.write(Aprendiz12(x7,y7,x3,y3,30, 50, 26, 40))
arq_e.write(Aprendiz12(x7,y7,x3,y3,30, 50, 27, 50))
arq_e.close()
print("--- %s seconds ---" % (time.time() - start_time))
