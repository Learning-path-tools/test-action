"""
tomamos las capturas si falla
Configuración y fixtures de pytest para el framework de automatización.
Este archivo se carga automáticamente por pytest.
"""
import re
from datetime import datetime
import pytest
import os
import datetime
from selenium.webdriver.remote.webdriver import WebDriver

from config.config import DEFAULT_BROWSER, DEFAULT_TIMEOUT, BASE_URLS, SCREENSHOTS_DIR
from utils.driver_factory import DriverFactory
from utils.logger import logger,setup_logger

def pytest_addoption(parser):
    """
    Agrega opciones de línea de comandos para pytest.
    """
    parser.addoption(
        "--url-index", 
        action="store", 
        default=None, 
        type=int,
        help="Índice de la URL a probar (1-19). Si no se especifica, se usará la URL predeterminada."
    )
    parser.addoption(
        "--all-urls", 
        action="store_true", 
        default=False,
        help="Ejecutar pruebas en todas las URLs disponibles."
    )

def pytest_generate_tests(metafunc):
    """
    Genera casos de prueba dinámicamente basados en las opciones de pytest.
    """
    # Si la prueba requiere el parámetro 'base_url' y no está ya parametrizada
    if "base_url" in metafunc.fixturenames and not hasattr(metafunc.function, "parametrize"):
        url_index = metafunc.config.getoption("url_index")
        all_urls = metafunc.config.getoption("all_urls")
        
        if all_urls:
            # Ejecutar la prueba con todas las URLs
            metafunc.parametrize("base_url", BASE_URLS)
        elif url_index is not None and 0 <= url_index < len(BASE_URLS):
            # Ejecutar la prueba con una URL específica
            metafunc.parametrize("base_url", [BASE_URLS[url_index]])
        else:
            # Ejecutar la prueba con la URL predeterminada
            metafunc.parametrize("base_url", [BASE_URLS[0]])

@pytest.fixture(scope="function")
def driver():
    """
    Script que que proporciona una instancia del WebDriver para cada función de test y corra mas rapido.
    
    Yields:
        WebDriver: Instancia del WebDriver configurada
    """
    logger.info(f"Iniciando navegador: {DEFAULT_BROWSER}")
    
    # Crear instancia del driver
    driver = DriverFactory.get_driver(DEFAULT_BROWSER)
    
    # Ceder el control al test
    yield driver
    
    # Teardown: cerrar el navegador
    logger.info("Cerrando navegador")
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para procesar el resultado de cada test y capturar screenshots en caso de fallos.
    """
    # Ejecutar todos los demás hooks para obtener el reporte
    outcome = yield
    rep = outcome.get_result()
    
    # Verificar si estamos en la fase de ejecución (setup/call/teardown)
    if rep.when == "call" and rep.failed:
        # Capturar screenshot si el test falló
        try:
            driver = item.funcargs.get("driver")
            if driver:
                # Obtener información de la URL base para incluirla en el nombre
                base_url = item.funcargs.get("base_url", "unknown")
                url_info = base_url.split("//")[1].split(".")[0]  # Extrae 'ftdspprod001' de la URL
                take_screenshot(driver, f"FAILED_{item.name}_{url_info}")
        except Exception as e:
            logger.error(f"Error al capturar screenshot: {e}")

def take_screenshot(driver: WebDriver, test_name: str):
    """
    Captura un screenshot del navegador actual.
    
    Args:
        driver (WebDriver): Instancia del WebDriver
        test_name (str): Nombre del test
    """
    
    # Obtener la URL actual para determinar el servidor
    current_url = driver.current_url
    
    # Extraer el identificador del servidor (ftdspprod001, ftdspprod002, etc.)
    server_match = re.search(r'ftdspprod\d{3}', current_url)
    server_id = server_match.group(0)#' if server_match else "unknown_server"'
    
    # Crear directorio específico para este servidor
    server_screenshots_dir = os.path.join(SCREENSHOTS_DIR, server_id)
    os.makedirs(server_screenshots_dir, exist_ok=True)
    
    # Generar nombre de archivo con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{server_screenshots_dir}/{test_name}_{server_id}.png"
    
    logger.info(f"Capturando screenshot: {filename}")
    driver.save_screenshot(filename)
    
@pytest.fixture(scope="function")
def setup(driver, base_url):
    """
    Fixture que configura el driver con una URL base específica.
    
    Args:
        driver: Instancia del WebDriver (desde el fixture 'driver')
        base_url: URL base a la que se navegará
        
    Returns:
        tuple: (WebDriver, str) - El driver configurado y la URL base
    """
    # Extraer identificador de la URL (por ejemplo, 'ftdspprod001')
    import re
    server_match = re.search(r'ftdspprod\d{3}', base_url)
    url_id = server_match.group(0) if server_match else base_url
    
    # Actualizar logger con el identificador de URL
    global logger
    logger = setup_logger(url_id)
    
    logger.info("📋 Configuración de la prueba")
    logger.info(f"  - Navegador: {DEFAULT_BROWSER}")
    logger.info(f"  - URL: {base_url}")
    logger.info(f"  - Identificador de servidor: {url_id}")
    logger.info(f"  - Timeout predeterminado: {DEFAULT_TIMEOUT} segundos")
    
    logger.info(f"🌐 Navegando a la URL base: {base_url}")
    try:
        driver.get(base_url)
        logger.info("✅ Navegación completada correctamente")
    except Exception as e:
        logger.error(f"❌ Error al navegar a {base_url}: {e}")
        raise
    
    return driver, base_url