# Sistema de Gestión de Reservas - Software FJ

Proyecto desarrollado en Python aplicando Programación Orientada a Objetos (POO) y manejo estructurado de excepciones, sin uso de bases de datos, para gestionar clientes, servicios y reservas de la empresa Software FJ.

UNIVERSIDAD UNAD
**Curso:** Programación (213023)  
**Estudiante:** Nelson Yadir Forigua Parra (Desarrollo individual)

---

## Estructura del Proyecto

* `main.py`: Archivo principal que ejecuta las pruebas del sistema (operaciones válidas e inválidas) sin detener la ejecución.
* `src/__init__.py`: Inicializa el paquete `src`.
* `src/exceptions.py`: Define las excepciones personalizadas del sistema y configura el registro de eventos y errores en `logs/sistema_fj.log`.
* `src/entities.py`: Contiene la clase abstracta `ElementoBase` y la clase `Cliente` con encapsulación y validación de datos.
* `src/services.py`: Contiene la clase abstracta `Servicio` y las clases hijas `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`.
* `src/bookings.py`: Contiene la clase `Reserva` (con control de estados: pendiente, confirmada, procesada y cancelada) y `AdministradorSoftwareFJ` para gestionar las listas en memoria.

---

## Cómo ejecutar el programa

1. Descarga o clona este repositorio en tu computador.
2. Abre una terminal dentro de la carpeta principal del proyecto.
3. Ejecuta el siguiente comando:

```bash
python main.py
