"""
Configuración del sistema de logging para el framework.
Proporciona funciones para registrar información, advertencias y errores.
"""
import re
import os
import logging
from datetime import datetime
from config.config import REPORTS_DIR

def setup_logger(url_identifier=None):
    """
    Configura y retorna un logger para el framework.
    
    Args:
        url_identifier (str, optional): Identificador de la URL para organizar logs
        
    Returns:
        Logger: Instancia configurada del logger
    """
    # Crear directorio de logs si no existe
    log_dir = os.path.join(REPORTS_DIR, "logs")
    
    # Si tenemos un identificador de URL, crear subdirectorio específico
    if url_identifier:
        # Extraer solo el nombre del servidor si es una URL completa
        if "//" in url_identifier:
            server_match = re.search(r'ftdspprod\d{3}', url_identifier)
            url_identifier = server_match.group(0) if server_match else url_identifier
        
        log_dir = os.path.join(log_dir, url_identifier)
    
    os.makedirs(log_dir, exist_ok=True)
    
    # Formato del nombre del archivo de log con fecha y hora
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"test_run_{timestamp}.log")
    
    # Configurar el logger
    logger = logging.getLogger("selenium_framework")
    
    # Establecer el nivel de logging a DEBUG para más detalle
    logger.setLevel(logging.DEBUG)
    
    # Evitar duplicación de handlers
    if logger.handlers:
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
    
    # Handler para escribir en archivo (nivel DEBUG)
    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s", 
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    
    # Handler para escribir en consola (nivel INFO o DEBUG)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S")
    console_handler.setFormatter(console_formatter)
    
    # Establecer nivel DEBUG en la consola para mostrar todos los pasos
    console_handler.setLevel(logging.DEBUG)
    
    logger.addHandler(console_handler)
    
    # Mensaje inicial
    logger.info(f"=== Iniciando sesión de pruebas para {url_identifier if url_identifier else 'servidor predeterminado'} ===")
    
    return logger

# Instancia global del logger
logger = setup_logger()