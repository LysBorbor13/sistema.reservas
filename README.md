#  Sistema de Reservas en Python

Este proyecto implementa un sistema completo para gestionar **clientes** y **reservas**, utilizando estructuras de datos como **listas**, **diccionarios (HashMap)** y archivos para **persistencia**.

El sistema permite registrar, editar, buscar y listar clientes y reservas, además de realizar **reportes automáticos**.

---

##  Características principales

###  Gestión de clientes
- Registrar cliente  
- Editar cliente  
- Buscar cliente  
- Listar todos los clientes  

###  Gestión de reservas
- Registrar reserva  
- Editar reserva  
- Buscar reserva  
- Listar reservas ordenadas por fecha  
- Eliminar reserva  

###  Reportes
- Reservas por cliente  
- Reservas por fecha  
- Reporte de totales (clientes y reservas)  

###  Persistencia de datos
El sistema guarda automáticamente:
- `clientes.json`
- `reservas.json`

De esta forma, **el programa conserva los datos incluso después de cerrarse**.

---

##  Tecnologías utilizadas

- Python 3.10+
- VS Code
- Git / GitHub
- Estructuras de Datos:
  - Listas
  - Diccionarios (HashMap)
  - Ordenamiento (sorted con lambda)

---

##  Estructura del proyecto

