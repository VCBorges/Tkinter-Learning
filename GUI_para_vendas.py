from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk() #variavel que inicia o tkinter

class Funcs(): #classe que terá os metodos para o funcionamento dos botões 

    def limpa_produto(self): #metodo do botão limpar
        self.id_entry.delete(0, END)
        self.nome_entry.delete(0, END) #faz o botão limpar funcionar na entry relacionada
        self.preco_entry.delete(0, END)
        self.lab_entry.delete(0, END)
        self.modo_entry.delete(0, END)
    
    def connect_db(self): #função que cria um database e conecta ele ao tkinter
        self.connect = sqlite3.connect("produtos.db") #cria um database
        self.cursor = self.connect.cursor() #conecta o database
    
    def disconnect_db(self): #função que desconecta o database
        self.connect.close()
    
    def montadb(self): 
        self.connect_db(); print("connecting to database...")  #exite uma mensagem de carregamento enquanto o database é conectado

        self.cursor.execute("""   
            CREATE TABLE IF NOT EXISTS produtos (
                ID INTEGER PRIMARY KEY,
                nome_produto CHAR(40) NOT NULL,
                preco INTEGER NOT NULL,
                laboratorio CHAR(40),
                modo_pagamento CHAR(40) NOT NULL    
            );
        """) #cria uma tabela no database
        self.connect.commit(); print("banco de dados criação")
        self.disconnect_db()
    
    def variaveis(self):
        self.id = self.id_entry.get()
        self.nome = self.nome_entry.get() #variavel que recebe o conteudo que esta na entry *nome_entry
        self.preco = self.preco_entry.get() #variavel que recebe o conteudo que esta na entry *preco_entry
        self.modo_pagamento = self.modo_entry.get() #variavel que recebe o conteudo que esta na entry *modo_entry
        self.laboratorio = self.lab_entry.get() #variavel que recebe o conteudo que esta na entry *lab_entry
    
    def add_prod(self): #metodo para adionar produtos no database
        
        self.variaveis()
        self.connect_db() #conecta ao database

        self.cursor.execute(""" INSERT INTO produtos (nome_produto, preco, laboratorio, modo_pagamento)
            VALUES(?, ?, ? ,?)""", (self.nome, self.preco, self.laboratorio, self.modo_pagamento)) #abre o cursor para receber um comando SQL de adicionar itens ao database; as variaveis subtituem os '?'
        self.connect.commit() #commita as mudanças
        self.disconnect_db() #disconecta do database
        self.select_lista() 
        self.limpa_produto()

    def select_lista(self): #metodo para selecionar os itens do database e adionar ao treeview

        self.lista.delete(*self.lista.get_children()) 
        self.connect_db() #conecta ao database
        listadb = self.cursor.execute(""" SELECT ID, nome_produto, preco, modo_pagamento, laboratorio FROM produtos""") #variavel que recebe o conteudo do comando SQL SELECT
        for i in listadb:
            self.lista.insert("", END, values=i) #adiciona os itens de listadb ao treeview 'lista'
        self.disconnect_db() #desconecta database

    def onDoubleClick(self,event): #metodo para adicionar o double click nos itens do treeview
        self.limpa_produto()

        for n in self.lista.selection(): #laço que adiciona o conteudo da TreeView nos respectivos entrys
            col1, col2, col3, col4, col5 = self.lista.item(n, 'values')
            self.id_entry.insert(END, col1)
            self.nome_entry.insert(END,col2)
            self.preco_entry.insert(END,col3)
            self.lab_entry.insert(END,col5)
            self.modo_entry.insert(END,col4)

    def deleta_produto(self):
        self.variaveis()
        self.connect_db()
        self.cursor.execute("""DELETE FROM produtos WHERE ID = ? """, (self.id,))
        self.connect.commit()
        self.disconnect_db()
        self.limpa_produto()
        self.select_lista()

    def altera_produto(self):
        self.variaveis()
        self.connect_db()
        self.cursor.execute(""" UPDATE produtos SET nome_produto = ?, preco = ?, laboratorio = ?, modo_pagamento = ? WHERE ID = ?""", (self.nome, self.preco, self.laboratorio, self.modo_pagamento, self.id))
        self.connect.commit()
        self.disconnect_db()
        self.select_lista()
        self.limpa_produto()

    def busca_produto(self):
        self.variaveis()
        self.connect_db()
        self.lista.delete(*self.lista.get_children())
        self.nome_entry.insert(END, '%')
        self.cursor.execute(""" SELECT ID, nome_produto, preco, laboratorio, modo_pagamento FROM produtos WHERE nome_produto LIKE '%s' ORDER BY nome_produto ASC """ % self.nome)
        buscanomePROD = self.cursor.fetchall()
        for i in buscanomePROD:
            self.lista.insert("", END, values=i)
        self.limpa_produto()
        self.disconnect_db()

