from src.entities import Cliente
from src.services import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from src.bookings import Reserva, AdministradorSoftwareFJ
from src.exceptions import registrador


def iniciar_pruebas() -> None:
    """Ejecuta 12 operaciones de prueba (válidas y con error) sin detener el programa."""
    registrador.info("=== INICIO DE PRUEBAS SOFTWARE FJ ===")
    print("Ejecutando pruebas de Software FJ...\n")

    admin = AdministradorSoftwareFJ()

    cliente1 = None
    cliente2 = None
    sala1 = None
    equipo1 = None
    asesoria1 = None
    reserva1 = None
    reserva2 = None

    # 1. Registro válido de cliente 1
    def prueba_01():
        nonlocal cliente1
        cliente1 = Cliente("CLI-1", "Laura Martínez", "10203040", "laura@correo.com", "3105551234")
        admin.agregar_cliente(cliente1)
        return cliente1.mostrar_resumen()

    admin.correr_operacion("Prueba 01 - Cliente válido 1", prueba_01)

    # 2. Registro válido de cliente 2
    def prueba_02():
        nonlocal cliente2
        cliente2 = Cliente("CLI-2", "Carlos Gómez", "80901020", "carlos@empresa.co", "3204449876")
        admin.agregar_cliente(cliente2)
        return cliente2.mostrar_resumen()

    admin.correr_operacion("Prueba 02 - Cliente válido 2", prueba_02)

    # 3. Registro inválido de cliente (correo sin arroba y documento corto)
    def prueba_03():
        cliente_malo = Cliente("CLI-3", "Ana", "123", "correo-malo", "3001112233")
        admin.agregar_cliente(cliente_malo)

    admin.correr_operacion("Prueba 03 - Cliente con datos inválidos", prueba_03)

    # 4. Creación válida de servicio de sala
    def prueba_04():
        nonlocal sala1
        sala1 = ReservaSala("SRV-1", "Sala Norte", 85000, capacidad_personas=12)
        admin.agregar_servicio(sala1)
        return sala1.describir()

    admin.correr_operacion("Prueba 04 - Crear servicio de sala", prueba_04)

    # 5. Creación válida de servicio de alquiler de equipo
    def prueba_05():
        nonlocal equipo1
        equipo1 = AlquilerEquipo("SRV-2", "Portátil Diseño", 45000, numero_serie="SER-9988")
        admin.agregar_servicio(equipo1)
        return equipo1.describir()

    admin.correr_operacion("Prueba 05 - Crear servicio de equipo", prueba_05)

    # 6. Creación válida de servicio de asesoría especializada
    def prueba_06():
        nonlocal asesoria1
        asesoria1 = AsesoriaEspecializada("SRV-3", "Soporte en la Nube", 120000, tema_experto="Arquitectura")
        admin.agregar_servicio(asesoria1)
        return asesoria1.describir()

    admin.correr_operacion("Prueba 06 - Crear servicio de asesoría", prueba_06)

    # 7. Creación inválida de servicio (precio negativo)
    def prueba_07():
        sala_mala = ReservaSala("SRV-4", "Sala Error", -20000, capacidad_personas=6)
        admin.agregar_servicio(sala_mala)

    admin.correr_operacion("Prueba 07 - Servicio con precio negativo", prueba_07)

    # 8. Reserva válida de sala con descuento y confirmación
    def prueba_08():
        nonlocal reserva1
        reserva1 = Reserva("RES-1", cliente1, sala1, horas=4, descuento_porcentaje=10.0, impuesto_porcentaje=19.0)
        admin.agregar_reserva(reserva1)
        reserva1.confirmar()
        return reserva1.mostrar_resumen()

    admin.correr_operacion("Prueba 08 - Reserva exitosa y confirmada", prueba_08)

    # 9. Intento de reservar la misma sala cuando ya está ocupada
    def prueba_09():
        reserva_repetida = Reserva("RES-2", cliente2, sala1, horas=2)
        admin.agregar_reserva(reserva_repetida)

    admin.correr_operacion("Prueba 09 - Reserva fallida por sala ocupada", prueba_09)

    # 10. Intento de alquilar equipo por menos horas del mínimo (1 hora < 2 horas)
    def prueba_10():
        reserva_corta = Reserva("RES-3", cliente2, equipo1, horas=1)
        admin.agregar_reserva(reserva_corta)

    admin.correr_operacion("Prueba 10 - Reserva fallida por pocas horas", prueba_10)

    # 11. Prueba de encadenamiento de errores al enviar un texto en el descuento
    def prueba_11():
        asesoria1.calcular_costo(horas=2, descuento_porcentaje="diez")  # type: ignore

    admin.correr_operacion("Prueba 11 - Encadenamiento de errores", prueba_11)

    # 12. Reserva confirmada y procesada, luego intento inválido de cancelarla
    def prueba_12():
        nonlocal reserva2
        reserva2 = Reserva("RES-4", cliente2, asesoria1, horas=3)
        admin.agregar_reserva(reserva2)
        reserva2.confirmar()
        reserva2.procesar()
        reserva2.cancelar()

    admin.correr_operacion("Prueba 12 - Reserva procesada y cancelación no permitida", prueba_12)

    admin.mostrar_todo()
    registrador.info("=== FIN DE PRUEBAS SOFTWARE FJ ===\n")


if __name__ == "__main__":
    iniciar_pruebas()