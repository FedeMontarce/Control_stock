Modulos
=======

La aplicacion esta organizada siguiendo el patron **MVC** combinado con el
patron **Observador**. A continuacion se documentan los modulos segun su
capa correspondiente.

----

Capa de datos
-------------

Estos modulos gestionan la conexion a la base de datos y las operaciones
sobre la tabla ``productos``.

Base de datos (``database``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: database
   :members:
   :undoc-members:
   :show-inheritance:

----

Modelo CRUD (``modelo``)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: modelo
   :members:
   :undoc-members:
   :show-inheritance:

----

Capa de logica
--------------

Contiene el controlador que actua como intermediario entre la vista y el
modelo, sin depender de ninguna biblioteca grafica.

Controlador (``controlador``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: controlador
   :members:
   :undoc-members:
   :show-inheritance:

----

Capa de presentacion
---------------------

Modulos responsables de la interfaz grafica y la interaccion con el usuario.

Vista (``vista``)
~~~~~~~~~~~~~~~~~~

.. automodule:: vista
   :members:
   :undoc-members:
   :show-inheritance:

----

Comunicacion TCP
----------------

Modulos que implementan la comunicacion cliente-servidor via sockets TCP.

Servidor (``servidor``)
~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: servidor
   :members:
   :undoc-members:
   :show-inheritance:

----

Cliente (``cliente``)
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: cliente
   :members:
   :undoc-members:
   :show-inheritance:

----

Utilidades
----------

Modulos auxiliares reutilizables que no pertenecen a ninguna capa especifica
del patron MVC.

Expresiones regulares (``mis_regex``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: mis_regex
   :members:
   :undoc-members:
   :show-inheritance:

----

Exportacion CSV (``importacion_csv``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: importacion_csv
   :members:
   :undoc-members:
   :show-inheritance:

----

Importacion CSV (``importacion_csv``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: importacion_csv
   :members:
   :undoc-members:
   :show-inheritance:

----

Decoradores (``decoradores``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: decoradores
   :members:
   :undoc-members:
   :show-inheritance: