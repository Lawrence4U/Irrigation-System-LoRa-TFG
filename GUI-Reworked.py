from pickle import TRUE
import tkinter as tk
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
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    opcion= [tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0),tk.IntVar(value=0)]
    ch1 = tk.Checkbutton(root, text="L", variable=opcion[0], command=cButtonEvent, indicatoron=0)
    ch1.pack()
    ch2 = tk.Checkbutton(root, text="M", variable=opcion[1], command=cButtonEvent  ,indicatoron=0)
    ch2.pack()
    ch3 = tk.Checkbutton(root, text="X", variable=opcion[2], command=cButtonEvent ,indicatoron=0)
    ch3.pack()
    monitor = tk.Label(root)
    monitor.pack()
    # tk.Radiobutton(frame,text="M", indicatoron=0)
    # lanzar hilos para el resto de la app
    root.mainloop()
    print("Hola")