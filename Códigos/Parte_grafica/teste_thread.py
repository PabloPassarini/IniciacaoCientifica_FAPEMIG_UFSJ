import threading

def tarefa1():
    for x in range(10):
        print("Tarefa1")

def tarefa2():
    for y in range(10):
        print("Tarefa2")


threading.Thread(target=tarefa1).start()
tarefa2()