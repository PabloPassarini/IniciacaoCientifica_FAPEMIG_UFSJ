import csv, os

os.system('cls') # Limpando o terminal


def Obter_dados(diretorio):
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


targetData = Obter_dados(r'E:\IC\Dados\TriangulacaoBH\BELOHORIZONTE.csv')
neighorAData = Obter_dados(r'E:\IC\Dados\TriangulacaoBH\FLORESTAL.csv')
neighorBData = Obter_dados(r'E:\IC\Dados\TriangulacaoBH\IBIRITE.csv')
neighorCData = Obter_dados(r'E:\IC\Dados\TriangulacaoBH\SETELAGOAS.csv')

soma = (len(targetData) + len(neighorAData) + len(neighorBData) + len(neighorCData))*4
print(soma)