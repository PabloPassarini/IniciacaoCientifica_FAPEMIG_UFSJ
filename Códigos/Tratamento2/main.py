import numpy as np
def get_colunas(tipo, vetor):
    tipo = tipo[16:]
    vetor = vetor.split(';')
    del vetor[len(vetor)-1]

    if tipo[0] != 'A':
        coluna_prec = 3
        coluna_tmax = 4
        coluna_tmin = 6    
    else:
        coluna_prec = 1
        coluna_tmax = 4
        coluna_tmin = 6

    vet_c = [coluna_prec, coluna_tmax, coluna_tmin] #Lista com os index das colunas de cada indicador climatico desejado, de acordo com o tipo de estação do INMET
    return vet_c

def sem_limite_nan(lista):
    sem_l = list()
    for i in range(len(lista)):
        aux = list()
        for j in range(6):
            if lista[i][j] == 'null':
                aux.append(float('nan'))
            else:
                aux.append(float(lista[i][j]))
        sem_l.append(aux)
    return sem_l
    
def remover_null(lista):
    fim = list()
    for i in range(len(lista)):
        condicao = 0
        for j in range(0, len(lista[i])):
            if lista[i][j] == 'null' or lista[i][j] == '':
                condicao = 1
        if condicao == 0:
            aux = list()
            for k in range(len(lista[i])):
                aux.append(float(lista[i][k]))
            fim.append(aux)

    
    return fim

def limpar_data(diretorio):
    arq = open(diretorio, 'r')
    dados_brutos = list()
    
    for i in arq:
        texto = i.replace('\n', '')
        dados_brutos.append(texto)
    del dados_brutos[len(dados_brutos)-1]
    nome = dados_brutos[0][6:]
    latitude = dados_brutos[3][11:]
    
    colunas = get_colunas(dados_brutos[1], dados_brutos[10])
    dados_limpos = list()

    for i in range(11, len(dados_brutos)): #Fazendo uma lista com as datas e com os indicadores climáticos desejados
        aux = list()
        texto = dados_brutos[i].split(';')
        del texto[len(texto)-1]

        data = texto[0].split('-')
        aux.append(data[0])
        aux.append(data[1])
        aux.append(data[2])
        for j in colunas:
            aux.append(texto[j])
        dados_limpos.append(aux)
    
    return dados_limpos

def prepara_input(lista, ind):
    
    m70_x = list()
    m70_y = list()
    m30_x = list()
    m30_y = list()
    
    matriz_x = list()
    matriz_y = list()
    for i in range(len(lista)):
        aux = list()
        try:
            for j in range(5):
                aux.append(lista[i+j][0])
                aux.append(lista[i+j][1])
                aux.append(lista[i+j][2])
                aux.append(lista[i+j][ind])
            if len(aux) == 20:
                matriz_x.append(aux[:19])
                matriz_y.append(aux[10])
        except IndexError:
            pass
    #print(matriz_x[0])
    t = math.floor(len(matriz_x)*0.7)

    for i in range(len(matriz_x)):
        if i <= t:
            m70_x.append(matriz_x[i])
            m70_y.append(matriz_y[i])
        else:
            m30_x.append(matriz_x[i])
            m30_y.append(matriz_y[i])     

    return m70_x, m70_y, m30_x, m30_y

import os, math
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPRegressor

os.system('cls')
alvo_limpa = limpar_data('E:\IC\Dados\TriangulacaoBH\BELOHORIZONTE.csv')
alvo_nan = sem_limite_nan(alvo_limpa)


imp_mean = SimpleImputer(missing_values=float('nan'), strategy='mean')
SimpleImputer()
imp_mean.fit(alvo_nan)
teste = imp_mean.transform(alvo_nan)

alvo_sem_null = remover_null(alvo_limpa)


m70_x_a, m70_y_a, m30_x_a, m30_y_a = prepara_input(alvo_sem_null, 5)
m70_x_b, m70_y_b, m30_x_b, m30_y_b = prepara_input(alvo_nan, 5)


aprendiz_a = MLPRegressor()
aprendiz_a = aprendiz_a.fit(m70_x_a, m70_y_a)

soma_ea = soma_er = 0
for i in range(len(m30_x_a)):
    exato = m30_y_a[i]
    aprox = aprendiz_a.predict([m30_x_a[i]])[0]

    erro_abs = abs(exato - aprox)
    erro_rel = erro_abs/exato

    soma_ea += erro_abs
    soma_er += erro_rel



print("---->Dados sem valor null<----")
print("Erro abs.: {}  ||  Erro rel.: {}  ||  R2: {}".format(soma_ea/len(m30_x_a), soma_er/len(m30_x_a), aprendiz_a.score(m30_x_a, m30_y_a)))

'''

aprendiz_s = MLPRegressor()
aprendiz_s = aprendiz_s.fit(m70_x, m70_y)
soma_ea = soma_er = 0
for i in range(len(m30_x)):
    valor_exato = m30_y[i]
    valor_aprox = aprendiz_s.predict([m30_x[i]])[0]

    erro_abs = abs(valor_exato - valor_aprox)
    erro_rel = erro_abs/valor_aprox
    soma_ea += erro_abs
    soma_er += erro_rel

print("Erros (sem limite): {} {}".format(soma_ea/len(m30_x), soma_er/len(m30_x)))
print("R2 sem limite: {}".format(aprendiz_s.score(m30_x, m30_y)))


teste2 = remover_null(alvo_limpa)
c_m70_x = list()
c_m70_y = list()
c_m30_x = list()
c_m30_y = list()
t = math.floor(len(teste2)*0.7)

for i in range(len(teste2)):
    if i <= t:
        aux = list()
        for j in range(0,5):
            aux.append(teste2[i][j])
        c_m70_x.append(aux)
        c_m70_y.append(teste2[i][5])
    else:
        aux = list()
        for j in range(0,5):
            aux.append(teste2[i][j])
        c_m30_x.append(aux)
        c_m30_y.append(teste2[i][5])

aprendiz_sem_null = MLPRegressor()
aprendiz_sem_null = aprendiz_sem_null.fit(c_m70_x, c_m70_y)

soma_ea = soma_er = 0
for i in range(len(c_m30_x)):
    valor_exato = m30_y[i]
    valor_aprox = aprendiz_sem_null.predict([c_m30_x[i]])[0]

    erro_abs = abs(valor_exato - valor_aprox)
    erro_rel = erro_abs/valor_aprox
    soma_ea += erro_abs
    soma_er += erro_rel

print("\n\nErros (sem null): {} {}".format(soma_ea/len(c_m30_x), soma_er/len(c_m30_x)))
print("R2 sem null: {}".format(aprendiz_sem_null.score(c_m30_x, c_m30_y)))


'''