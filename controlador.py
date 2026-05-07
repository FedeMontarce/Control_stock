"""
Modulo del controlador (patron MVC).

Actua como intermediario entre la :mod:`vista` y el :mod:`modelo`.
Se encarga de validar los datos ingresados por el usuario y de delegar
las operaciones al modelo correspondiente.

El controlador no depende de ninguna biblioteca de interfaz grafica.
Retorna tuplas ``(exito, mensaje)`` que la vista interpreta para mostrar
los resultados al usuario.
"""

import re
from modelo import Abmc
from mis_regex import patron_producto, precio_producto, stock_producto
from generar_csv import generar_csv
from importacion_csv import importar_csv

class Controlador:
    """Clase que gestiona la logica entre la Vista y el Modelo."""

    def __init__(self):
        """Inicializa el controlador creando una instancia del modelo."""
        self.modelo = Abmc()

    def registrar_observador(self, observador):
        """Delega el registro de un observador al modelo.

        :param observador: Funcion a registrar como observadora.
        :type observador: callable
        """
        self.modelo.registrar_observador(observador)

    def validar_producto(self, codigo, nombre, precio, stock):
        """Valida los datos de un producto.

        :param codigo: Codigo del producto.
        :type codigo: str
        :param nombre: Nombre del producto.
        :type nombre: str
        :param precio: Precio del producto.
        :type precio: str
        :param stock: Cantidad en stock.
        :type stock: str
        :return: Mensaje de error si la validacion falla, o ``None`` si es
         valido.
        :rtype: str or None
        """
        if not codigo.strip():
            return "El codigo es obligatorio"

        if not re.match(patron_producto, nombre.strip()):
            return "Producto invalido"

        if not re.match(precio_producto, precio):
            return "Precio invalido"

        if not re.match(stock_producto, stock):
            return "Stock invalido"

        return None

    def actualizar(self, tabla):
        """Recarga los datos de la tabla visual con los productos de la base
        de datos.

        :param tabla: Widget Treeview de Tkinter donde se muestran los
         productos.
        :type tabla: tkinter.ttk.Treeview
        :return: Tupla indicando exito y un mensaje descriptivo.
        :rtype: tuple[bool, str]
        """
        try:
            tabla.delete(*tabla.get_children())
            for fila in self.modelo.obtener_productos():
                tabla.insert("", "end", values=fila)
            return True, ""
        except RuntimeError as e:
            return False, str(e)

    def agregar(self, codigo, nombre, precio, stock):
        """Valida y agrega un nuevo producto a la base de datos.

        La tabla se actualiza automaticamente via el patron Observador.

        :param codigo: Codigo del producto.
        :type codigo: str
        :param nombre: Nombre del producto.
        :type nombre: str
        :param precio: Precio del producto.
        :type precio: str
        :param stock: Cantidad en stock.
        :type stock: str
        :return: Tupla indicando exito y un mensaje descriptivo.
        :rtype: tuple[bool, str]
        """
        error = self.validar_producto(codigo, nombre, precio, stock)
        if error:
            return False, error

        try:
            self.modelo.agregar_producto(codigo, nombre, float(precio),
                                         int(stock))
            return True, "Producto agregado correctamente"
        except (ValueError, RuntimeError) as e:
            return False, str(e)

    def eliminar(self, tabla):
        """Elimina el producto seleccionado en la tabla visual.

        La tabla se actualiza automaticamente via el patron Observador.

        :param tabla: Widget Treeview con el producto seleccionado.
        :type tabla: tkinter.ttk.Treeview
        :return: Tupla indicando exito y un mensaje descriptivo.
        :rtype: tuple[bool, str]
        """
        try:
            seleccion = tabla.selection()
            id_producto = tabla.item(seleccion, "values")[0]
            self.modelo.eliminar_producto(id_producto)
            return True, "Producto eliminado correctamente"
        except RuntimeError as e:
            return False, str(e)

    def modificar(self, id_prod, codigo, nombre, precio, stock, ventana):
        """Valida y actualiza los cambios sobre un producto existente.

        La tabla se actualiza automaticamente via el patron Observador.

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
        :return: Tupla indicando exito y un mensaje descriptivo.
        :rtype: tuple[bool, str]
        """
        error = self.validar_producto(codigo, nombre, precio, stock)
        if error:
            return False, error

        try:
            self.modelo.modificar_producto(id_prod, codigo, nombre,
                                           float(precio), int(stock))
            ventana.destroy()
            return True, "Producto modificado correctamente"
        except RuntimeError as e:
            return False, str(e)

    def importar_csv(self):
        """Exporta el inventario actual a un archivo CSV y lo guarda en el
        directorio.

        :return: Tupla indicando exito y un mensaje descriptivo.
        :rtype: tuple[bool, str]
        """
        try:
            productos = self.modelo.obtener_productos()
        except RuntimeError as e:
            return False, str(e)

        if generar_csv(productos):
            return True, "Reporte generado con exito"
        return False, "No se pudo generar el CSV"

    def importar_productos(self, ruta):
        """Importa productos desde un archivo CSV.

        Los productos nuevos se insertan y los existentes suman su stock.
        Al finalizar retorna un resumen de la operacion.

        :param ruta: Ruta al archivo CSV a importar.
        :type ruta: str
        :return: Tupla indicando exito y un mensaje descriptivo.
        :rtype: tuple[bool, str]
        """
        insertados, actualizados, fallidos = importar_csv(ruta, self.modelo)
        total = insertados + actualizados

        if total == 0 and fallidos == 0:
            return False, "El archivo CSV esta vacio o no tiene datos validos"

        mensaje = (f"Importacion finalizada:\n"
                   f"  • {insertados} producto(s) nuevo(s)\n"
                   f"  • {actualizados} stock(s) actualizado(s)\n"
                   f"  • {fallidos} fila(s) con errores")
        return True, mensaje