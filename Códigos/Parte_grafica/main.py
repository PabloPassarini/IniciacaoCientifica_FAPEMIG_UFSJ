from tkinter import *
from tkinter import filedialog as dlg
from tkinter import Canvas
from tratar_dados import Data_trat
import csv, os
os.system("cls")

def procura_arq(entry_txt):
    path = dlg.askopenfilename()
    entry_txt.set(path)

def escolhe_pasta(entry_txt):
    path = dlg.askdirectory()
    entry_txt.set(path)

def tratar():
    a = Data_trat(cid_target.get(), cid_viz1.get(),cid_viz2.get(), cid_viz3.get(), local_download.get())
    a.get_data_trada()
janela = Tk()
janela.state("zoomed")



cid_target = StringVar()
Label(janela, text='Cidade Alvo:', font='Arial 14 bold').place(x=20, y=20)
ent_arq_tg = Entry(janela, textvariable=cid_target, font='Arial 14', width=30)
ent_arq_tg.place(x=150, y=20)
btn_arq_tg = Button(janela, font='Arial 11', text="...", width=5, bg='lightgray', command=lambda: procura_arq(cid_target))
btn_arq_tg.place(x=500, y=19)

cid_viz1 = StringVar()
Label(janela, text="Cid.Vizinha1:", font='Arial 14 bold').place(x=20, y=60)
ent_arq_v1 = Entry(janela, textvariable=cid_viz1, font='Arial 14', width=30)
ent_arq_v1.place(x=150, y=60)
btn_arq_v1 = Button(janela, font='Arial 11', text="...", width=5, bg='lightgray', command=lambda: procura_arq(cid_viz1))
btn_arq_v1.place(x=500, y=59)

cid_viz2 = StringVar()
Label(janela, text="Cid.Vizinha2:", font='Arial 14 bold').place(x=20, y=100)
ent_arq_v2 = Entry(janela, textvariable=cid_viz2, font='Arial 14', width=30)
ent_arq_v2.place(x=150, y=100)
btn_arq_v2 = Button(janela, font='Arial 11', text="...", width=5, bg='lightgray', command=lambda: procura_arq(cid_viz2))
btn_arq_v2.place(x=500, y=99)

cid_viz3 = StringVar()
Label(janela, text="Cid.Vizinha3:", font='Arial 14 bold').place(x=20, y=140)
ent_arq_v3 = Entry(janela, textvariable=cid_viz3, font='Arial 14', width=30)
ent_arq_v3.place(x=150, y=140)
btn_arq_v3 = Button(janela, font='Arial 11', text="...", width=5, bg='lightgray', command=lambda: procura_arq(cid_viz3))
btn_arq_v3.place(x=500, y=139)


local_download = StringVar()
Label(janela, text="Salvar em:", font='Arial 14 bold').place(x=20, y=180)
ent_downarq = Entry(janela, textvariable=local_download, font='Arial 14', width=30)
ent_downarq.place(x=150, y=180)
btn_downarq= Button(janela, font='Arial 11', text="...", width=5, bg='lightgray', command=lambda: escolhe_pasta(local_download))
btn_downarq.place(x=500, y=179)

btn_salvar = Button(janela, text="Salvar", font='Arial 14 bold', width=44, bg='green', fg='white', command=tratar)
btn_salvar.place(x=20, y=220)
"""

with open(str(path)) as arq:
        reader = csv.reader(arq)
        for line in reader:
            print(line)
 """           
janela.mainloop()