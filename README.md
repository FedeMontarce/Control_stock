# Control de Stock

Aplicación de escritorio desarrollada en Python para gestionar un inventario de productos mediante un CRUD completo, aplicando arquitectura MVC y el patrón Observador.

---

## Vista previa

<img width="900" height="578" alt="image" src="https://github.com/user-attachments/assets/6b001730-9315-46b6-842e-af2bdaa3a62f" />

---

## Arquitectura

El proyecto sigue el patrón **MVC** combinado con el patrón **Observador**, donde el modelo notifica automáticamente a la vista ante cualquier cambio en los datos, sin intervención del controlador.

---

## Funcionalidades

- Alta, baja, modificación y consulta de productos
- Exportación e importación de inventario en formato CSV
- Registro de operaciones CRUD mediante decoradores
- Servidor de logs TCP por consola
- Validaciones de formulario con expresiones regulares

---
