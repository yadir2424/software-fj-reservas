from abc import ABC, abstractmethod
from src.entities import ElementoBase
from src.exceptions import (
    ErrorCalculoCosto,
    ErrorDatosInvalidos,
    ErrorFaltaDato,
)


class Servicio(ElementoBase, ABC):
    """Modelo general para los servicios de Software FJ."""

    def __init__(self, codigo: str, nombre: str, precio_hora: float, disponible: bool = True):
        # Guarda el código del servicio
        super().__init__(codigo)
        # Revisa el nombre del servicio
        if not isinstance(nombre, str) or len(nombre.strip()) < 3:
            raise ErrorDatosInvalidos("El nombre del servicio debe tener al menos 3 letras.")
        # Revisa que el precio por hora sea mayor que cero
        if not isinstance(precio_hora, (int, float)) or precio_hora <= 0:
            raise ErrorDatosInvalidos("El precio por hora debe ser mayor que cero.")

        self._nombre = nombre.strip()
        self._precio_hora = float(precio_hora)
        self.disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        """Entrega el nombre del servicio."""
        return self._nombre

    @property
    def precio_hora(self) -> float:
        """Entrega el precio base por hora."""
        return self._precio_hora

    @abstractmethod
    def validar_datos_servicio(self, **datos) -> None:
        """Revisa los datos especiales que pide cada tipo de servicio."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Explica las características del servicio."""
        pass

    # Método con parámetros opcionales (permite calcular con o sin descuento, impuesto o recargo)
    def calcular_costo(
        self,
        horas: int,
        descuento_porcentaje: float = 0.0,
        impuesto_porcentaje: float = 19.0,
        recargo_adicional: float = 0.0,
    ) -> float:
        """Calcula el total a pagar según horas, descuento, impuesto y recargo opcional."""
        try:
            # Llama a la validación propia del tipo de servicio
            self.validar_datos_servicio(horas=horas)

            # Revisa que los porcentajes y recargos tengan sentido
            if not (0 <= descuento_porcentaje < 100):
                raise ErrorDatosInvalidos("El descuento debe estar entre 0 y menos de 100.")
            if impuesto_porcentaje < 0:
                raise ErrorDatosInvalidos("El impuesto no puede ser negativo.")
            if recargo_adicional < 0:
                raise ErrorDatosInvalidos("El recargo adicional no puede ser negativo.")

            # Calcula subtotal, aplica descuento, suma recargo y aplica impuesto
            subtotal = self._precio_hora * horas
            con_descuento = subtotal * (1 - descuento_porcentaje / 100.0)
            total = (con_descuento + recargo_adicional) * (1 + impuesto_porcentaje / 100.0)

            if total <= 0:
                raise ErrorCalculoCosto("El costo final debe ser mayor que cero.")

            return round(total, 2)

        except (ErrorDatosInvalidos, ErrorFaltaDato):
            # Vuelve a lanzar el error si ya es un error conocido de datos
            raise
        except Exception as error_origen:
            # Une el error nuevo con el error original para saber qué falló por dentro
            raise ErrorCalculoCosto(
                f"No se pudo calcular el costo del servicio '{self.nombre}'."
            ) from error_origen

    def mostrar_resumen(self) -> str:
        """Devuelve un resumen corto del servicio."""
        estado = "Disponible" if self.disponible else "Ocupado"
        return f"Servicio [{self.codigo}] {self.nombre} (${self._precio_hora:,.2f}/h) - {estado}"


class ReservaSala(Servicio):
    """Servicio para reservar salas de reuniones o trabajo."""

    def __init__(self, codigo: str, nombre: str, precio_hora: float, capacidad_personas: int, disponible: bool = True):
        super().__init__(codigo, nombre, precio_hora, disponible)
        if not isinstance(capacidad_personas, int) or capacidad_personas <= 0:
            raise ErrorDatosInvalidos("La capacidad de la sala debe ser un número entero mayor que cero.")
        self._capacidad_personas = capacidad_personas

    @property
    def capacidad_personas(self) -> int:
        """Entrega cuántas personas caben en la sala."""
        return self._capacidad_personas

    def validar_datos_servicio(self, **datos) -> None:
        """Revisa que la sala se reserve entre 1 y 12 horas completas."""
        if "horas" not in datos:
            raise ErrorFaltaDato("Falta indicar las horas para reservar la sala.")
        horas = datos["horas"]
        if not isinstance(horas, int) or not (1 <= horas <= 12):
            raise ErrorDatosInvalidos("La reserva de sala debe ser entre 1 y 12 horas completas.")

    def describir(self) -> str:
        """Describe la sala."""
        return (
            f"[Sala] {self.nombre} | Capacidad: {self._capacidad_personas} personas | "
            f"Precio: ${self._precio_hora:,.2f}/hora"
        )


class AlquilerEquipo(Servicio):
    """Servicio para alquilar equipos tecnológicos."""

    def __init__(self, codigo: str, nombre: str, precio_hora: float, numero_serie: str, disponible: bool = True):
        super().__init__(codigo, nombre, precio_hora, disponible)
        if not isinstance(numero_serie, str) or len(numero_serie.strip()) < 4:
            raise ErrorDatosInvalidos("El número de serie del equipo debe tener al menos 4 caracteres.")
        self._numero_serie = numero_serie.strip().upper()

    @property
    def numero_serie(self) -> str:
        """Entrega el número de serie del equipo."""
        return self._numero_serie

    def validar_datos_servicio(self, **datos) -> None:
        """Revisa que el alquiler de equipo sea mínimo de 2 horas."""
        if "horas" not in datos:
            raise ErrorFaltaDato("Falta indicar las horas para alquilar el equipo.")
        horas = datos["horas"]
        if not isinstance(horas, int) or horas < 2:
            raise ErrorDatosInvalidos("El alquiler de equipo requiere mínimo 2 horas completas.")

    def describir(self) -> str:
        """Describe el equipo."""
        return (
            f"[Equipo] {self.nombre} | Serie: {self._numero_serie} | "
            f"Precio: ${self._precio_hora:,.2f}/hora"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio para asesorías técnicas especializadas."""

    def __init__(self, codigo: str, nombre: str, precio_hora: float, tema_experto: str, disponible: bool = True):
        super().__init__(codigo, nombre, precio_hora, disponible)
        if not isinstance(tema_experto, str) or not tema_experto.strip():
            raise ErrorFaltaDato("Debe indicar el tema de la asesoría especializada.")
        self._tema_experto = tema_experto.strip()

    @property
    def tema_experto(self) -> str:
        """Entrega el tema de la asesoría."""
        return self._tema_experto

    def validar_datos_servicio(self, **datos) -> None:
        """Revisa que la asesoría dure entre 1 y 8 horas completas."""
        if "horas" not in datos:
            raise ErrorFaltaDato("Falta indicar las horas de la asesoría.")
        horas = datos["horas"]
        if not isinstance(horas, int) or not (1 <= horas <= 8):
            raise ErrorDatosInvalidos("La asesoría debe durar entre 1 y 8 horas completas.")

    def describir(self) -> str:
        """Describe la asesoría."""
        return (
            f"[Asesoría] {self.nombre} | Tema: {self._tema_experto} | "
            f"Precio: ${self._precio_hora:,.2f}/hora"
        )