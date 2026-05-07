"""
Modulo para la exportacion de datos a formato CSV.

Permite generar un reporte del inventario actual en un archivo ``stock.csv``
ubicado en el mismo directorio que el ejecutable de la aplicacion.
"""

import csv 

def generar_csv(productos):
    """Exporta la lista de productos a un archivo CSV.

    Guarda el archivo ``stock.csv`` en el directorio de trabajo actual.
    Si el archivo ya existe, lo sobreescribe.

    :param productos: Lista de tuplas con los datos de cada producto.
    :type productos: list[tuple]
    :return: True si el archivo se genero correctamente, False si hubo error.
    :rtype: bool
    """
    try:
        with open("stock.csv", "w", newline="", encoding="utf-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["ID", "Código", "Nombre", "Precio", "Stock"])
            writer.writerows(productos)
        return True
    except Exception as error:
        print(f"Error al generar CSV: {error}")
        return False