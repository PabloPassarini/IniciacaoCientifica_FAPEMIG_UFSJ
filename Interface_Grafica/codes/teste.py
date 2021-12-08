local = r'E:\IC\Interface_Grafica\Dados_verificacao\dadoscomum.csv'

arq = open(local, 'r')
a = list()
for i in arq:
    a.append(i)

print(a[len(a)-1])