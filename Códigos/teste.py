import csv, os
import pandas as pd

os.system('cls')

def get_data(diretorio):
    buff = open("buff.csv", 'w')
    arq = open(diretorio, 'r')
    a = arq.readlines()
    del a[0:10]
    
    for i in range(len(a)):
        buff.write(a[i])

    buff.close()

    print(pd.read_csv('buff.csv', sep=';'))
    arq.close()
target = r'E:\IC\Dados\TriangulacaoBH\BELOHORIZONTE.csv'   
get_data(target)