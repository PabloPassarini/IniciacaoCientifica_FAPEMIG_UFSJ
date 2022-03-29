from sklearn import tree
import sklearn

# data ; indi 
lisa = 1
irregular = 0
maca = 1
laranja = 0

pomar = [[150, lisa], [130, lisa], [180, irregular], [160, irregular]]
resultado = [maca, maca, laranja, laranja]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(pomar, resultado)

peso = input("Entre com o preço: ")
superficie = input("Entre com a superficie: ")

if superficie == 'lisa':
    superficie = 1
else:
    superficie = 0

resultadoUsuario = clf.predict([[peso, superficie]])

if resultadoUsuario == 1:
    print("É uma maça")
else:
    print("É uma laranja")