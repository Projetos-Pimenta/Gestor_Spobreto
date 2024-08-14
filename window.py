from tkinter import *
import tkinter
import tkinter.messagebox
import datetime
import pyodbc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import locale
from datetime import datetime 
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

background_image_path = resource_path("background.png")
# Use background_image_path em vez do nome do arquivo diretamente


dados_conexao = (
    "Driver={SQL Server};"
    "Server=DESKTOP-9CCHMFJ\\SQLEXPRESS;"
    "Database=financeiro;"
    "UID=weslley170;"
    "PWD=weslley170;"
)


try:
       conn = pyodbc.connect(dados_conexao)
       print("Connection successful")
except pyodbc.Error as e:
       print("Error in connection:", e)
       # Senha do usuário

conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()


def btn_clicked0():
    print("entrar")
    print("Entrar")
    login = entry0.get()
    senha = entry1.get()
    if login != 'Weslley170' or senha !='Weslley170':
        tkinter.messagebox.showinfo(title='Negado!', message='Login e senha inválidos')
        window.quit()
        
    else:
        tkinter.messagebox.showinfo(title='Bem-Vindo!', message='Olá Spobreto!')
        entry0.delete(0, END)
        entry1.delete(0, END)

#login = entry0.get()
#senha = entry1.get()
#nome_produto = entry3.get()
#quantidade = entry4.get()
#valor = entry5.get()
#troco = entry6.get()
#msg_info = entry2.get()



#falta pensar
def btn_clicked1():
    print("Exibir vendas feitas")
    
    comando = """SELECT numero_notinha, nome_produto, quantidade, valor, troco, data_venda FROM Contabilidade"""
   
    cursor.execute(comando)
    resultados = cursor.fetchall()

    if not resultados:
        tkinter.messagebox.showinfo(
            title='Vendas', message='Nenhuma venda encontrada.')
        return
    
    # Limpa o campo entry2 antes de inserir novos dados
    entry2.delete('1.0', END)
    
    # Construir a string com os dados das vendas
    for linha in resultados:
        # Formatar a data
        data_venda = linha.data_venda.strftime("%d/%m/%Y %H:%M:%S")
        
        texto = (
            f'Numero da Notinha: {linha.numero_notinha}\n'
            f'Nome do Produto: {linha.nome_produto}\n'
            f'Quantidade: {linha.quantidade}\n'
            f'Valor: {linha.valor:.2f}\n'
            f'Troco: {linha.troco:.2f}\n'
            f'Data da Venda: {data_venda}\n'
            '-------------------------------\n'
        )
        entry2.insert(END, texto)  # Insere o texto no campo `entry2`



def btn_clicked2():
    print("Ver Relatório do Dia")
    
    today = datetime.today()
    data_formatada = today.strftime("%Y-%m-%d")
    
    comando = """
        SELECT nome_produto, SUM(quantidade) as total_quantidade, SUM(valor) as total_valor
        FROM Contabilidade
        WHERE CONVERT(date, data_venda) = ? 
        GROUP BY nome_produto
    """
    
    cursor.execute(comando, data_formatada)
    resultados = cursor.fetchall()

    # Verificar se houve algum resultado
    if not resultados:
        tkinter.messagebox.showinfo(title='Relatório', message='Nenhuma venda encontrada para hoje.')
        return
    
    nome_produtos = [linha.nome_produto for linha in resultados]
    total_quantidades = [linha.total_quantidade for linha in resultados]
    total_valor = sum(linha.total_valor for linha in resultados)

    # Cria uma nova janela para o gráfico
    graph_window = Toplevel(window)
    graph_window.title("Relatório de Vendas do Dia")
    
    fig, ax = plt.subplots()
    ax.bar(nome_produtos, total_quantidades)
    ax.set_xlabel("Nome do Produto")
    ax.set_ylabel("Quantidade Vendida")
    ax.set_title("Relatório de Vendas do Dia")
    
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    def fechar_grafico():
        graph_window.destroy()

    # Adiciona um botão para fechar o gráfico
    fechar_btn = Button(graph_window, text="Fechar", command=fechar_grafico)
    fechar_btn.pack()

    # Exibir o total de vendas em R$ na janela do gráfico
    total_label = Label(graph_window, text=f"Total de Vendas em R$: {total_valor:.2f}")
    total_label.pack()


def btn_clicked3():
    
    print("Ver ultima venda")
    numero_notinha = entry7.get()
    conexao = pyodbc.connect(dados_conexao)
    numero_notinha = entry7.get()
    
    comando = f"""SELECT * from Contabilidade
            WHERE numero_notinha = '{numero_notinha}';"""
    cursor.execute(comando)
    for linha in cursor.fetchall():
        entry2.delete(1.0, END)
        texto = f'Numero da Notinha:{linha.numero_notinha}\nNome do Produto:{linha.nome_produto}\nQuantidade:{linha.quantidade}\nValor:{linha.valor}\nTroco:{linha.troco}\nData venda: {linha.data_venda}'
        entry2.insert('1.0', texto)

    
