"""
Modulo de la vista (patron MVC).

Se encarga de construir la interfaz grafica utilizando Tkinter.
Interactua con el Controlador para ejecutar las operaciones
correspondientes sobre los datos.
"""

from tkinter import BOTH, LEFT, TOP, X, Y, Button, Entry, Frame, Label, \
    LabelFrame, StringVar, Toplevel, messagebox
from tkinter import ttk, filedialog
from controlador import Controlador
import servidor

COLUMNAS = ("id", "codigo", "nombre", "precio", "stock")
"""Orden original de las columnas de la tabla de productos."""

ANCHOS_COLUMNAS = {"id": 50, "codigo": 100, "nombre": 250,
                   "precio": 100, "stock": 80}
"""Anchos originales de cada columna en pixeles."""

ANCHO_BOTON = 20
"""Ancho fijo para todos los botones del panel lateral."""


class Vista:
    """Clase que representa la interfaz grafica de la aplicacion."""

    def __init__(self, root):
        """Inicializa la vista y construye la interfaz principal.

        :param root: Ventana principal de Tkinter.
        :type root: tkinter.Tk
        """
        self.root = root
        self.controlador = Controlador()
        self._configurar_ventana()
        self._construir_ui()

    def _configurar_ventana(self):
        """Configura las propiedades de la ventana."""
        self.root.title("Control de Stock")
        self.root.geometry("900x550")
        self.root.resizable(False, False)
        self.root.iconbitmap("imagenes/logo.ico")

    def _construir_ui(self):
        """Construye los componentes principales de la interfaz.

        Crea el panel de gestion CRUD y la tabla de productos.
        """
        self._crear_panel_crud()
        self._crear_tabla()
        self.controlador.registrar_observador(lambda: self.controlador.actualizar(self.tabla))
        self.controlador.actualizar(self.tabla)

    def _crear_panel_crud(self):
        """Crea el panel lateral con los campos y botones."""
        frame_crud = LabelFrame(self.root, padx=10, pady=10,
                                text="Gestión de Productos")
        frame_crud.pack(side=LEFT, fill=Y)

        Label(frame_crud, text="Código:").pack(anchor="w")
        self.entry_codigo = Entry(frame_crud, width=22)
        self.entry_codigo.pack(fill=X, pady=5)

        Label(frame_crud, text="Nombre:").pack(anchor="w")
        self.entry_nombre = Entry(frame_crud, width=22)
        self.entry_nombre.pack(fill=X, pady=5)

        Label(frame_crud, text="Precio:").pack(anchor="w")
        self.entry_precio = Entry(frame_crud, width=22)
        self.entry_precio.pack(fill=X, pady=5)

        Label(frame_crud, text="Stock:").pack(anchor="w")
        self.entry_stock = Entry(frame_crud, width=22)
        self.entry_stock.pack(fill=X, pady=5)

        Button(frame_crud, text="Agregar Producto",
               width=ANCHO_BOTON,
               command=self._agregar).pack(pady=(10, 5))

        Button(frame_crud, text="Eliminar Producto",
               width=ANCHO_BOTON,
               command=self._eliminar).pack(pady=5)

        Button(frame_crud, text="Modificar",
               width=ANCHO_BOTON,
               command=self._abrir_ventana_modificar).pack(pady=5)

        Button(frame_crud, text="Generar CSV",
               width=ANCHO_BOTON,
               command=self._exportar_csv).pack(pady=5)

        Button(frame_crud, text="Importar CSV",
               width=ANCHO_BOTON,
               command=self._importar_csv).pack(pady=5)

        Button(frame_crud, text="Iniciar Servidor",
               width=ANCHO_BOTON,
               command=self._iniciar_servidor).pack(pady=5)

        Button(frame_crud, text="Detener Servidor",
               width=ANCHO_BOTON,
               command=self._detener_servidor).pack(pady=5)

    def _crear_tabla(self):
        """Crea la tabla (Treeview) donde se muestran los productos."""
        frame_table = Frame(self.root, padx=10, pady=10)
        frame_table.pack(side=TOP, fill=BOTH, expand=True)

        self.tabla = ttk.Treeview(frame_table, columns=COLUMNAS,
                                  show="headings")

        for col in COLUMNAS:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=ANCHOS_COLUMNAS[col],
                              anchor="center" if col != "nombre" else "w")

        scrollbar_y = ttk.Scrollbar(frame_table, orient="vertical",
                                    command=self.tabla.yview)
        scrollbar_x = ttk.Scrollbar(frame_table, orient="horizontal",
                                    command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scrollbar_y.set,
                             xscrollcommand=scrollbar_x.set)

        scrollbar_x.pack(side="bottom", fill=X)
        self.tabla.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar_y.pack(side=LEFT, fill=Y)

    def _limpiar_campos(self):
        """Limpia todos los campos del formulario de alta."""
        self.entry_codigo.delete(0, "end")
        self.entry_nombre.delete(0, "end")
        self.entry_precio.delete(0, "end")
        self.entry_stock.delete(0, "end")

    def _agregar(self):
        """Obtiene los datos ingresados en los campos y delega la operacion
        de alta al controlador. Si tiene exito, limpia los campos.
        """
        exito, mensaje = self.controlador.agregar(
            self.entry_codigo.get(),
            self.entry_nombre.get(),
            self.entry_precio.get(),
            self.entry_stock.get()
        )
        if exito:
            self._limpiar_campos()
        else:
            messagebox.showerror("Error", mensaje)

    def _eliminar(self):
        """Pide confirmacion al usuario y delega la eliminacion al
        controlador.
        """
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un producto")
            return

        nombre = self.tabla.item(seleccion, "values")[2]
        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            f"¿Está seguro de que desea eliminar '{nombre}'?"
        )
        if confirmar:
            exito, mensaje = self.controlador.eliminar(self.tabla)
            if not exito:
                messagebox.showerror("Error", mensaje)

    def _abrir_ventana_modificar(self):
        """Abre una ventana secundaria para modificar el producto
        seleccionado.
        """
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione un producto")
            return

        valores = self.tabla.item(seleccion, "values")

        ventana = Toplevel(self.root)
        ventana.title("Modificar Producto")
        ventana.geometry("350x280")
        ventana.resizable(False, False)

        campos = [
            ("Código:", valores[1]),
            ("Nombre:", valores[2]),
            ("Precio:", valores[3]),
            ("Stock:", valores[4]),
        ]
        variables = []
        for texto, valor in campos:
            var = StringVar(value=valor)
            Label(ventana, text=texto).pack(anchor="w", padx=15, pady=(8, 0))
            Entry(ventana, textvariable=var, width=35).pack(padx=15)
            variables.append(var)

        codigo, nombre, precio, stock = variables

        Button(
            ventana,
            text="Guardar",
            width=ANCHO_BOTON,
            command=lambda: self._guardar_modificacion(
                valores[0],
                codigo.get(),
                nombre.get(),
                precio.get(),
                stock.get(),
                ventana
            )
        ).pack(pady=15)

    def _guardar_modificacion(self, id_prod, codigo, nombre, precio, stock,
                               ventana):
        """Delega la modificacion al controlador y muestra el resultado.

        :param id_prod: ID del producto a modificar.
        :type id_prod: int
        :param codigo: Nuevo codigo del producto.
        :type codigo: str
        :param nombre: Nuevo nombre del producto.
        :type nombre: str
        :param precio: Nuevo precio.
        :type precio: str
        :param stock: Nueva cantidad en stock.
        :type stock: str
        :param ventana: Ventana de edicion que se cierra al confirmar.
        :type ventana: tkinter.Toplevel
        """
        exito, mensaje = self.controlador.modificar(
            id_prod, codigo, nombre, precio, stock, ventana
        )
        if not exito:
            messagebox.showerror("Error", mensaje)

    def _exportar_csv(self):
        """Delega la exportacion a CSV al controlador y muestra el resultado.
        """
        exito, mensaje = self.controlador.importar_csv()
        if exito:
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    def _importar_csv(self):
        """Abre un dialogo para seleccionar un CSV e importa los productos.
        """
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv")]
        )
        if not ruta:
            return

        exito, mensaje = self.controlador.importar_productos(ruta)
        if exito:
            messagebox.showinfo("Importación finalizada", mensaje)
        else:
            messagebox.showerror("Error", mensaje)

    def _iniciar_servidor(self):
        """Inicia el servidor de logs TCP."""
        servidor.iniciar()
        messagebox.showinfo("Servidor", "Servidor iniciado")

    def _detener_servidor(self):
        """Detiene el servidor de logs TCP."""
        servidor.detener()
        messagebox.showinfo("Servidor", "Servidor detenido")