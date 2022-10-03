from pickle import TRUE
from time import sleep
from tkinter import *
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
    
    
    
    
if __name__ == "__main__":
    
    root = Tk()
    root.title("Interfaz")
    root.geometry("400x400+600+300")
    
    tabGroup = Notebook(root)
    
    tab1 = Frame(tabGroup)
    tab2 = Frame(tabGroup)
    
    tabGroup.add(tab1, text='Pestaña 1')
    tabGroup.add(tab2, text='Pestaña 2')
    
    tabGroup.pack(expand=1, fill="both")
    
    programas = Combobox(tab1, values=[1,2,3,4,5,6], width= 5, justify= 'center', state='readonly')
    programas.current(0)
    programas.bind("<<ComboboxSelected>>", comboSeleccionado)
    programas.pack(side="left")
    
    btnActivo = Button(tab1, command=toggle, text='Inactivo', style='A.TButton')
    btnActivo.pack(side='left')
    
    btnActivo2 = Button(tab1, command=toggle, text='Inactivo', style='B.TButton')
    btnActivo2.pack(side='left')
    
    style = Style()
    
    style.theme_use('alt')
    style.configure('A.TButton', width = 20, foreground = 'white', borderwidth=0, focusthickness=0, focuscolor='none', takefocus=False)
    style.map("A.TButton", background=[('pressed', 'green4'), ('!pressed', 'grey27')])
        
    
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