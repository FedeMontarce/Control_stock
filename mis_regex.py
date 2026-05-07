"""
Modulo de expresiones regulares para la validacion de datos del formulario.

Estas expresiones son utilizadas en el controlador para verificar que los 
valores ingresados por el usuario tengan el formato correcto.
"""

patron_producto = r"^[A-Za-z0-9]+([A-Za-z0-9 ]*[A-Za-z0-9]+)?$"
"""Valida el nombre de un producto.

Acepta letras (mayusculas y minusculas), digitos y espacios intermedios.
No permite cadenas vacias, ni que empiecen o terminen con espacio.
"""

precio_producto = r'^[1-9]\d*(\.\d{1,2})?$'
"""Valida el precio de un producto.

Acepta numeros enteros o decimales con hasta dos cifras decimales.
El precio debe ser mayor a cero (no acepta 0 ni 0.00).
"""

stock_producto = r'^\d+$'
"""Valida la cantidad de stock de un producto.

Acepta enteros positivos incluyendo cero.
Un stock de 0 indica que el producto existe pero esta agotado.
"""