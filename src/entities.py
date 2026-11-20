from abc import ABC, abstractmethod
from src.exceptions import ErrorDatosInvalidos


class ElementoBase(ABC):
    """Modelo general para los elementos principales del sistema."""

    def __init__(self, codigo: str):
        # Revisa que el código sea un texto y no esté vacío
        if not isinstance(codigo, str) or not codigo.strip():
            raise ErrorDatosInvalidos("El código del elemento no puede estar vacío.")
        # Guarda el código protegido
        self._codigo = codigo.strip()

    @property
    def codigo(self) -> str:
        """Entrega el código del elemento."""
        return self._codigo

    @abstractmethod
    def mostrar_resumen(self) -> str:
        """Obliga a cada elemento a explicar cómo se muestra en resumen."""
        pass


class Cliente(ElementoBase):
    """Representa a un cliente con sus datos protegidos y validados."""

    def __init__(self, codigo: str, nombre: str, documento: str, correo: str, telefono: str):
        # Inicializa el código usando la clase base
        super().__init__(codigo)
        # Asigna los datos pasando por las revisiones de cada propiedad
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        """Entrega el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Revisa que el nombre tenga al menos 3 letras."""
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ErrorDatosInvalidos("El nombre del cliente debe tener al menos 3 letras.")
        self._nombre = valor.strip()

    @property
    def documento(self) -> str:
        """Entrega el documento del cliente."""
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        """Revisa que el documento tenga solo números y mínimo 6 dígitos."""
        if not isinstance(valor, str) or not valor.strip().isdigit() or len(valor.strip()) < 6:
            raise ErrorDatosInvalidos(f"Documento no válido '{valor}': debe tener al menos 6 números.")
        self._documento = valor.strip()

    @property
    def correo(self) -> str:
        """Entrega el correo del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Revisa que el correo tenga '@' y un punto en el dominio."""
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise ErrorDatosInvalidos(f"Correo no válido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Entrega el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Revisa que el teléfono tenga entre 7 y 15 números."""
        limpio = valor.strip() if isinstance(valor, str) else ""
        if not limpio.isdigit() or not (7 <= len(limpio) <= 15):
            raise ErrorDatosInvalidos(f"Teléfono no válido '{valor}': debe tener entre 7 y 15 números.")
        self._telefono = limpio

    def mostrar_resumen(self) -> str:
        """Devuelve un resumen claro de los datos del cliente."""
        return (
            f"Cliente [{self.codigo}] {self.nombre} | "
            f"Documento: {self.documento} | Correo: {self.correo} | Teléfono: {self.telefono}"
        )