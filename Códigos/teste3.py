

arq = open('C:/Users/pablo/Desktop/alvo_limpa.txt', 'r')
a = list()
b = list()
aux = []
for i in arq:
    i = i.strip()
    i = i.replace("'","")
    i = i.replace(' ','')

    a.append(i)

print(a[0].split(','))



