from typing import List
from src.entities import Cliente, ElementoBase
from src.services import Servicio
from src.exceptions import (
    ErrorAccionNoPermitida,
    ErrorDatosInvalidos,
    ErrorGeneralSistema,
    ErrorServicioOcupado,
    registrador,
)


class Reserva(ElementoBase):
    """Une un cliente con un servicio por cierta cantidad de horas y controla su estado."""

    def __init__(
        self,
        codigo: str,
        cliente: Cliente,
        servicio: Servicio,
        horas: int,
        descuento_porcentaje: float = 0.0,
        impuesto_porcentaje: float = 19.0,
    ):
        super().__init__(codigo)

        # Revisa que el cliente y el servicio correspondan a sus clases correctas
        if not isinstance(cliente, Cliente):
            raise ErrorDatosInvalidos("Debe asignar un cliente válido a la reserva.")
        if not isinstance(servicio, Servicio):
            raise ErrorDatosInvalidos("Debe asignar un servicio válido a la reserva.")
        # Revisa que el servicio esté libre
        if not servicio.disponible:
            raise ErrorServicioOcupado(f"El servicio '{servicio.nombre}' no está disponible.")

        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = "PENDIENTE"
        # Calcula el valor total usando el método del servicio
        self._valor_total = servicio.calcular_costo(
            horas=horas,
            descuento_porcentaje=descuento_porcentaje,
            impuesto_porcentaje=impuesto_porcentaje,
        )

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def valor_total(self) -> float:
        return self._valor_total

    def confirmar(self) -> None:
        """Confirma la reserva y marca el servicio como ocupado."""
        if self._estado != "PENDIENTE":
            raise ErrorAccionNoPermitida(
                f"Solo se puede confirmar una reserva PENDIENTE. Estado actual: '{self._estado}'."
            )
        if not self._servicio.disponible:
            raise ErrorServicioOcupado(f"El servicio '{self._servicio.nombre}' ya fue ocupado.")
        self._estado = "CONFIRMADA"
        self._servicio.disponible = False

    def procesar(self) -> None:
        """Marca la reserva confirmada como realizada y libera el servicio."""
        if self._estado != "CONFIRMADA":
            raise ErrorAccionNoPermitida(
                f"Solo se puede procesar una reserva CONFIRMADA. Estado actual: '{self._estado}'."
            )
        self._estado = "PROCESADA"
        self._servicio.disponible = True

    def cancelar(self) -> None:
        """Cancela la reserva si no ha sido procesada ni cancelada antes."""
        if self._estado in ("CANCELADA", "PROCESADA"):
            raise ErrorAccionNoPermitida(
                f"No se puede cancelar una reserva en estado '{self._estado}'."
            )
        if self._estado == "CONFIRMADA":
            self._servicio.disponible = True
        self._estado = "CANCELADA"

    def mostrar_resumen(self) -> str:
        """Devuelve un resumen completo de la reserva."""
        return (
            f"Reserva [{self.codigo}] | Estado: {self._estado} | "
            f"Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} | "
            f"Horas: {self._horas}h | Total: ${self._valor_total:,.2f}"
        )


class AdministradorSoftwareFJ:
    """Guarda clientes, servicios y reservas en listas mientras el programa está abierto."""

    def __init__(self):
        # Listas en memoria (sin usar base de datos)
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []

    def agregar_cliente(self, cliente: Cliente) -> None:
        """Guarda un cliente nuevo si no repite código ni documento."""
        for existente in self._clientes:
            if existente.codigo == cliente.codigo or existente.documento == cliente.documento:
                raise ErrorAccionNoPermitida(
                    f"Ya existe un cliente con código '{cliente.codigo}' o documento '{cliente.documento}'."
                )
        self._clientes.append(cliente)

    def agregar_servicio(self, servicio: Servicio) -> None:
        """Guarda un servicio nuevo si no repite código."""
        for existente in self._servicios:
            if existente.codigo == servicio.codigo:
                raise ErrorAccionNoPermitida(f"Ya existe un servicio con código '{servicio.codigo}'.")
        self._servicios.append(servicio)

    def agregar_reserva(self, reserva: Reserva) -> None:
        """Guarda una reserva nueva si no repite código."""
        for existente in self._reservas:
            if existente.codigo == reserva.codigo:
                raise ErrorAccionNoPermitida(f"Ya existe una reserva con código '{reserva.codigo}'.")
        self._reservas.append(reserva)

    def correr_operacion(self, nombre_prueba: str, accion) -> bool:
        """Ejecuta una operación protegida para que los errores queden anotados y el programa siga."""
        try:
            resultado = accion()
        except ErrorGeneralSistema as err:
            # Muestra el error original si hubo encadenamiento de errores
            origen = f" | Motivo inicial: {repr(err.__cause__)}" if err.__cause__ else ""
            texto = f"[ERROR CONTROLADO] {nombre_prueba} -> {type(err).__name__}: {err}{origen}"
            registrador.error(texto)
            print(texto)
            return False
        except Exception as err:
            texto = f"[ERROR NO PREVISTO] {nombre_prueba} -> {type(err).__name__}: {err}"
            registrador.exception(texto)
            print(texto)
            return False
        else:
            # Se ejecuta solo cuando la operación salió bien sin errores
            extra = f" -> {resultado}" if resultado else ""
            texto = f"[CORRECTO] {nombre_prueba}{extra}"
            registrador.info(texto)
            print(texto)
            return True
        finally:
            # Se ejecuta siempre al terminar la prueba, haya error o no
            registrador.info(f"[REGISTRO] Terminó la revisión de: {nombre_prueba}")

    def mostrar_todo(self) -> None:
        """Imprime el estado final de lo guardado en las listas."""
        print("\n" + "=" * 70)
        print("RESUMEN FINAL DEL SISTEMA - SOFTWARE FJ")
        print("=" * 70)
        print(f"Clientes registrados ({len(self._clientes)}):")
        for c in self._clientes:
            print("  *", c.mostrar_resumen())

        print(f"\nServicios registrados ({len(self._servicios)}):")
        for s in self._servicios:
            estado = "Disponible" if s.disponible else "Ocupado"
            print(f"  * {s.describir()} | Estado: {estado}")

        print(f"\nReservas registradas ({len(self._reservas)}):")
        for r in self._reservas:
            print("  *", r.mostrar_resumen())
        print("=" * 70)