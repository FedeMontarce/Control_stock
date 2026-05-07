"""
Punto de entrada de la aplicacion.

Inicializa la base de datos, lanza la interfaz grafica y garantiza
el cierre correcto de la conexion al salir.
"""

from tkinter import Tk
from vista import Vista
from database import inicializar_db, cerrar_db

if __name__ == "__main__":
    inicializar_db()
    root = Tk()
    Vista(root)
    root.mainloop()
    cerrar_db()