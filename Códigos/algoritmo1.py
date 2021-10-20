import csv, os

os.system('cls') # Limpando o terminal


def get_data(diretorio):
    aux = list()
    with open(diretorio) as arq:
        reader = csv.reader(arq)
        for line in reader:
            aux.append(line)
    
    del aux[len(aux)-1]
    del aux[0:11]
    
    for i in range(len(aux)):
        aux[i] = str(aux[i]).strip('[')
        aux[i] = str(aux[i]).strip(']')
        aux[i] = str(aux[i]).strip("'")
        aux[i] = str(aux[i]).split(';')
        del aux[i][9] #Tira o valor da posição 9 de cada vetor (o valor é '')
        # Para deixa salvo apenas os dados de precipitação, temperatura max e temperatura minima
        del aux[i][1:3]
        del aux[i][3]
        del aux[i][4:6]

    ''' -> Para visualizar os dados salvos <-
    for i in aux:
        print(i)
    '''
    real = list()

    for i in range(len(aux)):
        condicao = 0
        for j in range(1,4):
            if aux[i][j] == 'null':
                condicao = 1
        
        if condicao == 0:
            real.append(aux[i])


    return real #Retorna a lista com os dados tratados, onde na lista em cada linha temos: [data, precipitação, temperatura max, temperatura min]

def get_coordinates(diretorio):
    aux = list()
    with open(diretorio) as arq:
        reader = csv.reader(arq)
        for i in reader:
            aux.append(i)
        
    del aux[10:]

    estacao = str(aux[0]).split(':')
    estacao = estacao[1].strip(']')
    estacao = (estacao.strip("'")).strip()

    latitude = str(aux[2]).split(':')
    latitude = latitude[1].strip(']')
    latitude = (latitude.strip("'")).strip()

    longitude = str(aux[3]).split(':')
    longitude = longitude[1].strip(']')
    longitude = (longitude.strip("'")).strip()

    altitude = str(aux[4]).split(':')
    altitude = altitude[1].strip(']')
    altitude = (altitude.strip("'")).strip()

    aux.clear()

    aux.append(estacao)
    aux.append(latitude)
    aux.append(longitude)
    aux.append(altitude)
    return aux


target = r'E:\IC\Dados\TriangulacaoBH\BELOHORIZONTE.csv'
neighorA = r'E:\IC\Dados\TriangulacaoBH\FLORESTAL.csv'
neighorB = r'E:\IC\Dados\TriangulacaoBH\IBIRITE.csv'
neighorC = r'E:\IC\Dados\TriangulacaoBH\SETELAGOAS.csv'

targetData = get_data(target)
neighorAData = get_data(neighorA)
neighorBData = get_data(neighorB)
neighorCData = get_data(neighorC)


coord_target = get_coordinates(target)
coord_neighorA = get_coordinates(neighorA)
coord_neighorB = get_coordinates(neighorB)
coord_neighorC = get_coordinates(neighorC)

