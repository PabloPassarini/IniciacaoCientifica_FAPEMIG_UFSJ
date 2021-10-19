import csv, os
os.system('cls') #Limpando os dados do terminal

dados = list()
aux = list()
datas = list()
medicoes = list()
with open(r'E:\IC\Dados\TriangulacaoBH\BELOHORIZONTE.csv') as arq:
    reader = csv.reader(arq)
    for linha in reader:
        dados.append(linha)

del dados[len(dados)-1] #Retirando a ultima linha do arquivo .csv (da para tirar no propio arquivo, mas se for trabalhar com vários arquivos, o trabalho vai ser massante)
del(dados[0:11]) #Remove o cabeçalho do arquivo

for i in range(len(dados)):
    dados[i] = str(dados[i]).strip('[')
    dados[i] = str(dados[i]).strip(']')
    dados[i] = str(dados[i]).strip("'")
    dados[i] = str(dados[i]).split(';')
    del(dados[i][9])

for i in range(len(dados)):
    datas.append(str(dados[i][0]).split('-')) #Lista dedicada para armazenar as datas no formato: [ano,mes,dia]
    medicoes.append(dados[i][1:9]) #Lista dedicada, somente para as medições

qtd_faltantes = 0
total = 0
ind = 0

janela = list()
ano_start = datas[0][0]

for i in range(len(datas)):
    if ano_start == datas[i][0]:
        for j in range(8):
            if medicoes[i][j] == 'null':
                qtd_faltantes = qtd_faltantes + 1
            
            total = total + 1 
    else:
        buff = str(ano_start) + ' ' + str(qtd_faltantes) + ' ' + str(total)
        janela.append(buff)
        ano_start = datas[i][0] 
        qtd_faltantes = 0
        total = 0

for i in janela:
    print(i)


