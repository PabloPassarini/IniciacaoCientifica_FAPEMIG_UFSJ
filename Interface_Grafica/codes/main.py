from tkinter import *
from tkinter import filedialog as dlg
from tkinter import messagebox as msg
from tkinter import ttk
from tratar import Tratamento
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import datetime as dt
import os
import matplotlib.dates as mdates
import matplotlib.ticker as plticker
os.system("cls")

fundo = '#4F4F4F' #? Cor de fundo da tela
fun_b = '#3CB371' #? Cor de fundo dos botoes
fun_ap = '#9C444C'
fun_alt = '#C99418'
class Selecionar_Arquivos_win(Toplevel):
    def __init__(self, master=None):
        def procura_arq(entry_txt):
            path = dlg.askopenfilename()
            entry_txt.set(path)

        def escolhe_pasta(entry_txt):
            path = dlg.askdirectory()
            entry_txt.set(path)

        def tratar(alvo, vA, vB, vC, download):
            
            datat = Tratamento() #* Criando um objeto que tem como atributos os endereços dos arquivos
            datat.alvo = alvo
            datat.vizinhaA = vA
            datat.vizinhaB = vB
            datat.vizinhaC = vC
            datat.download = download
            datat.get_data_trada()
            msg.showinfo(title="Sucesso!", message="Arquivos Selecionados com sucesso!")
            Toplevel.destroy(self)

        Toplevel.__init__(self, master=master)

        self.title('Selecionar arquivos')
        self.geometry("500x370")
        self.configure(background=fundo)


        Label(self, text='SELECIONAR ARQUIVOS', font='Arial 18 bold', fg='white',bg=fundo).place(x=110, y=10)

        dir_alvo = StringVar()
        Label(self, text="Cidade Alvo:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=50)   
        Entry(self, textvariable=dir_alvo, font='Arial 12', width=45).place(x=20, y=75)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(dir_alvo)).place(x=440, y=73)

        dir_vA = StringVar()
        Label(self, text="Cidade vizinha A:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)   
        Entry(self, textvariable=dir_vA, font='Arial 12', width=45).place(x=20, y=125)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(dir_vA)).place(x=440, y=123)

        dir_vB = StringVar()
        Label(self, text="Cidade vizinha B:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=150)   
        Entry(self, textvariable=dir_vB, font='Arial 12', width=45).place(x=20, y=175)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(dir_vB)).place(x=440, y=173)

        dir_vC = StringVar()
        Label(self, text="Cidade vizinha C:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=200)   
        Entry(self, textvariable=dir_vC, font='Arial 12', width=45).place(x=20, y=225)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(dir_vC)).place(x=440, y=223)

        dir_save = StringVar()
        Label(self, text="Local para salvar os dados tratados:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=250)
        Entry(self, textvariable=dir_save, font='Arial 12', width=45).place(x=20, y=275)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: escolhe_pasta(dir_save)).place(x=440, y=273)

        #Todo: Para Agilizar os testes
        dir_alvo.set('E:/IC/Dados/TriangulacaoBH/BELOHORIZONTE.csv')
        dir_vA.set('E:/IC/Dados/TriangulacaoBH/FLORESTAL.csv')
        dir_vB.set('E:/IC/Dados/TriangulacaoBH/IBIRITE.csv')
        dir_vC.set('E:/IC/Dados/TriangulacaoBH/SETELAGOAS.csv')
        dir_save.set('E:/IC/Interface_Grafica/Dados_verificacao')

        Button(self, text='Prosseguir', font='Arial 12 bold', fg='white', bg=fun_b, width=45, command=lambda: tratar(dir_alvo.get(), dir_vA.get(), dir_vB.get(), dir_vC.get(), dir_save.get())).place(x=21, y=320)


class Aprendizado_Marquina(Toplevel):
    def __init__(self, master=None):



        Toplevel.__init__(self, master=master)
        self.title('Aprendizado de máquina')
        self.geometry("800x800")
        self.configure(background=fundo)
