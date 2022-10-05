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
    print(programas.get())
    
def commandFreq():
    if varFrecuencia.get():
        print("Hola")
    else:
        print("ADios")
        
    return
    
    
if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Interfaz")
    root.geometry("400x400+600+300")
    
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
    
    programas = Combobox(tab1, values=[1,2,3,4,5,6], width= 5, justify= 'center', state='readonly')
    programas.current(0)
    programas.bind("<<ComboboxSelected>>", comboSeleccionado)
    programas.grid(row=0,column=0)
    
    btnActivo = Button(tab1, command=toggle, text='Inactivo', style='A.TButton')
    btnActivo.grid(row=1,column=0)
    
    btnActivo2 = Label(tab1, text='Frecuencia del programa')
    btnActivo2.grid(row=2,column=0)
    
    varFrecuencia = tk.IntVar()
    rad1 = tk.Radiobutton(tab1, text='Único',indicatoron=0, variable=varFrecuencia, value =0, command=commandFreq)
    rad2 = tk.Radiobutton(tab1, text='Personalizado',indicatoron= 0,variable=varFrecuencia, value =1, command=commandFreq)
    rad1.grid(row=3, column=0)
    rad2.grid(row=3, column=1)
    
    
    
    
    
    
        
    
    # frame = Frame(root)
    # frame.pack()
    # opcion= [IntVar(value=0),IntVar(value=0),IntVar(value=0),IntVar(value=0),IntVar(value=0),IntVar(value=0),IntVar(value=0)]
    # ch1 = Checkbutton(frame, text="L", variable=opcion[0], command=cButtonEvent, indicatoron=0)
    # ch1.pack()
    # ch2 = Checkbutton(frame, text="M", variable=opcion[1], command=cButtonEvent  ,indicatoron=0)
    # ch2.pack()
    # imagen = PhotoImage(file="imagenes\circulo.png").subsample(40,40)
    # imagen2 = PhotoImage(file="imagenes\circulo2.png").subsample(80,80)
    # ch3 = Checkbutton(frame, text="X", variable=opcion[2], command=cButtonEvent , indicatoron=0, image=imagen, selectimage=imagen2)
    # ch3.pack()
    # tk.Radiobutton(frame,text="M", indicatoron=0)
    # lanzar hilos para el resto de la app
    root.mainloop()