from tkinter import *
from tkinter import filedialog as dlg
from tkinter import Canvas
from tratar_dados import Data_trat
import csv, os, threading
os.system("cls")

def procura_arq(entry_txt):
    path = dlg.askopenfilename()
    entry_txt.set(path)

def escolhe_pasta(entry_txt):
    path = dlg.askdirectory()
    entry_txt.set(path)

def tratar():
    a = Data_trat(cid_target.get(), cid_viz1.get(),cid_viz2.get(), cid_viz3.get(), local_download.get())
    arq = open("locais_salvos.txt", 'w')
    arq.write(local_download.get())
    arq.close()
    a.get_data_trada()

    
janela = Tk()
janela.state("zoomed")
janela.configure(bg='lightgray')


cid_target = StringVar()
Label(janela, text='Cidade Alvo:', font='Arial 12 bold',bg='lightgray').place(x=20, y=20)
ent_arq_tg = Entry(janela, textvariable=cid_target, font='Arial 12', width=50)
ent_arq_tg.place(x=20, y=45)
btn_arq_tg = Button(janela, font='Arial 10 bold', text="...", width=5, fg='white',bg='gray', command=lambda: procura_arq(cid_target))
btn_arq_tg.place(x=480, y=43)


cid_viz1 = StringVar()
Label(janela, text="Cididade Vizinha 1:", font='Arial 12 bold',bg='lightgray').place(x=20, y=80)
ent_arq_v1 = Entry(janela, textvariable=cid_viz1, font='Arial 12', width=50)
ent_arq_v1.place(x=20, y=105)
btn_arq_v1 = Button(janela, font='Arial 10 bold', text="...", width=5, fg='white',bg='gray', command=lambda: procura_arq(cid_viz1))
btn_arq_v1.place(x=480, y=103)

cid_viz2 = StringVar()
Label(janela, text="Cididade Vizinha 2:", font='Arial 12 bold', bg='lightgray').place(x=20, y=140)
ent_arq_v2 = Entry(janela, textvariable=cid_viz2, font='Arial 12', width=50)
ent_arq_v2.place(x=20, y=165)
btn_arq_v2 = Button(janela, font='Arial 10 bold', text="...", width=5, fg='white',bg='gray', command=lambda: procura_arq(cid_viz2))
btn_arq_v2.place(x=480, y=163)

cid_viz3 = StringVar()
Label(janela, text="Cidade Vizinha 3:", font='Arial 12 bold', bg='lightgray').place(x=20, y=200)
ent_arq_v3 = Entry(janela, textvariable=cid_viz3, font='Arial 12', width=50)
ent_arq_v3.place(x=20, y=225)
btn_arq_v3 = Button(janela, font='Arial 10 bold', text="...", width=5, fg='white',bg='gray', command=lambda: procura_arq(cid_viz3))
btn_arq_v3.place(x=480, y=223)


local_download = StringVar()
Label(janela, text="Salvar em:", font='Arial 12 bold', bg='lightgray').place(x=20, y=260)
ent_downarq = Entry(janela, textvariable=local_download, font='Arial 12', width=50)
ent_downarq.place(x=20, y=285)
btn_downarq= Button(janela, font='Arial 10 bold', text="...", width=5, fg='white', bg='gray', command=lambda: escolhe_pasta(local_download))
btn_downarq.place(x=480, y=283)

btn_salvar = Button(janela, text="Salvar", font='Arial 12 bold', width=50, bg='green', fg='white', command=tratar)
btn_salvar.place(x=20, y=320)

janela.mainloop()