from tkinter import *
from tkinter import filedialog as dlg
from tkinter import messagebox as msg
from tkinter import ttk

from pyparsing import col
from tratar import Tratamento
from ml import Treinamento
from triangulacao import Triangulaction
from meta_learning import MetaL
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
import datetime as dt
import os
import matplotlib.dates as mdates
import pyscreenshot
from tksheet import Sheet

os.system("cls")

fundo = '#4F4F4F' #? Cor de fundo da tela
fun_b = '#3CB371' #? Cor de fundo dos botoes
fun_ap = '#9C444C'
fun_alt = '#C99418'
fun_meta_le = '#191970'

class Selecionar_Arquivos_win(Toplevel):
    def tratar(self):
        datat = Tratamento() #* Criando um objeto que tem como atributos os endereços dos arquivos
        datat.alvo = self.dir_alvo.get()
        datat.vizinhaA = self.dir_vA.get()
        datat.vizinhaB = self.dir_vB.get()
        datat.vizinhaC = self.dir_vC.get()
        datat.download = self.dir_save.get()
        datat.get_data_trada()
        msg.showinfo(title="Sucesso!", message="Arquivos Selecionados com sucesso!")
        Toplevel.destroy(self)
    def __init__(self, master=None):

        
        def procura_arq(entry_txt):
            path = dlg.askopenfilename()
            entry_txt.set(path)

        def escolhe_pasta(entry_txt):
            path = dlg.askdirectory()
            entry_txt.set(path)

        

        Toplevel.__init__(self, master=master)

        self.title('Selecionar arquivos')
        self.geometry("500x420")
        
        self.configure(background=fundo)

        
        Grid.columnconfigure(self, 0, weight=1)
        
        
        
        Label(self, text='SELECIONAR ARQUIVOS', font='Arial 18 bold', fg='white',bg=fundo).grid(row=0, column=0, padx=10, pady=2, columnspan=3)

        self.dir_alvo = StringVar()
        Label(self, text="Cidade Alvo:", font='Arial 12 bold', fg='white', bg=fundo).grid(row=1, column=0,  padx=10, pady=2, sticky='W')
        Entry(self, textvariable= self.dir_alvo, font='Arial 12', width=45).grid(row=2, column=0, sticky='WE', padx=10, pady=2)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_alvo)).grid(row=2, column=1, sticky='W', padx=10, pady=2)

        self.dir_vA = StringVar()
        Label(self, text="Cidade vizinha A:", font='Arial 12 bold', fg='white', bg=fundo).grid(row=3, column=0, ipadx=10, pady=2, sticky='W')  
        Entry(self, textvariable= self.dir_vA, font='Arial 12', width=45).grid(row=4, column=0, sticky='WE', padx=10, pady=2)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_vA)).grid(row=4, column=1, sticky='W', padx=10, pady=2)

        self.dir_vB = StringVar()
        Label(self, text="Cidade vizinha B:", font='Arial 12 bold', fg='white', bg=fundo).grid(row=5, column=0,  ipadx=10, pady=2, sticky='W') 
        Entry(self, textvariable=self.dir_vB, font='Arial 12', width=45).grid(row=6, column=0, sticky='WE', padx=10, pady=2)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_vB)).grid(row=6, column=1, sticky='W', padx=10, pady=2)

        self.dir_vC = StringVar()
        Label(self, text="Cidade vizinha C:", font='Arial 12 bold', fg='white', bg=fundo).grid(row=7, column=0,  ipadx=10, pady=2, sticky='W')  
        Entry(self, textvariable=self.dir_vC, font='Arial 12', width=45).grid(row=8, column=0, sticky='WE', padx=10, pady=2)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_vC)).grid(row=8, column=1, sticky='W', padx=10, pady=10)

        self.dir_save = StringVar()
        Label(self, text="Local para salvar os dados tratados:", font='Arial 12 bold', fg='white', bg=fundo).grid(row=9, column=0, ipadx=10, pady=2, sticky='W')
        teste = Entry(self, textvariable=self.dir_save, font='Arial 12', width=45).grid(row=10, column=0, sticky='WE', padx=10, pady=2)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: escolhe_pasta(self.dir_save)).grid(row=10, column=1, sticky='W', padx=10, pady=10)
        '''
        Label(self, text='SELECIONAR ARQUIVOS', font='Arial 18 bold', fg='white',bg=fundo).place(x=110, y=10)

        self.dir_alvo = StringVar()
        Label(self, text="Cidade Alvo:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=50)   
        Entry(self, textvariable= self.dir_alvo, font='Arial 12', width=45).place(x=20, y=75)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_alvo)).place(x=440, y=73)

        self.dir_vA = StringVar()
        Label(self, text="Cidade vizinha A:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)   
        Entry(self, textvariable= self.dir_vA, font='Arial 12', width=45).place(x=20, y=125)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_vA)).place(x=440, y=123)

        self.dir_vB = StringVar()
        Label(self, text="Cidade vizinha B:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=150)   
        Entry(self, textvariable=self.dir_vB, font='Arial 12', width=45).place(x=20, y=175)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_vB)).place(x=440, y=173)

        self.dir_vC = StringVar()
        Label(self, text="Cidade vizinha C:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=200)   
        Entry(self, textvariable=self.dir_vC, font='Arial 12', width=45).place(x=20, y=225)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: procura_arq(self.dir_vC)).place(x=440, y=223)

        self.dir_save = StringVar()
        Label(self, text="Local para salvar os dados tratados:", font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=250)
        teste = Entry(self, textvariable=self.dir_save, font='Arial 12', width=45).place(x=20, y=275)
        Button(self, text='...', font='Arial 10 bold', fg='white', bg=fun_b, width=4, command=lambda: escolhe_pasta(self.dir_save)).place(x=440, y=273)
        '''
        #Todo: Para Agilizar os testes
        self.dir_alvo.set('E:/IC/Dados/NOVAS REGIOES/AMPA/1_BELTERRA.csv')
        self.dir_vA.set('E:/IC/Dados/NOVAS REGIOES/AMPA/2_MONTE_ALEGRE.csv')
        self.dir_vB.set('E:/IC/Dados/NOVAS REGIOES/AMPA/3_OBIDOS.csv')
        self.dir_vC.set('E:/IC/Dados/NOVAS REGIOES/AMPA/4_PARINTINS.csv')
        self.dir_save.set('E:/IC/Dados/NOVAS REGIOES/AMPA/dados')

        Button(self, text='Prosseguir', font='Arial 12 bold', fg='white', bg=fun_b, width=45, command=self.tratar).grid(row=11, column=0, padx=10, pady=2, columnspan=3)



