import logging
from pathlib import Path

# Crea la carpeta 'logs' si todavía no existe
Path("logs").mkdir(exist_ok=True)

# Configura el archivo de texto donde se guardarán los eventos y errores
logging.basicConfig(
    filename="logs/sistema_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)

# Crea el registrador que usarán todos los demás archivos
registrador = logging.getLogger("SoftwareFJ")


class ErrorGeneralSistema(Exception):
    """Error base del sistema Software FJ."""
    pass


class ErrorDatosInvalidos(ErrorGeneralSistema):
    """Se usa cuando un dato no cumple las reglas o está vacío."""
    pass


class ErrorFaltaDato(ErrorGeneralSistema):
    """Se usa cuando falta un dato obligatorio."""
    pass


class ErrorServicioOcupado(ErrorGeneralSistema):
    """Se usa cuando el servicio no está disponible."""
    pass


class ErrorAccionNoPermitida(ErrorGeneralSistema):
    """Se usa cuando se intenta una acción que no corresponde al estado actual."""
    pass


class ErrorCalculoCosto(ErrorGeneralSistema):
    """Se usa cuando ocurre un problema al calcular el valor de un servicio."""
    pass