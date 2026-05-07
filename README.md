# Control de Stock

Aplicación de escritorio desarrollada en Python para gestionar un inventario de productos mediante un CRUD completo, aplicando arquitectura MVC y el patrón Observador.

---

## Vista previa

<img width="900" height="578" alt="vista_cs" src="https://github.com/user-attachments/assets/f92403f3-6770-43ef-9d1e-40f7d9b3944d" />

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
