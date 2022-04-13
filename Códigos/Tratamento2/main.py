import numpy as np
from sklearn.metrics import median_absolute_error
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
alvo_nan2 = teste.tolist()

m70_x_a, m70_y_a, m30_x_a, m30_y_a = prepara_input(alvo_sem_null, 5)
m70_x_b, m70_y_b, m30_x_b, m30_y_b = prepara_input(alvo_nan2, 5)

n_teste = 30
media_ea = media_er = 0
print("---->Dados sem valor null<----")
for j in range(n_teste):
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

    media_ea += soma_ea/len(m30_x_a)
    media_er += soma_er/len(m30_x_a)
    print(" {}->Erro abs.: {:.6f}  ||  Erro rel.: {:.6f}  ||  R2: {:.6f}".format(j+1, soma_ea/len(m30_x_a), soma_er/len(m30_x_a), aprendiz_a.score(m30_x_a, m30_y_a)))


print("Média das 30 exec ->Erro abs.: {:.6f}  ||  Erro rel.: {:.6f}  ||  R2: {:.6f}".format(media_ea/n_teste, media_er/n_teste, aprendiz_a.score(m30_x_a, m30_y_a)))


print("\n\n---->Dados com valores null substituidos sem limites<----")
media_ea = media_er = 0
for j in range(n_teste):
    aprendiz_b = MLPRegressor()
    aprendiz_b = aprendiz_b.fit(m70_x_b, m70_y_b)
    soma_ea = soma_er = 0

    for i in range(len(m30_x_b)):
        exato = m30_y_b[i]
        aprox = aprendiz_b.predict([m30_x_b[i]])[0]

        erro_abs = abs(exato - aprox)
        erro_rel = erro_abs/exato

        soma_ea += erro_abs
        soma_er += erro_rel
    
    media_ea += soma_ea/len(m30_x_b)
    media_er += soma_er/len(m30_x_b)
    print(" {}->Erro abs.: {:.6f}  ||  Erro rel.: {:.6f}  ||  R2: {}".format(j+1, soma_ea/len(m30_x_b), soma_er/len(m30_x_b), aprendiz_b.score(m30_x_b, m30_y_b)))

print("Média das 30 exec ->Erro abs.: {:.6f}  ||  Erro rel.: {:.6f}  ||  R2: {:.6f}".format(media_ea/n_teste, media_er/n_teste, aprendiz_b.score(m30_x_b, m30_y_b)))