from ctypes import alignment
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
    print(chLunes.state())
    global opcion
    valores = intVartoInt(opcion)
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
    style.configure('A.TCheckbutton', foreground = 'white', anchor='center', width=3, indicatorrelief=tk.FLAT, indicatormargin=-10, indicatordiameter=-10, heigth=3)
    style.map('A.TCheckbutton', background=[('!selected', 'grey27'), ('selected', 'green4')])
    
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
    radFreq1 = tk.Radiobutton(tab1, text='Único',indicatoron=0, variable=varFrecuencia, value =0, command=commandFreq)
    radFreq2 = tk.Radiobutton(tab1, text='Personalizado',indicatoron= 0,variable=varFrecuencia, value =1, command=commandFreq)

    ##Programacion semanal
    ###Primero habria que cargar la selección existente para este dia
    opcion= [tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0)]
    chLunes = Checkbutton(tab1, text="L", variable=opcion[0], command=cButtonEvent, style='A.TCheckbutton')
    chMartes = Checkbutton(tab1, text="M", variable=opcion[1], command=cButtonEvent, style='A.TCheckbutton')
    chMiercoles = Checkbutton(tab1, text="X", variable=opcion[2], command=cButtonEvent, style='A.TCheckbutton')
    chJueves = Checkbutton(tab1, text="J", variable=opcion[3], command=cButtonEvent, style='A.TCheckbutton')
    chViernes = Checkbutton(tab1, text="V", variable=opcion[4], command=cButtonEvent, style='A.TCheckbutton')
    chSabado = Checkbutton(tab1, text="S", variable=opcion[5], command=cButtonEvent, style='A.TCheckbutton')
    chDomingo = Checkbutton(tab1, text="D", variable=opcion[6], command=cButtonEvent, style='A.TCheckbutton')
    
    #distribución
    selPrograma.place(x=20, y=20)
    btnActivo.place(x=20, y=50)
    btnActivo2.place(x=20, y=80)
    radFreq1.place(x=30, y=110)
    radFreq2.place(x=71, y=110)
    chLunes.place(x= 20, y=150)
    chMartes.place(x= 50, y=150)
    chMiercoles.place(x= 80, y=150)
    chJueves.place(x= 110, y=150)
    chViernes.place(x= 140, y=150)
    chSabado.place(x= 170, y=150)
    chDomingo.place(x= 200, y=150)
    # rad1.winfo_rootx()+rad1.winfo_width()
    
    

    root.mainloop()