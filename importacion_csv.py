"""
Modulo para la importacion de productos desde un archivo CSV.

Lee un archivo CSV con el formato exportado por la aplicacion e intenta
insertar cada producto. Si el codigo ya existe, suma el stock al existente.
Al finalizar reporta cuantos productos se importaron, actualizaron y fallaron.
"""

import csv
import logging
import re
from mis_regex import patron_producto, precio_producto, stock_producto

logger = logging.getLogger("stock")

def importar_csv(ruta, modelo):
    """Importa productos desde un archivo CSV hacia la base de datos.

    Por cada fila del archivo:

    - Si el codigo no existe, inserta el producto.
    - Si el codigo ya existe, suma el stock al registro existente.
    - Si los datos son invalidos, cuenta la fila como fallida.

    :param ruta: Ruta al archivo CSV a importar.
    :type ruta: str
    :param modelo: Instancia del modelo CRUD.
    :type modelo: modelo.Abmc
    :return: Tupla con la cantidad de insertados, actualizados y fallidos.
    :rtype: tuple[int, int, int]
    """
    insertados = 0
    actualizados = 0
    fallidos = 0

    try:
        with open(ruta, newline="", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            for fila in reader:
                codigo = fila.get("Código", "").strip()
                nombre = fila.get("Nombre", "").strip()
                precio = fila.get("Precio", "").strip()
                stock = fila.get("Stock", "").strip()

                if not _validar_fila(codigo, nombre, precio, stock):
                    logger.warning("Fila invalida omitida: %s", fila)
                    fallidos += 1
                    continue
                
                try:
                    producto = modelo.buscar_por_codigo(codigo)
                    if producto:
                        nuevo_stock = producto.stock + int(stock)
                        modelo.modificar_producto(
                            producto.id, codigo, nombre,
                            float(precio), nuevo_stock
                        )
                        actualizados += 1
                    else:
                        modelo.agregar_producto(
                            codigo, nombre, float(precio), int(stock)
                        )
                        insertados += 1
                except Exception as e:
                    logger.error("Error al procesar fila %s: %s", fila, e)
                    fallidos += 1

    except Exception as error:
        logger.error("Error al leer el archivo CSV: %s", error)
        return 0, 0, 0

    logger.info(
        "Importacion finalizada: %d insertados, %d actualizados, %d fallidos",
        insertados, actualizados, fallidos
    )
    return insertados, actualizados, fallidos


def _validar_fila(codigo, nombre, precio, stock):
    """Valida los campos de una fila del CSV.

    :param codigo: Codigo del producto.
    :type codigo: str
    :param nombre: Nombre del producto.
    :type nombre: str
    :param precio: Precio del producto.
    :type precio: str
    :param stock: Cantidad en stock.
    :type stock: str
    :return: True si todos los campos son validos, False en caso contrario.
    :rtype: bool
    """
    if not codigo:
        return False
    if not re.match(patron_producto, nombre):
        return False
    if not re.match(precio_producto, precio):
        return False
    if not re.match(stock_producto, stock):
        return False
    return True