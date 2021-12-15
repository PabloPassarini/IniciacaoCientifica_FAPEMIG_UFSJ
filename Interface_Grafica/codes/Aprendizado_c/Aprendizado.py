from sklearn import tree
import os
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


def Aprendiz_m1(n,x7, y7, x3, y3, n_t, cri, spli, max_d, min_s, max_f,  max_l):
    soma_30_ea = 0
    soma_30_er = 0

    for j in range(n_t):
        clf = tree.DecisionTreeRegressor(criterion=cri, splitter=spli, max_depth=max_d, min_samples_leaf=min_s, max_features=max_f, max_leaf_nodes=max_l)
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

    pts = round((((soma_30_er/30)*100) - 100)* (-1),2)

    texto = "Aprendiz "+ str(n)  +" " + str(pts) + "pts:  ->Erro Absoluto:" + str(round(soma_30_ea/30,4)) + " || ->Erro Relativo:"  + str(round(soma_30_er/30,4)) + " || ->Criterion: " + cri + "  ||  ->Spliter:  " + spli + "  ||  ->Max_depth: " + str(max_d) + "  ||  ->Min_samples_leaf: " + str(min_s) + "  ||  ->Max_features: " + str(max_f) + "  ||  ->Max_leaf_nodes: " + str(max_l) + "\n"
    return texto














cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt'
erros = r'E:\IC\Interface_Grafica\Dados_verificacao\erros_arvoreD2.txt'
prec = 3
tmax = 4
tmin = 5

numeros_teste = 30
x, y, x7, y7, x3, y3 = prepara_matriz(cidade,tmax,4)

arq_e = open(erros, 'w')
arq_e.write("----- Grupo 1 -----\n")
#! n,x7, y7, x3, y3, n_t, cri, spli, max_d, min_s, max_f,  max_l
arq_e.write(Aprendiz_m1(1, x7, y7, x3, y3, numeros_teste, "squared_error", "best", None, 1, None, None))
arq_e.write(Aprendiz_m1(2, x7, y7, x3, y3, numeros_teste, "friedman_mse", "best", None, 1, None, None))
arq_e.write(Aprendiz_m1(3, x7, y7, x3, y3, numeros_teste, "poisson", "best", None, 1, None, None))

arq_e.write("\n----- Grupo 2 -----\n")

arq_e.write(Aprendiz_m1(4, x7, y7, x3, y3, numeros_teste, "squared_error", "random", None, 1, None, None))
arq_e.write(Aprendiz_m1(5, x7, y7, x3, y3, numeros_teste, "friedman_mse", "random", None, 1, None, None))
arq_e.write(Aprendiz_m1(6, x7, y7, x3, y3, numeros_teste, "poisson", "random", None, 1, None, None))

arq_e.write("\n----- Grupo 3 -----\n")
cont = 7

for i in range(10,40,10):
    arq_e.write(Aprendiz_m1(cont, x7, y7, x3, y3, numeros_teste, "squared_error", "best", i, 1, None, None))
    cont += 1

for i in range(10,40,10):
    arq_e.write(Aprendiz_m1(cont, x7, y7, x3, y3, numeros_teste, "friedman_mse", "best", i, 1, None, None))
    cont += 1

for i in range(10,40,10):
    arq_e.write(Aprendiz_m1(cont, x7, y7, x3, y3, numeros_teste, "poisson", "best", i, 1, None, None))
    cont += 1


for i in range(10,40,10):
    arq_e.write(Aprendiz_m1(cont, x7, y7, x3, y3, numeros_teste, "squared_error", "random", i, 1, None, None))
    cont += 1

for i in range(10,40,10):
    arq_e.write(Aprendiz_m1(cont, x7, y7, x3, y3, numeros_teste, "friedman_mse", "random", i, 1, None, None))
    cont += 1

for i in range(10,40,10):
    arq_e.write(Aprendiz_m1(cont, x7, y7, x3, y3, numeros_teste, "poisson", "random", i, 1, None, None))
    cont += 1

