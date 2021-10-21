import csv, os

os.system('cls') # Limpando o terminal


def get_data(diretorio): #Função para a aquisição e tratamento dos dados
    aux = list()
    with open(diretorio) as arq:
        reader = csv.reader(arq)
        for line in reader:
            aux.append(line) #Cada linha do arquivo é uma lista, então se colocarmos essa lista em outra lista, teremos uma matriz, nesse caso a matriz se chama aux
    
    del aux[len(aux)-1]  #Remove a ultima linha em branco do arquivo, da pra fazer isso manualmente, mas caso o usuario trabalhe com inumeros arquivos, remover a ultima linha de cada arquivo pode ser um trabalho massante 
    del aux[0:11]        #Remove o cabeçalho do arquivo .csv
    
    for i in range(len(aux)):   
        #Removendo os caracteres desenecessários
        aux[i] = str(aux[i]).strip('[')     
        aux[i] = str(aux[i]).strip(']')
        aux[i] = str(aux[i]).strip("'")
        aux[i] = str(aux[i]).split(';')

        del aux[i][9] #Remove a ultima coluna, pois ela fica vazia, ('')

        #Remove as outras colunas, deixando somente a de data, precipitação, temperatura max e temperatura min
        del aux[i][1:3]
        del aux[i][3]
        del aux[i][4:6]

    ''' -> Para visualizar os dados salvos <-
    for i in aux:
        print(i)
    '''
    real = list() #Lista/Matriz final

    #Removendo todas as linhas que possuem o valor null
    for i in range(len(aux)):
        condicao = 0
        for j in range(1,4):
            if aux[i][j] == 'null':
                condicao = 1
        
        if condicao == 0:
            real.append(aux[i])


    return real #Retorna a lista com os dados tratados, onde na lista em cada linha temos: [data, precipitação, temperatura max, temperatura min]

def get_coordinates(diretorio): #Função para obter as coordenadas de cada cidade
    aux = list()
    with open(diretorio) as arq:
        reader = csv.reader(arq)
        for i in reader:
            aux.append(i)
        
    #Tratamento de dados
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
    return aux #Retorna um 'vetor' com os dados: [nome da estação, latitude, longitude, altitude]

def normaliza_dados(lista): #Função que retorna a matriz com os dados normalizados
    menor = float(lista[0][1])
    maior = menor
    aux = list()
    dadosn = list()
    
    for i in range(len(lista)): #Encontrar o maior e o menor valor de uma coluna especifica 
        valor = float(lista[i][1])
        
        if valor < menor:
            menor = valor
        if valor > maior:
            maior = valor
    
    for i in range(len(lista)):
        dado = ((float(lista[i][1])-menor)/(maior - menor))*0.6 + 0.2
        aux.clear()             #'Resetando' a lista aux
        aux.append(lista[i][0]) #Inserindo a data numa lista aux
        aux.append(dado)        #Inserindo o dado normalizado na lista aux

        dadosn.append(aux)      #Inserindo a lista aux dentro da lista dadosn (que em outra linguem, eu estaria criando uma nova linha em uma matriz)

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

normaliza_dados(targetData)