class Principal(Frame):
    def open_sa(self): #* sa = Selecionar Arquivos
        window = Selecionar_Arquivos_win()
        window.mainloop()

    def open_apr(self): 
        window = Aprendizado_Marquina()
        window.mainloop()
    
    def get_col(self):
        if self.num_enf.get() == "Precipitação":
            y_name = "Precipitação (mm)"
            col = 3
        elif self.num_enf.get() == "Temperatura máxima":
            col = 4
            y_name = "Temperatura (°C)"
        elif self.num_enf.get() == "Temperatura mínima":
            y_name = "Temperatura (°C)"
            col = 5
        return y_name, col

    def graficos_comum(self):
        my_data = Tratamento()
        data_ana = my_data.retorna_arq(self.num.get())
        
        self.gera_range()

        nome_y, col = self.get_col()

        eixo_x = list()
        if self.num.get() == 'Dados comum':
            eixo_y1 = list()
            eixo_y2 = list()
            eixo_y3 = list()
            eixo_y4 = list()
            util, tar,t_va, t_vb, t_vc = my_data.get_qtd()
            eixo_y_bar = [util, tar,t_va, t_vb, t_vc]
            eixo_x_bar = ['Comum', 'Alvo','Total vA', 'Total vB', 'Total vC']
        else:
            eixo_y = list()

        dados_lb = list()
        for i in data_ana:
            dados_lb.append(i)

            ano = str(i[0])
            mes = str(i[1])
            dia = str(i[2])
            text_data = mes + '/' + dia + '/' + ano
            eixo_x.append(dt.datetime.strptime(text_data,"%m/%d/%Y").date())

            if self.num.get() == 'Dados comum':
                eixo_y1.append(float(i[col]))
                eixo_y2.append(float(i[col+3]))
                eixo_y3.append(float(i[col+6]))
                eixo_y4.append(float(i[col+9]))
            else:
                eixo_y.append(float(i[col]))
        
        self.caixad_var.set(dados_lb)

        fig = Figure(figsize=(13,9.5), dpi=100)
        

        if self.num.get() == 'Dados comum':
            plot1 = fig.add_subplot(321)
            plot2 = fig.add_subplot(322)
            plot3 = fig.add_subplot(323)
            plot4 = fig.add_subplot(324)
            plot5 = fig.add_subplot(325)
            plot6 = fig.add_subplot(326)
            plot1.plot(eixo_x, eixo_y1, label="Alvo")
            plot2.plot(eixo_x, eixo_y2, label="Viz A", color="red")
            plot3.plot(eixo_x, eixo_y3, label="Viz B", color='green')
            plot4.plot(eixo_x, eixo_y4, label="Viz C", color='orange')
            plot5.scatter(eixo_x, eixo_y1, s=2, alpha=1, color='blue')
            plot5.scatter(eixo_x, eixo_y2, s=2, alpha=1, color='red')
            plot5.scatter(eixo_x, eixo_y3, s=2, alpha=1, color='green')
            plot5.scatter(eixo_x, eixo_y4, s=2, alpha=1, color='orange')
            plot6.bar(eixo_x_bar, eixo_y_bar)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot2.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot3.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot4.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot5.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot1.legend()
            plot2.legend()
            plot3.legend()
            plot4.legend()
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot3.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot4.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot5.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot1.grid(True)
            plot2.grid(True)
            plot3.grid(True)
            plot4.grid(True)
            plot5.grid(True)
            plot1.set_ylabel(nome_y)
            plot2.set_ylabel(nome_y)
            plot3.set_ylabel(nome_y)
            plot4.set_ylabel(nome_y)
            plot5.set_ylabel(nome_y)
            plot6.set_ylabel('Qtd. de dados')
            
        else:
            plot1 = fig.add_subplot(111)
            plot1.plot(eixo_x, eixo_y)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
                   
            plot1.grid(True)       
            plot1.set_ylabel(nome_y)
            plot1.set_title(self.num_enf.get())
        canvas = FigureCanvasTkAgg(fig, master=self.master)
            
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=600, y=57)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
        
    def graficos_range(self):
        my_data = Tratamento()
        data_ana = my_data.retorna_arq(self.num.get())
        
        nome_y, col = self.get_col()

        ano_inicio = int(self.var_ini.get())
        ano_final = int(self.var_fim.get())
        if ano_final < ano_inicio:
            msg.showerror(title='Invalid', message='O range inserido é inválido')
            return
        if self.num_enf.get() == 'Dados comum':
            self.grafico_dc(ano_inicio,ano_final)
            return
        
        eixo_x = list()
        if self.num.get() == 'Dados comum':
            eixo_y1 = list()
            eixo_y2 = list()
            eixo_y3 = list()
            eixo_y4 = list()
            util, tar,t_va, t_vb, t_vc = my_data.get_qtd()
            eixo_y_bar = [util, tar,t_va, t_vb, t_vc]
            eixo_x_bar = ['Comum', 'Alvo','Total vA', 'Total vB', 'Total vC']
        else:
            eixo_y = list()

        dados_lb = list()

        for i in data_ana:
            if int(i[0]) >= ano_inicio and int(i[0]) <= ano_final:
                dados_lb.append(i)

                ano = str(i[0])
                
                mes = str(i[1])
                dia = str(i[2])
                text_data = mes + '/' + dia + '/' + ano
                eixo_x.append(dt.datetime.strptime(text_data,"%m/%d/%Y").date())

                if self.num.get() == 'Dados comum':
                    eixo_y1.append(float(i[col]))
                    eixo_y2.append(float(i[col+3]))
                    eixo_y3.append(float(i[col+6]))
                    eixo_y4.append(float(i[col+9]))
                else:
                    eixo_y.append(float(i[col]))
        
        self.caixad_var.set(dados_lb)
        fig = Figure(figsize=(13,9.5), dpi=100)
        

        if self.num.get() == 'Dados comum':
            plot1 = fig.add_subplot(321)
            plot2 = fig.add_subplot(322)
            plot3 = fig.add_subplot(323)
            plot4 = fig.add_subplot(324)
            plot5 = fig.add_subplot(325)
            plot6 = fig.add_subplot(326)
            plot1.plot(eixo_x, eixo_y1, label="Alvo")
            plot2.plot(eixo_x, eixo_y2, label="Viz A", color="red")
            plot3.plot(eixo_x, eixo_y3, label="Viz B", color='green')
            plot4.plot(eixo_x, eixo_y4, label="Viz C", color='orange')
            plot5.scatter(eixo_x, eixo_y1, s=2, alpha=1, color='blue')
            plot5.scatter(eixo_x, eixo_y2, s=2, alpha=0.6, color='red')
            plot5.scatter(eixo_x, eixo_y3, s=2, alpha=0.6, color='green')
            plot5.scatter(eixo_x, eixo_y4, s=2, alpha=0.6, color='orange')
            plot6.bar(eixo_x_bar, eixo_y_bar)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot2.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot3.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot4.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot5.set_xticklabels(eixo_x, rotation=15, ha='right')
            plot1.legend()
            plot2.legend()
            plot3.legend()
            plot4.legend()
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot2.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot3.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot4.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot5.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y")) 
            plot1.grid(True)
            plot2.grid(True)
            plot3.grid(True)
            plot4.grid(True)
            plot5.grid(True)
            plot1.set_ylabel(nome_y)
            plot2.set_ylabel(nome_y)
            plot3.set_ylabel(nome_y)
            plot4.set_ylabel(nome_y)
            plot5.set_ylabel(nome_y)
            plot6.set_ylabel('Qtd. de dados')
            
        else:
            plot1 = fig.add_subplot(111)
            plot1.plot(eixo_x, eixo_y)
            plot1.set_xticklabels(eixo_x, rotation=15, ha='right')   
            plot1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%y"))   
                
            plot1.grid(True)
            plot1.set_ylabel(nome_y)
            plot1.set_title(self.num_enf.get())
        canvas = FigureCanvasTkAgg(fig, master=self.master)
            
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=600, y=57)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
    
    def gera_range(self):
        teste = Tratamento()
        self.var_ini = StringVar()
        self.anos = teste.get_range(self.num.get())
        Label(self, text='Início:', font='Arial 10 bold', fg='white', bg=fundo).place(x=40, y=190)
        self.com_ini = ttk.Combobox(self, values=self.anos, textvariable=self.var_ini, font='Arial 12', justify=CENTER, state='readonly', width=15).place(x=40, y=210)

        self.var_fim = StringVar()
        Label(self, text='Final:', font='Arial 10 bold', fg='white', bg=fundo).place(x=210, y=190)
        self.com_fim = ttk.Combobox(self, values=self.anos, textvariable=self.var_fim, font='Arial 12', justify=CENTER, state='readonly', width=15).place(x=210, y=210)
        
        Button(self, text='Definir Range', font='Arial 10 bold', fg='white', bg=fun_b, width=23, command=self.graficos_range).place(x=380, y=209)

        print(self.var_fim.get())
            
    

    def __init__(self, *args, **kwargs):
        
        Frame.__init__(self, master=None, bg=fundo)
        
        self.master.title("IC_FAPEMIG - IG V1.1")
        self.master.state("zoomed")

        Label(self, text='TRATAMENTO DE DADOS', font='Arial 14 bold', fg='white', bg=fundo).place(x=190, y=20)
        self.btn_select = Button(self, text="Selecionar arquivos .csv", font='Arial 12 bold ', fg='white',bg=fun_b, width=48, command=self.open_sa)
        self.btn_select.place(x=60, y=60)

        Label(self, text='VIZUALIZAR DADOS', font='Arial 14 bold', fg='white', bg=fundo).place(x=215, y=100)
        
        self.num = StringVar()
        caixa = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C', 'Dados comum']
        Label(self, text="Dado:", font='Arial 10 bold', bg=fundo, fg='white').place(x=40, y=140)
        self.combo = ttk.Combobox(self, values=caixa, textvariable=self.num, width=15, font='Arial 12', justify=CENTER, state='readonly').place(x=40, y=160)
        

        self.num_enf = StringVar()
        enfoque = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        Label(self, text='Parâmetro:', font='Arial 10 bold', bg=fundo, fg='white').place(x=210, y=140)
        self.com_enf = ttk.Combobox(self, values=enfoque, textvariable=self.num_enf, width=15, font='Arial 12', justify=CENTER, state='readonly').place(x=210, y=160)
    
        Button(self, text='Selecionar', font='Arial 10 bold', fg='white', bg=fun_b, width=23, command=self.graficos_comum).place(x=380, y=159)

        self.caixad_var = StringVar()
        self.caixa_data = Listbox(self, width=75, height=15 ,listvariable=self.caixad_var, font='Arial 10').place(x=40, y=250)

        Button(self, text='Aprendizado de Máquina', font='Arial 12 bold', fg='white', bg=fun_ap, width=48, command=self.open_apr).place(x=60, y=520)

        self.pack(fill='both', expand=True)




if __name__ == '__main__':
    mainwindow = Principal()
    mainwindow.mainloop()   