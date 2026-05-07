"""
Modulo de la capa de acceso a la base de datos.

Contiene la clase :class:`Abmc` que encapsula todas las operaciones de la 
logica de negocios sobre la tabla ``productos``.

Implementa el patron **Observador**: cuando los datos cambian, notifica
automaticamente a todos los observadores registrados.

Configura el sistema de logging de la aplicacion, escribiendo los registros
en consola y en el archivo ``stock.log``.
"""

import logging
from database import Producto
from peewee import IntegrityError
from decoradores import log_ingreso, log_eliminacion, log_actualizacion

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("stock.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

class Abmc:
    """Clase que gestiona las operaciones CRUD sobre la tabla productos.

    Actua como **sujeto** del patron Observador. Mantiene una lista de
    funciones observadoras que son invocadas automaticamente cada vez que
    los datos son modificados.
    """

    def __init__(self):
        """Inicializa el modelo con una lista de observadores vacia."""
        self._observadores = []

    def registrar_observador(self, observador):
        """Registra una funcion como observadora del modelo.

        La funcion sera llamada sin argumentos cada vez que los datos
        cambien como resultado de una operacion de alta, baja o modificacion.

        :param observador: Funcion a registrar como observadora.
        :type observador: callable
        """
        self._observadores.append(observador)

    def _notificar(self):
        """Notifica a todos los observadores registrados.

        Invoca cada funcion observadora en el orden en que fue registrada.
        """
        for observador in self._observadores:
            observador()

    @log_ingreso
    def agregar_producto(self, codigo, nombre, precio, stock):
        """Agrega un nuevo producto a la base de datos.

        :param codigo: Codigo unico del producto.
        :type codigo: str
        :param nombre: Nombre del producto.
        :type nombre: str
        :param precio: Precio del producto.
        :type precio: float
        :param stock: Cantidad en stock.
        :type stock: int
        :raises ValueError: Si el codigo ya existe en la base de datos.
        :raises RuntimeError: Si ocurre un error inesperado al insertar.
        """
        try:
            Producto.create(
                codigo=codigo,
                nombre=nombre,
                precio=precio,
                stock=stock
            )
            self._notificar()
        except IntegrityError:
            raise ValueError("El codigo ya existe")
        except Exception as error:
            raise RuntimeError(f"Error al agregar producto: {error}")

    @log_eliminacion
    def eliminar_producto(self, id_producto):
        """Elimina un producto de la base de datos por su ID.

        :param id_producto: ID del producto a eliminar.
        :type id_producto: int
        :raises RuntimeError: Si ocurre un error al intentar eliminar.
        """
        try:
            Producto.delete_by_id(id_producto)
            self._notificar()
        except Exception as error:
            raise RuntimeError(f"Error al eliminar producto: {error}")

    @log_actualizacion
    def modificar_producto(self, id_producto, codigo, nombre, precio, stock):
        """Modifica los datos de un producto existente.

        :param id_producto: ID del producto a modificar.
        :type id_producto: int
        :param codigo: Nuevo codigo del producto.
        :type codigo: str
        :param nombre: Nuevo nombre del producto.
        :type nombre: str
        :param precio: Nuevo precio del producto.
        :type precio: float
        :param stock: Nueva cantidad en stock.
        :type stock: int
        :raises RuntimeError: Si ocurre un error al intentar modificar.
        """
        try:
            Producto.update(
                codigo=codigo,
                nombre=nombre,
                precio=precio,
                stock=stock
            ).where(Producto.id == id_producto).execute()
            self._notificar()
        except Exception as error:
            raise RuntimeError(f"Error al modificar producto: {error}")

    def buscar_por_codigo(self, codigo):
        """Busca un producto por su codigo.

        :param codigo: Codigo del producto a buscar.
        :type codigo: str
        :return: Instancia del producto si existe, ``None`` si no se encuentra.
        :rtype: database.Producto or None
        """
        try:
            return Producto.get(Producto.codigo == codigo)
        except Producto.DoesNotExist:
            return None

    def obtener_productos(self):
        """Obtiene todos los productos ordenados por ID.

        :return: Lista de tuplas con los datos de cada producto.
        :rtype: list[tuple]
        :raises RuntimeError: Si ocurre un error al consultar la base de datos.
        """
        try:
            return [
                (p.id, p.codigo, p.nombre, f"{p.precio:.2f}", p.stock)
                for p in Producto.select().order_by(Producto.id)
            ]
        except Exception as error:
            raise RuntimeError(f"Error al obtener productos: {error}")