arq_e.write("\n----- Grupo 4 -----\n")

arq_e.write(Aprendiz_m1(cont, x7, y7, x3, y3, numeros_teste, "squared_error", "random", 10, 50, None, None))
arq_e.write(Aprendiz_m1(cont+1, x7, y7, x3, y3, numeros_teste, "squared_error", "random", 10, 100, None, None))
arq_e.write(Aprendiz_m1(cont+2, x7, y7, x3, y3, numeros_teste, "friedman_mse", "random", 10, 50, None, None))
arq_e.write(Aprendiz_m1(cont+3, x7, y7, x3, y3, numeros_teste, "friedman_mse", "random", 10, 100, None, None))
arq_e.write(Aprendiz_m1(cont+4, x7, y7, x3, y3, numeros_teste, "poisson", "random", 10, 50, None, None))
arq_e.write(Aprendiz_m1(cont+5, x7, y7, x3, y3, numeros_teste, "poisson", "random", 10, 100, None, None))

arq_e.write("\n\n")

arq_e.write(Aprendiz_m1(cont+7, x7, y7, x3, y3, numeros_teste, "squared_error", "best", 10, 50, None, None))
arq_e.write(Aprendiz_m1(cont+8, x7, y7, x3, y3, numeros_teste, "squared_error", "best", 10, 100, None, None))
arq_e.write(Aprendiz_m1(cont+9, x7, y7, x3, y3, numeros_teste, "friedman_mse", "best", 10, 50, None, None))
arq_e.write(Aprendiz_m1(cont+10, x7, y7, x3, y3, numeros_teste, "friedman_mse", "best", 10, 100, None, None))
arq_e.write(Aprendiz_m1(cont+11, x7, y7, x3, y3, numeros_teste, "poisson", "best", 10, 50, None, None))
arq_e.write(Aprendiz_m1(cont+12, x7, y7, x3, y3, numeros_teste, "poisson", "best", 10, 100, None, None))



arq_e.write("\n----- Grupo 5 -----\n")

arq_e.write(Aprendiz_m1(cont+13, x7, y7, x3, y3, numeros_teste, "squared_error", "random", 10, 50, "auto", None))
arq_e.write(Aprendiz_m1(cont+14, x7, y7, x3, y3, numeros_teste, "squared_error", "random", 10, 100, "auto", None))
arq_e.write(Aprendiz_m1(cont+15, x7, y7, x3, y3, numeros_teste, "friedman_mse", "random", 10, 50, "auto", None))
arq_e.write(Aprendiz_m1(cont+16, x7, y7, x3, y3, numeros_teste, "friedman_mse", "random", 10, 100, "auto", None))
arq_e.write(Aprendiz_m1(cont+18, x7, y7, x3, y3, numeros_teste, "poisson", "random", 10, 50, "auto", None))
arq_e.write(Aprendiz_m1(cont+19, x7, y7, x3, y3, numeros_teste, "poisson", "random", 10, 100, "auto", None))

arq_e.write(Aprendiz_m1(cont+20, x7, y7, x3, y3, numeros_teste, "squared_error", "best", 10, 50, "auto", None))
arq_e.write(Aprendiz_m1(cont+21, x7, y7, x3, y3, numeros_teste, "squared_error", "best", 10, 100, "auto", None))
arq_e.write(Aprendiz_m1(cont+22, x7, y7, x3, y3, numeros_teste, "friedman_mse", "best", 10, 50, "auto", None))
arq_e.write(Aprendiz_m1(cont+23, x7, y7, x3, y3, numeros_teste, "friedman_mse", "best", 10, 100, "auto", None))
arq_e.write(Aprendiz_m1(cont+24, x7, y7, x3, y3, numeros_teste, "poisson", "best", 10, 50, "auto", None))
arq_e.write(Aprendiz_m1(cont+25, x7, y7, x3, y3, numeros_teste, "poisson", "best", 10, 100, "auto", None))