class App(Funcs):
    def __init__(self):
        self.root = root

        self.tela() #metedo de definções da janela

        self.frames_da_tela() #insere o frame na janela

        self.widgets_frame1() #insere os widgets

        self.lista_frame2() #insere a lista do frame 2

        self.montadb() #metodo para montar o database

        self.select_lista() #metodo para adicionar iten no treeview

        self.Menus()

        root.mainloop() #mantem a janela aberta

    def tela(self): #metodo que configura a aparencia da janela

        self.root.title("Cadastro") #define o titulo da janela

        self.root.configure(background='grey29')   #define a cor do background da janela; pode ser uma imagem png tbm

        self.root.geometry("780x500") #metodo que define o tamanho padrão da janela

        self.root.resizable(True, True) #define se o tamanho da janela pode ser alterado; primeiro parametro altura e o segundo a largura

        #self.root.maxsize(width=900, height=700) #define um tamanho maximo para a janela

        #self.root.minsize(width=900, height=700) #define o tamanho minimo da janela

    def frames_da_tela(self): #metodo que cria e configura os frames
        
        self.frame_1 = Frame(self.root, bd= 10, highlightbackground='grey21',highlightthickness=3, bg= 'grey38') #Frame: cria o frame;bd=: borda; bg=: cor de fundo do frame; highlightbackground= cor da borda em volta do frame; highlightthickness= tamanho da borda em volta do frame
        self.frame_1.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.46)  #função que defina a posição onde o objeto ficara posicionado na janela; baseado nos parametros relx, rely, relwidth e relheight que vão de 0 a 1
        
        self.frame_2 = Frame(self.root, bd= 10, highlightbackground='grey21',highlightthickness=3,bg='grey38')
        self.frame_2.place(relx= 0.02, rely= 0.5, relwidth= 0.96, relheight= 0.46)

    def widgets_frame1(self): #função para criar botões 

        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)

        self.aba1.configure(background="grey38")
        self.aba2.configure(background="grey38")

        self.abas.add(self.aba1, text="aba1")
        self.abas.add(self.aba2, text="aba2")
        self.abas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.botao_limpar = Button(self.aba1, text='Limpar',command=self.limpa_produto, bg='grey29',highlightbackground='grey21') #Button: cria o botão; self.frame onde ele estara, text= texto que estara escrito no botão, bd=: tipo de borda;fg=: cor do texto;font=: fonte do texto;
        self.botao_limpar.place(relx= 0.2, rely= 0.9, relwidth=0.1, relheight=0.15) #função que define a posição do botão e o seu tamanho

        self.botao_buscar = Button(self.aba1, text='Buscar', bg='grey29',highlightbackground='grey21', command=self.busca_produto) 
        self.botao_buscar.place(relx= 0.31, rely= 0.9, relwidth=0.1, relheight=0.15)

        self.botao_alterar = Button(self.aba1, text='Alterar', command=self.altera_produto, bg='grey29',highlightbackground='grey21') 
        self.botao_alterar.place(relx= 0.42, rely= 0.9, relwidth=0.1, relheight=0.15)

        self.botao_inserir = Button(self.aba1, text='Inserir', command=self.add_prod, bg='grey29',highlightbackground='grey21') 
        self.botao_inserir.place(relx= 0.53, rely= 0.9, relwidth=0.1, relheight=0.15)

        self.botao_apagar = Button(self.aba1, text='Apagar',command=self.deleta_produto, bg='grey29',highlightbackground='grey21') 
        self.botao_apagar.place(relx= 0.64, rely= 0.9, relwidth=0.1, relheight=0.15)

        #LABELS
        self.lb_nome = Label(self.aba1,text="Nome:", bg= 'grey38') #Função que cria uma Label 
        self.lb_nome.place(relx= 0.001, rely= 0.1, relwidth=0.1, relheight=0.15)

        self.lb_preco = Label(self.aba1,text="Preço:", bg= 'grey38') #Função que cria uma Label 
        self.lb_preco.place(relx= 0.75, rely= 0.1, relwidth=0.1, relheight=0.15)

        self.lb_lab = Label(self.aba1,text="Laboratorio:", bg= 'grey38') #Função que cria uma Label 
        self.lb_lab.place(relx= 0.55, rely= 0.4, relwidth=0.16, relheight=0.15)

        self.lb_modo = Label(self.aba1,text="Modo de Pagamento:", bg= 'grey38') #Função que cria uma Label 
        self.lb_modo.place(relx= 0.001, rely= 0.4, relwidth=0.228, relheight=0.15)

        self.id_entry = Entry(self.aba1,background='grey')  #Função que cria um entrada de texto
        self.id_entry.place(relx= 0.09, rely= 0.6, relwidth=0.1, relheight=0.15) #relwidth: tamanho da barra de entrada

        self.nome_entry = Entry(self.aba1,background='grey')  #Função que cria um entrada de texto
        self.nome_entry.place(relx= 0.09, rely= 0.1, relwidth=0.65, relheight=0.15) #relwidth: tamanho da barra de entrada

        self.preco_entry = Entry(self.aba1,background='grey')  #Função que cria um entrada de texto
        self.preco_entry.place(relx= 0.84, rely= 0.1, relwidth=0.15, relheight=0.15)

        self.modo_entry = Entry(self.aba1,background='grey')  #Função que cria um entrada de texto
        self.modo_entry.place(relx= 0.22, rely= 0.4, relwidth=0.3, relheight=0.15)

        self.lab_entry = Entry(self.aba1,background='grey')  #Função que cria um entrada de texto
        self.lab_entry.place(relx= 0.698, rely= 0.4, relwidth=0.295, relheight=0.15)

    def lista_frame2(self): #frame 2 4
        
        self.lista = ttk.Treeview(self.frame_2, height=3, columns=('col1','col2','col3','col4','col5')) #função que cria a treeview
        self.lista.heading('#0', text='') #função que cria o heading da coluna;"# " codigo da coluna; define o texto do heading
        self.lista.heading('#1', text='ID')
        self.lista.heading('#2', text='Nome')
        self.lista.heading('#3', text='Preço')
        self.lista.heading('#4', text='Modo de Pagamento')
        self.lista.heading('#5', text='Laboratorio')

        self.lista.column('#0', width=1) #função que define a grossura da coluna na lista
        self.lista.column('#1', width=1)
        self.lista.column('#2', width=150)
        self.lista.column('#3', width=50)
        self.lista.column('#4', width=200)
        self.lista.column('#5', width=150)

        self.lista.place(relx= 0.01, rely= 0.1, relwidth=0.95, relheight=0.85) #função que define a posição da tabela

        self.scrolllista = Scrollbar(self.frame_2,orient='vertical',command=self.lista.yview) #função que cria uma scrollbar; define o sentido da scrollbar
        self.lista.configure(yscroll=self.scrolllista.set) #função que faz a fusão da tabela com a scrollbar
        self.scrolllista.place(relx=0.96,rely=0.1,relwidth=0.03,relheight=0.85) #função que define a posição da scrollbar
        
        self.lista.bind("<Double-1>", self.onDoubleClick)

    def Menus(self):
        menubar = Menu(self.root,bg="grey25")
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): 
            self.root.destroy()

        menubar.add_cascade(label= "Opções", menu= filemenu)
        menubar.add_cascade(label= "sobre", menu= filemenu2)

        filemenu.add_command(label="Sair", command= Quit)
        filemenu2.add_command(label="Limpa Cliente", command= self.limpa_produto)

App()   

