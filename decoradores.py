"""
Modulo de decoradores para el registro de operaciones CRUD.
 
Los decoradores de este modulo se aplican sobre los metodos del
:mod:`modelo` e informan por consola cada vez que se produce un
ingreso, eliminacion o actualizacion de un registro en la base de datos.
"""
 
from functools import wraps
 
def log_operacion(mensaje):
    """Decorador parametrizable que informa por consola una operacion CRUD.
 
    :param mensaje: Etiqueta que identifica el tipo de operacion.
    :type mensaje: str
    :return: Decorador listo para aplicar sobre una funcion.
    :rtype: callable
    """
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            resultado = func(*args, **kwargs)
            print(f"[{mensaje}] de registro")
            return resultado
        return wrapper
    return decorador
 
 
log_ingreso = log_operacion("INGRESO")
"""Informa el ingreso de un nuevo registro."""
 
log_eliminacion = log_operacion("ELIMINACION")
"""Informa la eliminacion de un registro."""
 
log_actualizacion = log_operacion("ACTUALIZACION")
"""Informa la actualizacion de un registro."""