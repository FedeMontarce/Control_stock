"""
Modulo de configuracion de la base de datos.

Definimos la conexion a SQLite mediante Peewee ORM, el modelo de la tabla
``productos`` y la funcion de inicializacion de la base de datos.
"""

from peewee import SqliteDatabase, Model, AutoField, CharField, FloatField, \
IntegerField

db = SqliteDatabase("stock.db")
"""Instancia de la base de datos SQLite."""

class BaseModel(Model):
    """Modelo base del que heredan todos los modelos de la aplicacion."""
    class Meta:
        database = db

class Producto(BaseModel):
    """Representa un producto dentro del sistema de control de stock.

    :param id: Identificador unico autoincremental.
    :type id: int
    :param codigo: Codigo unico del producto.
    :type codigo: str
    :param nombre: Nombre del producto.
    :type nombre: str
    :param precio: Precio del producto.
    :type precio: float
    :param stock: Disponibilidad.
    :type stock: int
    """
    id = AutoField()
    codigo = CharField(unique=True)
    nombre = CharField()
    precio = FloatField()
    stock = IntegerField()

def inicializar_db():
    """Conecta a la base de datos y crea las tablas si no existen."""
    db.connect()
    db.create_tables([Producto])

def cerrar_db():
    """Cierra la conexion a la base de datos si esta abierta.
    
    Debe llamarse al cerrar la aplicacion para evitar bloqueos en el archivo
    ``stock.db``.
    """
    if not db.is_closed():
        db.close()