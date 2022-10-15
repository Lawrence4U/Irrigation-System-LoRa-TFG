from pickle import TRUE
from time import sleep
import tkinter as tk
from tkinter.ttk import *
from xmlrpc.client import Boolean
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import text
from matplotlib.sankey import RIGHT

def toggle():
    print(btnActivo['text'])
    
    
    if btnActivo['text'] == "Inactivo":
        print("opt1")
        btnActivo.state(["pressed"])
        btnActivo.configure(text='Activo')
        print(btnActivo.state())
    else:
        btnActivo.state(["!pressed"])
        btnActivo.configure(text='Inactivo')
        print(btnActivo.state())


def intVartoInt(lista):
    lista = [i.get() for i in lista]
    return lista
    
    
    
def cButtonEvent():
    global opcion
    valores = intVartoInt(opcion)
    # ch3.configure(relief=FLAT)
    print(valores)
    
def comboSeleccionado(*args):
    print(selPrograma.get())
    
def commandFreq():
    if varFrecuencia.get():
        print("Personalizado")
    else:
        print("Unico")
        
    return
    
    
if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Interfaz")
    root.geometry("400x400+600+300")
    
    altura = root.winfo_screenwidth()
    anchura = root.winfo_screenheight()
    #cargando estilos
    style = Style()
    
    style.theme_use('alt')
    style.configure('A.TButton', width = 10, foreground = 'white', borderwidth=0, focusthickness=0, focuscolor='none', takefocus=False)
    style.map("A.TButton", background=[('pressed', 'green4'), ('!pressed', 'grey27')])
    style.configure('TLabels', width = 10, foreground = 'white2')
    style.configure('TRadiobutton', indicatoron=0)
    
    #Cargando ventana
    tabGroup = Notebook(root)
    
    tab1 = Frame(tabGroup)
    tab2 = Frame(tabGroup)
    
    tabGroup.add(tab1, text='Pestaña 1')
    tabGroup.add(tab2, text='Pestaña 2')
    tabGroup.pack(expand=1, fill="both")
    
    selPrograma = Combobox(tab1, values=[1,2,3,4,5,6], width= 5, justify= 'center', state='readonly')
    selPrograma.current(0)
    selPrograma.bind("<<ComboboxSelected>>", comboSeleccionado)
    
    btnActivo = Button(tab1, command=toggle, text='Inactivo', style='A.TButton')
    btnActivo2 = Label(tab1, text='Frecuencia del programa')
    
    varFrecuencia = tk.IntVar()
    rad1 = tk.Radiobutton(tab1, text='Único',indicatoron=0, variable=varFrecuencia, value =0, command=commandFreq)
    rad2 = tk.Radiobutton(tab1, text='Personalizado',indicatoron= 0,variable=varFrecuencia, value =1, command=commandFreq)

    #distribución
    # selPrograma.grid(row=0,column=0)
    selPrograma.place(x=20,y=20)
    btnActivo.place(x=20,y=50)
    btnActivo2.place(x=20,y= 80)
    rad1.place(x=40,y= 110)
    rad2.place(x=100,y= 110)  
    
    
    root.mainloop()