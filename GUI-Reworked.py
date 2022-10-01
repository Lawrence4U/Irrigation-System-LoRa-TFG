from pickle import TRUE
from time import sleep
from tkinter import *
from tkinter import ttk
from xmlrpc.client import Boolean
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.sankey import RIGHT




def intVartoInt(lista):
    lista = [i.get() for i in lista]
    return lista
    
    
    
def cButtonEvent():
    global opcion
    valores = intVartoInt(opcion)
    print(valores)
    
if __name__ == "__main__":
    events = ""
    root = Tk()
    root.geometry("400x400+300+300")
    frame = Frame(root)
    frame.pack()
    opcion= [IntVar(value=0),IntVar(value=0),IntVar(value=0),IntVar(value=0),IntVar(value=0),IntVar(value=0),IntVar(value=0)]
    ch1 = Checkbutton(frame, text="L", variable=opcion[0], command=cButtonEvent, indicatoron=0)
    ch1.pack()
    ch2 = Checkbutton(frame, text="M", variable=opcion[1], command=cButtonEvent  ,indicatoron=0)
    ch2.pack()
    imagen = PhotoImage(file="imagenes\circulo.png").subsample(40,40)
    imagen2 = PhotoImage(file="imagenes\circulo2.png").subsample(40,40)
    ch3 = Checkbutton(frame, text="X", variable=opcion[2], command=cButtonEvent , indicatoron=0, image=imagen, selectimage=imagen2)
    ch3.pack()
    # tk.Radiobutton(frame,text="M", indicatoron=0)
    # lanzar hilos para el resto de la app
    root.mainloop()