def btn_clicked4():
    print("Adcionar")  
    nome_produto = entry3.get()
    quantidade = entry4.get()
    valor = entry5.get()
    troco = entry6.get()
    numero_notinha = entry7.get()

    if not nome_produto or not quantidade or not valor or not troco:
        tkinter.messagebox.showinfo(title='Gestor!', message='Preencha todos os campos!')
        return

    try:
        quantidade = int(quantidade)
        valor = float(valor)
        troco = float(troco)
    except ValueError:
        tkinter.messagebox.showinfo(title='Gestor!', message='Preencha os campos de quantidade, valor e valor pago corretamente!')
        return

    troco = troco - valor

    if troco < 0:
        tkinter.messagebox.showinfo(title='Gestor!', message='O valor pago é menor que o valor da compra!')
        return

    conexao = pyodbc.connect(dados_conexao)
    cursor = conexao.cursor()
    if conexao:
        cursor = conexao.cursor()
        try:
            cursor.execute("""
                INSERT INTO Contabilidade (numero_notinha, nome_produto, quantidade, valor, troco)
                VALUES (?, ?, ?, ?, ?)
            """, (numero_notinha, nome_produto, quantidade, valor, troco))
            conexao.commit()
            tkinter.messagebox.showinfo(title='Gestor!', message=f'Venda Adicionada com Sucesso! \nTroco: R${troco:.2f}')
            entry7.delete(0, END)
            entry3.delete(0, END)
            entry4.delete(0, END)
            entry5.delete(0, END)
            entry6.delete(0, END)
            entry2.delete('1.0', END)  # Limpa a caixa de texto
            entry2.insert('1.0', f'Troco: R${troco:.2f}')  # Exibe o troco na caixa de texto
        except Exception as e:
            tkinter.messagebox.showerror("Erro!", f"Erro ao adicionar venda: {e}")
        finally:
            cursor.close()
            conexao.close()
def btn_clicked5():
    print("Deletar")
    numero_notinha = entry7.get()

    conexao = pyodbc.connect(dados_conexao)
    if conexao:
            cursor = conexao.cursor()
            try:
                cursor.execute("DELETE FROM Contabilidade WHERE numero_notinha=?", (numero_notinha,))
                conexao.commit()
                tkinter.messagebox.showinfo(title='Gestor!', message='Venda Deletada com Sucesso!')
            except Exception as e:
                tkinter.messagebox.showerror("Erro!", f"Erro ao deletar venda: {e}")
            finally:
                cursor.close()
                conexao.close()


window = Tk()
window.title('Controle De Vendas')

window.geometry("761x717")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 717,
    width = 761,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    369.0, 353.5,
    image=background_img)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    122.0, 273.5,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry0.place(
    x = 35, y = 258,
    width = 174,
    height = 29)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    122.0, 333.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry1.place(
    x = 35, y = 318,
    width = 174,
    height = 29)

entry2_img = PhotoImage(file = f"img_textBox2.png")
entry2_bg = canvas.create_image(
    501.5, 637.0,
    image = entry2_img)

entry2 = Text(
    bd = 0,
    bg = "#e7e7e7",
    highlightthickness = 0)

entry2.place(
    x = 316, y = 569,
    width = 371,
    height = 134)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked0,
    relief = "flat")

b0.place(
    x = 73, y = 396,
    width = 87,
    height = 28)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked1,
    relief = "flat")

b1.place(
    x = 431, y = 242,
    width = 174,
    height = 31)

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked2,
    relief = "flat")

b2.place(
    x = 551, y = 195,
    width = 174,
    height = 31)

img3 = PhotoImage(file = f"img3.png")
b3 = Button(
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked3,
    relief = "flat")

b3.place(
    x = 551, y = 149,
    width = 174,
    height = 31)

img4 = PhotoImage(file = f"img4.png")
b4 = Button(
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked4,
    relief = "flat")

b4.place(
    x = 321, y = 149,
    width = 174,
    height = 31)

img5 = PhotoImage(file = f"img5.png")
b5 = Button(
    image = img5,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked5,
    relief = "flat")

b5.place(
    x = 321, y = 195,
    width = 174,
    height = 31)

entry3_img = PhotoImage(file = f"img_textBox3.png")
entry3_bg = canvas.create_image(
    620.5, 341.5,
    image = entry3_img)

entry3 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

entry3.place(
    x = 535, y = 329,
    width = 171,
    height = 23)

entry4_img = PhotoImage(file = f"img_textBox4.png")
entry4_bg = canvas.create_image(
    620.5, 392.5,
    image = entry4_img)

entry4 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

entry4.place(
    x = 535, y = 380,
    width = 171,
    height = 23)

entry5_img = PhotoImage(file = f"img_textBox5.png")
entry5_bg = canvas.create_image(
    620.5, 434.5,
    image = entry5_img)

entry5 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

entry5.place(
    x = 535, y = 422,
    width = 171,
    height = 23)

entry6_img = PhotoImage(file = f"img_textBox6.png")
entry6_bg = canvas.create_image(
    620.5, 485.5,
    image = entry6_img)

entry6 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

entry6.place(
    x = 535, y = 473,
    width = 171,
    height = 23)

entry7_img = PhotoImage(file = f"img_textBox7.png")
entry7_bg = canvas.create_image(
    619.5, 300.5,
    image = entry7_img)

entry7 = Entry(
    bd = 0,
    bg = "#d9d9d9",
    highlightthickness = 0)

entry7.place(
    x = 535, y = 288,
    width = 169,
    height = 23)

window.resizable(False, False)
window.mainloop()