Control de Stock
================

**Control de Stock** es una aplicacion de escritorio desarrollada en Python
que permite gestionar un inventario de productos mediante un CRUD completo
(Create, Read, Update, Delete).

Aplica una arquitectura **MVC** (Model – View – Controller) combinada con el
patron **Observador**, donde el modelo notifica automaticamente a la vista
ante cualquier cambio en los datos:

- El **modelo** se encarga del acceso y la manipulacion de los datos.
- La **vista** representa la interfaz grafica que el usuario visualiza.
- El **controlador** gestiona las solicitudes del usuario y coordina la logica
  del sistema sin depender de ninguna biblioteca de interfaz grafica.

Caracteristicas principales
-----------------------------

- Alta, baja, modificacion y consulta de productos.
- Validaciones mediante expresiones regulares centralizadas.
- Exportacion e importacion del inventario a formato CSV.
- Registro de operaciones CRUD mediante decoradores.
- Servidor de logs TCP por consola.
- Actualizacion automatica de la tabla via patron Observador.
- Interfaz grafica desarrollada con **Tkinter**.
- Base de datos gestionada con **Peewee ORM** sobre **SQLite**.
- Manejo de errores estructurado con excepciones tipadas.

Requisitos
-----------

- Python 3.10 o superior.
- Peewee ORM (``pip install peewee``).
- Furo para Sphinx (``pip install furo``), solo para generar la documentacion.

Contenido de la documentacion
-------------------------------

.. toctree::
   :maxdepth: 2
   :caption: Modulos

   modulos

Indices
-------

* :ref:`genindex`
* :ref:`modindex`