class Aprendizado_Marquina(Toplevel):
    def int_float(self, val):
        try:
            return int(val)
        except ValueError:
            return float(val)

    def valid_maxf(self, val):
        if val.isdigit() == True:
            val = int(val)
        elif val.isalnum() == True and val.isdigit() == False:
            val = str(val)
        elif val.isalnum() == False and val.isdigit() == False and val.isalpha() == False:
            val = float(val)
        
        return val

    def salvar_paramt(self):
        img = pyscreenshot.grab(bbox=(0,25,1920,1040))
        img.show()
        img.save(r'C:\Users\pablo\Desktop\teste.png')

    def data_prev(self, pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x):
        self.laf_res = LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)

        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)

        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_predict, label='Predict', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
    
    def get_end(self, cidade):
        Trat = Tratamento()
        return Trat.retorna_end(cidade)

    def gerar_preview_dt(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        


        cidade = self.get_end(self.data_s.get())

        indicador = self.ind_s.get()
        divisao = int(self.por_trei.get())
        criterio = self.criterion_v.get()
        splitter = self.splitter_v.get()
        maxd = int(self.maxd_v.get())             #* Max_depth
        minsams = self.int_float(self.minsam_s_v.get())    #* Min_samples_split
        minsaml = self.int_float(self.minsam_l_v.get())    #* Min_samples_leaf
        minwei = float(self.minweifra_l_v.get())
        maxfe = self.valid_maxf(self.maxfeat_v.get())
        maxleaf = int(self.maxleaf_n.get())
        
        minim = float(self.minimp_dec.get())
        ccp = float(self.ccp_alp_v.get())
        n_tes = int(self.num_teste.get())

        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.ArvoreDecisao(cidade, indicador, divisao, criterio, splitter, maxd, minsaml, maxfe, maxleaf, n_tes, minsams, minwei, minim, ccp, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def gerar_preview_nn(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        
        cidade = self.get_end(self.data_s.get())
        
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5
    
        divisao = int(self.por_trei.get())

        activ = self.activation_v.get()
        solv = self.solver_v.get()
        alph = float(self.alpha_v.get())
        batc = self.batch_size_v.get()
        learn_r = self.learning_rate_v.get()
        learn_r_ini = float(self.learning_rate_init_v.get())
        powt = float(self.power_t_v.get())
        maxit = int(self.max_iter_v.get())
        shuf = self.shuffle_v.get()
        tol = float(self.tol_v.get())
        verb = self.verbose_v.get()
        warms = self.warm_start_v.get()
        moment = float(self.momentum_v.get())
        neste = self.nesterovs_momentum_v.get()
        earlyst = self.early_stopping_v.get()
        valid = float(self.validation_fraction_v.get())
        b1 = float(self.beta_1_v.get())
        b2 = float(self.beta_2_v.get())
        niter = int(self.n_iter_no_change_v.get())
        maxfun = int(self.max_fun_v.get())
        n_teste = int(self.num_teste.get())
        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.RedeNeural(cidade, indicador, divisao, n_teste, activ, solv, alph, batc, learn_r, learn_r_ini, powt, maxit, shuf, tol, verb, warms, moment, neste, earlyst, valid, b1, b2, niter, maxfun, salvar_m)

        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
    
    def gerar_preview_svm(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()
        
        cidade = self.get_end(self.data_s.get())
        
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5
    
        divisao = int(self.por_trei.get())
        n_teste = int(self.num_teste.get())
        kern = self.kernel_v.get()
        degre = self.degree_v.get()
        gam = self.gamma_v.get()
        coef = float(self.coef0_v.get())
        t = float(self.tol_v.get())
        c = float(self.c_v.get())
        eps = float(self.epsilon_v.get())
        shr = self.shrinking_v.get()
        cach = float(self.cache_size_v.get())
        verb = self.verbose_v.get()
        maxi = int(self.maxiter_v.get())


        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.SVR(cidade, indicador, divisao, n_teste, kern, degre, gam, coef, t, c, eps, shr, cach, verb, maxi, salvar_m)

        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)
        
    def gerar_preview_Kn(self):
        prev = Treinamento()
        salvar_m = self.save_model.get()

        cidade = self.get_end(self.data_s.get())

        '''if self.data_s.get() == 'Cidade alvo':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\alvo_limpa.txt'
        elif self.data_s.get() == 'Vizinha A':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaA_limpa.txt'
        elif self.data_s.get() == 'Vizinha B':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaB_limpa.txt'
        elif self.data_s.get() == 'Vizinha C':
            cidade = r'E:\IC\Interface_Grafica\Dados_verificacao\vizinhaC_limpa.txt'''

        n_tes = int(self.num_teste.get())
        divisao = int(self.por_trei.get())
        n_neig = self.n_neighbors_v.get()
        algor = self.algorithm_v.get()
        leaf_s = self.leaf_size_v.get()
        pv = self.p_v.get()
        n_job = self.n_jobs_v.get()

        if n_job.isdigit() == True:
            n_job = int(n_job)
            
        indicador = self.ind_s.get()
        if indicador == 'Precipitação':
            indicador = 3
        elif indicador == 'Temperatura máxima':
            indicador = 4
        elif indicador == 'Temperatura mínima':
            indicador = 5

        pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x = prev.KNeighbors(cidade, indicador, divisao, n_tes, n_neig, algor, leaf_s, pv, n_job, salvar_m)
        self.data_prev(pts, media_ea, media_er, maior_ea, exat_maior, pre_maior, menor_ea, exat_menor, pre_menor, eixo_y_exato, eixo_y_predict, eixo_x)

    def gera_param(self):
        opcao = self.ml_selected.get()
        if opcao == 'Decision Trees':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_p = LabelFrame(self, text='Parâmetros', width=600, height=395, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=100)

            self.criterion_v = StringVar()
            lista_cri = ["squared_error", "friedman_mse", "absolute_error", "poisson"]
            self.criterion_v.set("squared_error")
            Label(self, text='Criterion:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_cri, textvariable=self.criterion_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

            self.splitter_v = StringVar()
            lista_spl = ["best", "random"]
            self.splitter_v.set("best")
            Label(self, text='Splitter:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            ttk.Combobox(self, values=lista_spl, textvariable=self.splitter_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)
            

            self.maxd_v = StringVar()
            self.maxd_v.set("10")
            Label(self, text="Max_deph (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            self.ent_maxd = Entry(self, textvariable=self.maxd_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

            self.minsam_s_v = IntVar()
            self.minsam_s_v.set(2)
            Label(self, text="Min_samples_split (int/float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            self.minsam_s = Entry(self, textvariable=self.minsam_s_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)
            
            self.minsam_l_v = IntVar()
            self.minsam_l_v.set(50)
            Label(self, text="Min_samples_leaf (int/float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            self.ent_minsam_l = Entry(self, textvariable=self.minsam_l_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

            self.minweifra_l_v = StringVar()
            self.minweifra_l_v.set("0.0")
            Label(self, text="Min_weight_fraction_leaf (float (.)):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            self.ent_minweifra_l = Entry(self, textvariable=self.minweifra_l_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)
            
            self.maxfeat_v = StringVar()
            self.maxfeat_v.set("auto")
            Label(self, text="Max_features :", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Label(self, text="Valores para Max_features:", font='Arial 12 bold', fg=fun_alt, bg=fundo).place(x=340, y=300)
            Label(self, text="int / float / 'auto' / 'sqrt' / 'log2'", font='Arial 12 bold', fg=fun_alt, bg=fundo).place(x=340, y=325)
            self.ent_maxfeat_v = Entry(self, textvariable=self.maxfeat_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

            self.maxleaf_n = StringVar()
            self.maxleaf_n.set("10")
            Label(self, text="Max_leaf_nodes (int)", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            self.ent_maxleaf_n = Entry(self, textvariable=self.maxleaf_n, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

            self.minimp_dec = StringVar()
            self.minimp_dec.set("0.0")
            Label(self, text="Min_impurity_decrease (float (.))", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            self.ent_minimp_dec = Entry(self, textvariable=self.minimp_dec, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

            self.ccp_alp_v = StringVar()
            self.ccp_alp_v.set("0.0")
            Label(self, text="Ccp_alpha (value>0.0 float):", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            self.ent_ccp_alp = Entry(self, textvariable=self.ccp_alp_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

            self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=500)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=520)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=520)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=580)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=580)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)

           
            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_dt).place(x=50, y=685)
            #Button(self, text='Salvar Paramt.', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.salvar_paramt).place(x=340, y=685)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=685)
        elif opcao == 'Neural network':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=625, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)

            self.activation_v = StringVar()
            lista_act = ['identity', 'logistic', 'tanh', 'relu']
            self.activation_v.set('relu')
            Label(self, text='Activation:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_act, textvariable=self.activation_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)
            
            self.solver_v = StringVar()
            lista_sol = ['lbfgs', 'sgd', 'adam']
            self.solver_v.set('adam')
            Label(self, text='Solver:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            ttk.Combobox(self, values=lista_sol, textvariable=self.solver_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

            self.alpha_v = StringVar()
            self.alpha_v.set('0.0001')
            Label(self, text='Alpha:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.alpha_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

            self.batch_size_v = StringVar()
            self.batch_size_v.set('auto')
            Label(self, text='Batch_size (int / "auto"):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.batch_size_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

            self.learning_rate_v = StringVar()
            lista_learn = ['constant', 'invscaling', 'adaptive']
            self.learning_rate_v.set('constant')
            Label(self, text="Learning_rate:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            ttk.Combobox(self, values=lista_learn, textvariable=self.learning_rate_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=265)

            self.learning_rate_init_v = StringVar()
            self.learning_rate_init_v.set('0.001')
            Label(self, text='Learning_rate_init (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            Entry(self, textvariable=self.learning_rate_init_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=265)

            self.power_t_v = StringVar()
            self.power_t_v.set('0.5')
            Label(self, text='Power_t (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Entry(self, textvariable=self.power_t_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=325)

            self.max_iter_v = StringVar()
            self.max_iter_v.set('200')
            Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=300)
            Entry(self, textvariable=self.max_iter_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=325)


            self.shuffle_v = BooleanVar()
            self.shuffle_v.set(True)
            Label(self, text='Shuffle (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            Entry(self, textvariable=self.shuffle_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=385)

            self.tol_v = StringVar()
            self.tol_v.set('0.0001')
            Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            Entry(self, textvariable=self.tol_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=385)

            self.verbose_v = BooleanVar()
            self.verbose_v.set(False)
            Label(self, text='Verbose (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            Entry(self, textvariable=self.verbose_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=445)

            self.warm_start_v = BooleanVar()
            self.warm_start_v.set(False)
            Label(self, text='Warm_start (bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=420)
            Entry(self, textvariable=self.warm_start_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=445)

            self.momentum_v = StringVar()
            self.momentum_v.set('0.9')
            Label(self, text='Momentum (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=480)
            Entry(self, textvariable=self.momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=505)

            self.nesterovs_momentum_v = BooleanVar()
            self.nesterovs_momentum_v.set(True)
            Label(self, text='Nesterovs_momentum:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=480)
            Entry(self, textvariable=self.nesterovs_momentum_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=505)

            self.early_stopping_v = BooleanVar()
            self.early_stopping_v.set(False)
            Label(self, text='Early_stopping:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=540)
            Entry(self, textvariable=self.early_stopping_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=565)

            self.validation_fraction_v = StringVar()
            self.validation_fraction_v.set('0.1')
            Label(self, text='Validation_fraction (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=540)
            Entry(self, textvariable=self.validation_fraction_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=565)

            self.beta_1_v = StringVar()
            self.beta_1_v.set('0.9')
            Label(self, text='Beta_1 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=600)
            Entry(self, textvariable=self.beta_1_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=625)

            self.beta_2_v = StringVar()
            self.beta_2_v.set('0.999')
            Label(self, text='Beta_2 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=600)
            Entry(self, textvariable=self.beta_2_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=625)

            self.n_iter_no_change_v = StringVar()
            self.n_iter_no_change_v.set('10')
            Label(self, text='N_iter_no_change (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=660)
            Entry(self, textvariable=self.n_iter_no_change_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=685)

            self.max_fun_v = StringVar()
            self.max_fun_v.set('15000')
            Label(self, text='max_fun (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=660)
            Entry(self, textvariable=self.max_fun_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=685)

            '''   data   '''
            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=730)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=750)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=775)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=750)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=775)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=810)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=835)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=810)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=835)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_nn).place(x=50, y=915)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=915)
        elif opcao == 'Nearest Neighbors':

           w = Canvas(self, width=615, height=900, background=fundo, border=0)
           w.place(x=10, y=95)
           

           self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100) 

           self.n_neighbors_v = IntVar()
           self.n_neighbors_v.set(5)
           Label(self, text='N_neighbors (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
           Entry(self, textvariable=self.n_neighbors_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=145)

           self.algorithm_v = StringVar()
           lista_alg = ['auto', 'ball_tree', 'kd_tree', 'brute']
           self.algorithm_v.set('auto')
           Label(self, text='Algorithm:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
           ttk.Combobox(self, values=lista_alg, textvariable=self.algorithm_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=145)

           self.leaf_size_v = IntVar()
           self.leaf_size_v.set(30)
           Label(self, text='Leaf_size (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
           Entry(self, textvariable=self.leaf_size_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=205)

           self.p_v = IntVar()
           self.p_v.set(2)
           Label(self, text='P (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
           Entry(self, textvariable=self.p_v, width=27, font='Arial 12', justify=CENTER).place(x=340, y=205)

           self.n_jobs_v = StringVar()
           self.n_jobs_v.set('5')
           Label(self, text='N_jobs (int / "None"):', font='Aria 12 bold', fg='white', bg=fundo).place(x=50, y=240)
           Entry(self, textvariable=self.n_jobs_v, width=27, font='Arial 12', justify=CENTER).place(x=50, y=265)

           self.lbf_d = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=320)

           self.data_s = StringVar()
           self.data_s.set('Cidade alvo')
           lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
           Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=340)
           self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

           self.ind_s = StringVar()
           self.ind_s.set('Temperatura máxima')
           lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
           Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=340)
           ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

           self.por_trei = IntVar()
           self.por_trei.set(70)
           Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=400)
           Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)

           self.num_teste = IntVar()
           self.num_teste.set(5)
           Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=400)
           self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

           Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_Kn).place(x=50, y=505)
           self.save_model = IntVar()
           Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505) 
        elif opcao == 'Support Vector':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=385, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)
            
            self.kernel_v = StringVar()
            lista_ker = ['linear', 'poly', 'rbf', 'sigmoid']
            self.kernel_v.set('rbf')
            Label(self, text='Kernel:', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            ttk.Combobox(self, values=lista_ker, textvariable=self.kernel_v, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=145)

            self.degree_v = IntVar()
            self.degree_v.set(3)
            Label(self, text='Degree (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            Entry(self, textvariable=self.degree_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145) 

            self.gamma_v = StringVar()
            self.gamma_v.set('scale')
            Label(self, text='Gamma ("scale", "auto", float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.gamma_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

            self.coef0_v = StringVar()
            self.coef0_v.set('0.0')
            Label(self, text='Coef0 (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.coef0_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

            self.tol_v = StringVar()
            self.tol_v.set('0.001')
            Label(self, text='Tol (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            Entry(self, textvariable=self.tol_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)

            self.c_v = StringVar()
            self.c_v.set('1.0')
            Label(self, text='C (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=240)
            Entry(self, textvariable=self.c_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=265)

            self.epsilon_v = StringVar()
            self.epsilon_v.set('0.1')
            Label(self, text='Epsilon (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=300)
            Entry(self, textvariable=self.epsilon_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=325)   

            self.shrinking_v = BooleanVar()
            self.shrinking_v.set(True)
            Label(self, text='Shrinking (Bool):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=300)
            Entry(self, textvariable=self.shrinking_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=325)

            self.cache_size_v = StringVar()
            self.cache_size_v.set('200')
            Label(self, text='Cache_size (float):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=360)
            Entry(self, textvariable=self.cache_size_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=385)   

            self.verbose_v = BooleanVar()
            self.verbose_v.set(False)
            Label(self, text='Verbose (Bool):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=360)
            Entry(self, textvariable=self.verbose_v, font='Arial 12', width=27, justify=CENTER).place(x=340, y=385)

            self.maxiter_v = IntVar()
            self.maxiter_v.set(-1)
            Label(self, text='Max_iter (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=420)
            Entry(self, textvariable=self.maxiter_v, font='Arial 12', width=27, justify=CENTER).place(x=50, y=445)

            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=500)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=520)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=545)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=520)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=545)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=580)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=605)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=580)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=605)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=680)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=680)
        elif opcao == 'Gaussian Process':
            w = Canvas(self, width=615, height=900, background=fundo, border=0)
            w.place(x=10, y=95)
            self.lbf_para_nn = LabelFrame(self, text='Parâmetros', width=600, height=205, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=100)
            
            self.alpha_gp = StringVar()
            self.alpha_gp.set('0.0000000001')
            Label(self, text='Alpha (float): ', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=120)
            Entry(self, textvariable=self.alpha_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=145)
            
            self.n_restarts_op = IntVar()
            self.n_restarts_op.set(0)
            Label(self, text='N_restart_optimizer (int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=120)
            Entry(self, textvariable=self.n_restarts_op, font='Arial 12', width=27, justify=CENTER).place(x=340, y=145)

            self.normalize_y_gp = BooleanVar()
            self.normalize_y_gp.set(0)
            Label(self, text='Normalize_y (Bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=180)
            Entry(self, textvariable=self.normalize_y_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=205)

            self.copy_X_train = BooleanVar()
            self.copy_X_train.set(0)
            Label(self, text='Copy_X_train (Bool 1/0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=180)
            Entry(self, textvariable=self.copy_X_train, font='Arial 12', width=27, justify=CENTER).place(x=340, y=205)

            self.rand_state_gp = StringVar()
            self.rand_state_gp.set('None')
            Label(self, text='Random_state ("None" / int):', font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=240)
            Entry(self, textvariable=self.rand_state_gp, font='Arial 12', width=27, justify=CENTER).place(x=50, y=265)
            

            self.lbf_dt_nn = LabelFrame(self, text='Dados', width=600, height=170, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=320)

            self.data_s = StringVar()
            self.data_s.set('Cidade alvo')
            lista_dt = ['Cidade alvo', 'Vizinha A', 'Vizinha B', 'Vizinha C']
            Label(self, text="Dados para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=340)
            self.combo_c = ttk.Combobox(self, values=lista_dt, textvariable=self.data_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=50, y=365)

            self.ind_s = StringVar()
            self.ind_s.set('Temperatura máxima')
            lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
            Label(self, text='Indicador:', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=340)
            ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=25, font='Arial 12', justify=CENTER, state='readonly').place(x=340, y=365)

            self.por_trei = IntVar()
            self.por_trei.set(70)
            Label(self, text="Porção para treinamento:", font='Arial 12 bold', fg='white', bg=fundo).place(x=50, y=400)
            Scale(self, variable=self.por_trei, orient=HORIZONTAL, length=240).place(x=50, y=425)
        
            self.num_teste = IntVar()
            self.num_teste.set(5)
            Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=400)
            self.ent_num_teste = Entry(self, textvariable=self.num_teste, width=27, font='Arial 12', justify=CENTER).place(x=340, y=425)

            Button(self, text='Preview', font='Arial 11 bold', fg='white', bg=fun_b, width=25, command=self.gerar_preview_svm).place(x=50, y=505)
            self.save_model = IntVar()
            Checkbutton(self, text='Salvar modelo', variable=self.save_model, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=505)

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Aprendizado de máquina')
        self.state("zoomed")
        self.configure(background=fundo)

        Label(self, text='APRENDIZADO DE MÁQUINA', font='Arial 14 bold', fg='white', bg=fundo).place(x=200, y=20)

        self.ml_selected = StringVar()
        self.ml_selected.set('Decision Trees')
        lista_ml = ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml, textvariable=self.ml_selected, width=28, font='Arial 12', justify=CENTER, state='readonly').place(x=20, y=60)
        Button(self, text='Escolher Machine Learning', font='Arial 11 bold', fg='white', bg=fun_ap, width=30, command=self.gera_param).place(x=340, y=59)

class Triangulaction_techniques(Toplevel):
    def ver_est(self):
        trian = Triangulaction()
        trian.show_map()

    def preview_idw(self):
        LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        trian = Triangulaction()
        ind = self.ind_s.get()
        if ind == 'Precipitação':
            foco = 1
        elif ind == 'Temperatura máxima':
            foco = 2
        else:
            foco = 3

        trian.idw(foco)

        eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_idw()
        
        pts = round(abs((media_er*100)-100) ,2)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)
        '''
        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)
        '''
        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_tri, label='IDW', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def preview_aa(self):
        LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        trian = Triangulaction()
        ind = self.ind_s.get()
        if ind == 'Precipitação':
            foco = 1
        elif ind == 'Temperatura máxima':
            foco = 2
        else:
            foco = 3

        trian.aa(foco)

        eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_aa()
        
        pts = round(abs((media_er*100)-100) ,2)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)
        '''
        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)
        '''
        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_tri, label='AA', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def preview_rw(self):
        LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        trian = Triangulaction()
        ind = self.ind_s.get()
        if ind == 'Precipitação':
            foco = 1
        elif ind == 'Temperatura máxima':
            foco = 2
        else:
            foco = 3

        trian.rw(foco)

        eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_rw()
        
        pts = round(abs((media_er*100)-100) ,2)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)
        '''
        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)
        '''
        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_tri, label='RW', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def preview_onr(self):
        LabelFrame(self, text='Preview dos resultados', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=650, y=50)
        trian = Triangulaction()
        ind = self.ind_s.get()
        if ind == 'Precipitação':
            foco = 1
        elif ind == 'Temperatura máxima':
            foco = 2
        else:
            foco = 3

        trian.onr(foco)

        eixo_x, eixo_y_tri, eixo_y_exato, media_ea, media_er, lixo = trian.get_onr()
        
        pts = round(abs((media_er*100)-100) ,2)
        Label(self, text='Pontuação (0-100): '+ str(pts) +'pts', font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=70)
        media_ea = round(media_ea, 4)
        Label(self, text='Média Erro absoluto: '+ str(media_ea), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=100)
        media_er = round(media_er, 4)
        Label(self, text='Média Erro relativo: '+ str(media_er), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=130)
        '''
        Label(self, text='Maior erro absoluto: ' + str(round(maior_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=160)
        Label(self, text="Valor exato do maior EA: " + str(round(exat_maior,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=160)
        Label(self, text="Predict do maior EA: " + str(round(pre_maior, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=160)

        Label(self, text='Menor erro absoluto: ' + str(round(menor_ea,4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=680, y=190)
        Label(self, text="Valor exato do menor EA: " + str(round(exat_menor,4)),font='Arial 12 bold', fg='white', bg=fundo).place(x=940, y=190)
        Label(self, text="Predict do menor EA: " + str(round(pre_menor, 4)), font='Arial 12 bold', fg='white', bg=fundo).place(x=1200, y=190)
        '''
        figura = Figure(figsize=(12,7.3), dpi=100)
        plot_r = figura.add_subplot(111)
        plot_r.plot(eixo_x, eixo_y_exato,label='Exato', color='green')
        plot_r.plot(eixo_x, eixo_y_tri, label='ONR', color='red')
        plot_r.legend()
        plot_r.grid(True)
        plot_r.set_ylabel("Temperatura(°C)")
        plot_r.set_xlabel("Comparações")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=680, y=240)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()



    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Técnicas de Triangulação')
        self.state("zoomed")
        self.configure(background=fundo)

        Label(self, text='TÉCNICAS DE TRIANGULAÇÃO', font='Arial 14 bold', fg='white', bg=fundo).place(x=180, y=20)

        Button(self, text='Visualizar Estações', font='Arial 11 bold', fg='white', bg=fun_alt, width=55, command=self.ver_est).place(x=70, y=80)

        Label(self, text='Indicador climático:', font='Arial 13 bold', fg='white', bg=fundo).place(x=70, y=140)
        self.ind_s = StringVar()
        self.ind_s.set('Temperatura máxima')
        lista_ind = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        ttk.Combobox(self, values=lista_ind, textvariable=self.ind_s, width=40, font='Arial 11', justify=CENTER, state='readonly').place(x=230, y=140)


        LabelFrame(self, text='Métodos de Triangulação', width=600, height=250, font='Arial 12 bold', fg ='white', bg=fundo).place(x=20, y=200)

        Button(self, text='Arithmetic Average',font='Arial 11 bold', fg='white', bg=fun_alt, width=58, command=self.preview_aa).place(x=55, y=240)
        Button(self, text='Inverse Distance Weighted',font='Arial 11 bold', fg='white', bg=fun_alt, width=58, command=self.preview_idw).place(x=55, y=280)
        Button(self, text='Optimized Inverse Distance Weighted',font='Arial 11 bold', fg='white', bg=fun_alt, width=58).place(x=55, y=320)
        Button(self, text='Regional Weight',font='Arial 11 bold', fg='white', bg=fun_alt, width=58, command=self.preview_rw).place(x=55, y=360)
        Button(self, text='Optimized Normal Ratio',font='Arial 11 bold', fg='white', bg=fun_alt, width=58, command=self.preview_onr).place(x=55, y=400)

class MetaLearning(Toplevel):
    def gerar_teste_perso(self):
        base = self.ml_lv0_p.get()
        tria = self.ml_tr0_p.get()
        meta = self.ml_lv1.get()
        ind = self.ind_meta_perso.get()
        n_teste = int(self.num_teste_mtp.get())
        pre0 = int(self.pre_para_lv0.get())
        pre1 = int(self.pre_para_lv1.get())
        janela = self.type_input.get()
        if ind == 'Precipitação':
            foco = 1
        elif ind == 'Temperatura máxima':
            foco = 2
        elif ind == 'Temperatura mínima':
            foco = 3
        mp = MetaL()
        meta_ea, meta_er, meta_porc_erro, meta_r2, x_meta, y_meta, y_alvo, base_ea, base_er, base_porc, base_r2, tria_ea, tria_er = mp.meta_learning_personalizado(foco, base, tria, meta, 0, 0, n_teste, janela)
        
        
        LabelFrame(self, text='PREVIEW DOS RESULTADOS:', width=1250, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=640, y=60)

        texto = "ERRO ABSOLUTO:    Machine Learning: " + str(round(base_ea, 4)) + "   ||   Triangulação: " + str(round(tria_ea,4)) + "   ||   Meta Learning: " + str(round(meta_ea,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=90)
        
        texto = "ERRO RELATIVO:      Machine Learning: " + str(round(base_er, 4)) + "   ||   Triangulação: " + str(round(tria_er,4)) + "   ||   Meta Learning: " + str(round(meta_er,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=130)
        
        texto = "ERRO(%):                     Machine Learning: " + str(round(base_porc, 4)) + "   ||   Triangulação: " + str(round(tria_ea*100,4)) +  "   ||   Meta Learning: " + str(round(meta_porc_erro,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=170)
        
        texto = "R2:                                  Machine Learning: " + str(round(base_r2, 4)) +  "   ||   Meta Learning: " + str(round(meta_r2,4))
        Label(self, text=texto, font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=210)

        figura = Figure(figsize=(12.3, 7.5), dpi=100)
        plot1 = figura.add_subplot(2,2,1)
        x_ea = ["MacL", 'Trian', 'Meta']
        y_ea = [base_ea, tria_ea, meta_ea]
        plot1.bar(x_ea, y_ea)
        plot1.set_ylabel("Erro Absoluto")
        
        plot2 = figura.add_subplot(2,2,2)
        x_er = ["MacL", 'Trian', 'Meta']
        y_er = [base_er, tria_er, meta_er]
        plot2.bar(x_er, y_er)
        plot2.set_ylabel("Erro Relativo")

        plot3 = figura.add_subplot(2,2,3)
        x_por = ["MacL", 'Trian','Meta']
        y_por = [base_porc, tria_ea*100,meta_porc_erro]
        plot3.bar(x_por, y_por)
        plot3.set_ylabel("Erro (%)")

        plot4 = figura.add_subplot(2,2,4)
        x_r2 = ["MacL", 'Meta']
        y_r2 = [base_r2, meta_r2]
        plot4.bar(x_r2, y_r2)
        plot4.set_ylabel("R2")

        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=650, y=250)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()

    def gerar_teste_global(self):
      
        foco = self.ind_meta_comb.get()
        num_t = int(self.num_teste_mtc.get())
        janela = 'Sim'
        
        mc = MetaL()
        
        todos, ranking = mc.meta_learning_combina(foco, 0, 0, num_t, janela)
        
        
        LabelFrame(self, text='RESULTADOS:', width=1260, height=950, font='Arial 12 bold', fg='white', bg=fundo).place(x=640,y=60)

        Label(self, text='Modelos gerados:', font='Arial 12 bold', fg='white', bg=fundo).place(x=660, y=90)
                
        dados_todos = list()
        for i in range(len(todos)):
            buff = list()
            buff.append(todos[i][0])
            buff.append(todos[i][1])
            buff.append(todos[i][2])
            buff.append(todos[i][3])
            buff.append(todos[i][5])
            buff.append(todos[i][6])
            buff.append(todos[i][7])
            dados_todos.append(buff)

        self.tabela_todos = Sheet(self, data=dados_todos, headers=['Modelo','Base Learning', 'Triangulation', 'Meta Learning', 'Erro Absoluto', 'Erro Relativo', 'Erro(%)'], width=890, height=500)
        self.tabela_todos.enable_bindings()
        self.tabela_todos.place(x=660, y=120)
        

        Label(self, text='Ranking dos modelos:', font='Arial 12 bold', fg='white', bg=fundo).place(x=1580, y=90)

        dados_ranking = list()
        x = list()
        y = list()
        for i in range(len(ranking)):
            buff = list()
            buff.append(ranking[i][0])
            buff.append(round(float(ranking[i][1].replace(',', '.')), 4))  
            dados_ranking.append(buff)

            if i <= 15:
                x.append(str(ranking[i][0]))
                y.append(float(ranking[i][1].replace(',', '.')))

        
        self.tabela_ranking = Sheet(self, data=dados_ranking, headers=['Modelo', 'Erro'], width=270, height=500, column_width=115)
        self.tabela_ranking.enable_bindings()
        self.tabela_ranking.place(x=1580, y=120)   

        figura = Figure(figsize=(12, 3.3), dpi=100)
        plot = figura.add_subplot(1,1,1)

        plot.bar(x, y)
        plot.set_ylabel('Erro(%)')
        plot.set_xlabel("Modelos")
        plot.grid(True)
        
        canvas = FigureCanvasTkAgg(figura, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().place(x=660, y=650)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.place(x=1150, y=10)
        toolbar.update()
     
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)
        self.title('Meta Learning')
        self.state("zoomed")
        self.configure(background=fundo)

        Label(self, text='META-LEARNING', font='Arial 14 bold', fg='white', bg=fundo).place(x=240, y=20)

        LabelFrame(self, text='TESTE PERSONALIZADO:', width=600, height=450, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=60)

        Label(self, text='Base-Learning (Level 0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=90)
        self.ml_lv0_p = StringVar()
        self.ml_lv0_p.set('Decision Trees')
        lista_ml0 =  ['Nenhum','Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml0, textvariable=self.ml_lv0_p, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=120)

        Label(self, text='Triangulation (Level 0):', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=190)
        self.ml_tr0_p = StringVar()
        self.ml_tr0_p.set('Arithmetic Average')
        lista_tr0 =  ['Nenhum', 'Arithmetic Average', 'Inverse Distance Weighted', 'Regional Weight', 'Optimized Normal Ratio']
        ttk.Combobox(self, values=lista_tr0, textvariable=self.ml_tr0_p, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=220)

        Label(self, text='Meta-Learning (Level 1):', font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=145)
        self.ml_lv1 = StringVar()
        self.ml_lv1.set('Decision Trees')
        lista_ml1 =  ['Decision Trees', 'Neural network', 'Nearest Neighbors', 'Support Vector', 'Gaussian Process']
        ttk.Combobox(self, values=lista_ml1, textvariable=self.ml_lv1, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=340, y=175)

        Label(self, text='Indicador climático:', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=270)
        self.ind_meta_perso = StringVar()
        self.ind_meta_perso.set('Temperatura máxima')
        lista_ind_meta_p = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        ttk.Combobox(self, values=lista_ind_meta_p, textvariable=self.ind_meta_perso, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=300)

        self.num_teste_mtp = IntVar()
        self.num_teste_mtp.set(1)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=270)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste_mtp, width=29, font='Arial 12', justify=CENTER).place(x=340, y=300)

        Label(self, text='Deseja usar alguma ML pré-parametrizada?', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=340)
        self.pre_para_lv0 = IntVar()
        self.pre_para_lv1 = IntVar()
        Checkbutton(self, text='Level 0', variable=self.pre_para_lv0, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=40, y=360)
        Checkbutton(self, text='Level 1', variable=self.pre_para_lv1, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=180, y=360)
        
        Label(self, text='Deseja utilizar a janela deslizante?', font='Arial 12 bold', fg='White', bg=fundo).place(x=40, y=400)
        self.type_input = StringVar()
        self.type_input.set('Sim')
        lista_type_input = ['Sim', 'Não']
        ttk.Combobox(self, values=lista_type_input, textvariable=self.type_input, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=430)
        
        Button(self, text='Gerar Preview', font='Arial 11 bold', bg=fun_meta_le, fg='white', width=62, command=self.gerar_teste_perso).place(x=40, y=470)

        '''Teste global'''
        LabelFrame(self, text='TESTE GLOBAL:', width=600, height=210, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=520)
        
        Label(self, text='Quais MLs você deseja utilizar?', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=550)

        self.pre_nn_comb = IntVar()
        self.pre_dt_comb = IntVar()
        self.pre_nneig_comb = IntVar()
        self.pre_sv_comb = IntVar()
        self.pre_gp_comb = IntVar()
        Checkbutton(self, text='NN', variable=self.pre_nn_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=40, y=580)
        Checkbutton(self, text='DT', variable=self.pre_dt_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=140, y=580)
        Checkbutton(self, text='NNeig.', variable=self.pre_nneig_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=240, y=580)
        Checkbutton(self, text='SV', variable=self.pre_sv_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=340, y=580)
        Checkbutton(self, text='GP', variable=self.pre_gp_comb, bg=fundo, font='Arial 12 bold', activebackground=fundo).place(x=440, y=580)
        
        Label(self, text='Indicador climático:', font='Arial 12 bold', fg='white', bg=fundo).place(x=40, y=620)
        self.ind_meta_comb = StringVar()
        self.ind_meta_comb.set('Temperatura máxima')
        lista_ind_meta_p = ['Precipitação', 'Temperatura máxima', 'Temperatura mínima']
        ttk.Combobox(self, values=lista_ind_meta_p, textvariable=self.ind_meta_comb, width=30, font='Arial 11', justify=CENTER, state='readonly').place(x=40, y=650)

        self.num_teste_mtc = IntVar()
        self.num_teste_mtc.set(1)
        Label(self, text="Número de testes (int):", font='Arial 12 bold', fg='white', bg=fundo).place(x=340, y=620)
        self.ent_num_teste = Entry(self, textvariable=self.num_teste_mtc, width=29, font='Arial 12', justify=CENTER).place(x=340, y=650)
        
        Button(self, text='Gerar Preview TG', font='Arial 11 bold', bg=fun_meta_le, fg='white', width=62, command=self.gerar_teste_global).place(x=40, y=690)

        #Aviso
        LabelFrame(self, text='ATENÇÃO:', width=600, height=120, font='Arial 12 bold', fg='white', bg=fundo).place(x=20, y=740)
        Label(self, text='Dependendo da combinação feita no "Teste Personalizado" ou no "TESTE ', font='Arial 12 bold', fg='#FF8C00', bg=fundo).place(x=40, y=770)
        Label(self, text='GLOBAL", pode demorar alguns minutos, devido ao processamento.', font='Arial 12 bold', fg='#FF8C00', bg=fundo).place(x=40, y=790)
        Label(self, text='Fique à vontade para utilizar seu computador para fazer outras coisas.', font='Arial 12 bold', fg='#FF8C00', bg=fundo).place(x=40, y=820)

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
            

            if self.num.get() == 'Dados comum':
                try:
                    
                    eixo_y1.append(float(i[col].replace(',', '.')))
                    eixo_y2.append(float(i[col+3].replace(',', '.')))
                    eixo_y3.append(float(i[col+6].replace(',', '.')))
                    eixo_y4.append(float(i[col+9].replace(',', '.')))
                    eixo_x.append(dt.datetime.strptime(text_data,"%m/%d/%Y").date())
                except ValueError:
                    pass
                
            else:
                try:
                    eixo_y.append(float(i[col]))
                    eixo_x.append(dt.datetime.strptime(text_data,"%m/%d/%Y").date())
                except ValueError:
                    pass
        
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

        #print(self.var_fim.get())
            
    def open_tri(self):
        window = Triangulaction_techniques()
        window.mainloop()

    def open_meta_learning(self):
        window = MetaLearning()
        window.mainloop()

    def __init__(self, *args, **kwargs):
        
        Frame.__init__(self, master=None, bg=fundo)
        
        self.master.title("IC_FAPEMIG - IG V1.1")
        self.master.state("zoomed")

        Label(self, text='TRATAMENTO DE DADOS', font='Arial 14 bold', fg='white', bg=fundo).place(x=190, y=20)
        self.btn_select = Button(self, text="Selecionar arquivos .csv", font='Arial 12 bold ', fg='white',bg=fun_b, width=52, command=self.open_sa)
        self.btn_select.place(x=40, y=60)

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

        Button(self, text='Aprendizado de Máquina', font='Arial 12 bold', fg='white', bg=fun_ap, width=52, command=self.open_apr).place(x=40, y=520)
        self.pack(fill='both', expand=True)

        Button(self, text='Triangulação', font='Arial 12 bold', fg='white', bg=fun_alt,width=52, command=self.open_tri).place(x=40, y=560)

        Button(self, text='Meta-Learning', font='Arial 12 bold', fg='white', bg=fun_meta_le, width=52, command=self.open_meta_learning).place(x=40, y=600)
        
if __name__ == '__main__':
    mainwindow = Principal()
    mainwindow.mainloop()   