arq_e.write("\n")

arq_e.write(Aprendiz_m1(cont+26, x7, y7, x3, y3, numeros_teste, "squared_error", "random", 10, 50, "log2", None))
arq_e.write(Aprendiz_m1(cont+27, x7, y7, x3, y3, numeros_teste, "squared_error", "random", 10, 100, "log2", None))
arq_e.write(Aprendiz_m1(cont+28, x7, y7, x3, y3, numeros_teste, "friedman_mse", "random", 10, 50, "log2", None))
arq_e.write(Aprendiz_m1(cont+29, x7, y7, x3, y3, numeros_teste, "friedman_mse", "random", 10, 100, "log2", None))
arq_e.write(Aprendiz_m1(cont+30, x7, y7, x3, y3, numeros_teste, "poisson", "random", 10, 50, "log2", None))
arq_e.write(Aprendiz_m1(cont+31, x7, y7, x3, y3, numeros_teste, "poisson", "random", 10, 100, "log2", None))

arq_e.write(Aprendiz_m1(cont+32, x7, y7, x3, y3, numeros_teste, "squared_error", "best", 10, 50, "log2", None))
arq_e.write(Aprendiz_m1(cont+33, x7, y7, x3, y3, numeros_teste, "squared_error", "best", 10, 100, "log2", None))
arq_e.write(Aprendiz_m1(cont+34, x7, y7, x3, y3, numeros_teste, "friedman_mse", "best", 10, 50, "log2", None))
arq_e.write(Aprendiz_m1(cont+35, x7, y7, x3, y3, numeros_teste, "friedman_mse", "best", 10, 100, "log2", None))
arq_e.write(Aprendiz_m1(cont+36, x7, y7, x3, y3, numeros_teste, "poisson", "best", 10, 50, "log2", None))
arq_e.write(Aprendiz_m1(cont+37, x7, y7, x3, y3, numeros_teste, "poisson", "best", 10, 100, "log2", None))

arq_e.write("\n")

arq_e.write(Aprendiz_m1(cont+38, x7, y7, x3, y3, numeros_teste, "squared_error", "random", 10, 50, "sqrt", None))
arq_e.write(Aprendiz_m1(cont+39, x7, y7, x3, y3, numeros_teste, "squared_error", "random", 10, 100, "sqrt", None))
arq_e.write(Aprendiz_m1(cont+40, x7, y7, x3, y3, numeros_teste, "friedman_mse", "random", 10, 50, "sqrt", None))
arq_e.write(Aprendiz_m1(cont+41, x7, y7, x3, y3, numeros_teste, "friedman_mse", "random", 10, 100, "sqrt", None))
arq_e.write(Aprendiz_m1(cont+42, x7, y7, x3, y3, numeros_teste, "poisson", "random", 10, 50, "sqrt", None))
arq_e.write(Aprendiz_m1(cont+43, x7, y7, x3, y3, numeros_teste, "poisson", "random", 10, 100, "sqrt", None))

arq_e.write(Aprendiz_m1(cont+44, x7, y7, x3, y3, numeros_teste, "squared_error", "best", 10, 50, "sqrt", None))
arq_e.write(Aprendiz_m1(cont+45, x7, y7, x3, y3, numeros_teste, "squared_error", "best", 10, 100, "sqrt", None))
arq_e.write(Aprendiz_m1(cont+46, x7, y7, x3, y3, numeros_teste, "friedman_mse", "best", 10, 50, "sqrt", None))
arq_e.write(Aprendiz_m1(cont+47, x7, y7, x3, y3, numeros_teste, "friedman_mse", "best", 10, 100, "sqrt", None))
arq_e.write(Aprendiz_m1(cont+48, x7, y7, x3, y3, numeros_teste, "poisson", "best", 10, 50, "sqrt", None))
arq_e.write(Aprendiz_m1(cont+49, x7, y7, x3, y3, numeros_teste, "poisson", "best", 10, 100, "sqrt", None))


arq_e.close()
