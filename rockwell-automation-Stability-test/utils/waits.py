"""
Utilidades para implementar estrategias de espera personalizadas.
Permite esperar a que se cumplan condiciones específicas en la página.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver

from utils.logger import logger
from config.config import DEFAULT_TIMEOUT

def wait_for_page_load(driver: WebDriver, timeout=DEFAULT_TIMEOUT):
    """
    Espera a que la página termine de cargar (document.readyState === 'complete').
    
    Args:
        driver (WebDriver): Instancia del WebDriver
        timeout (int, optional): Tiempo máximo de espera en segundos
    """
    logger.debug("Esperando a que la página termine de cargar")
    old_page = driver.find_element_by_tag_name('html')
    
    def check_page_loaded(driver):
        new_page = driver.find_element_by_tag_name('html')
        return new_page.id != old_page.id
    
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
    except TimeoutException:
        logger.error(f"Página no cargó completamente después de {timeout} segundos")
        raise

def wait_for_url_contains(driver: WebDriver, partial_url: str, timeout=DEFAULT_TIMEOUT):
    """
    Espera a que la URL actual contenga una subcadena específica.
    
    Args:
        driver (WebDriver): Instancia del WebDriver
        partial_url (str): Subcadena que debe contener la URL
        timeout (int, optional): Tiempo máximo de espera en segundos
        
    Returns:
        bool: True si la URL contiene la subcadena, False en caso contrario
    """
    logger.debug(f"Esperando a que la URL contenga: {partial_url}")
    try:
        return WebDriverWait(driver, timeout).until(
            EC.url_contains(partial_url)
        )
    except TimeoutException:
        logger.warning(f"La URL no contiene '{partial_url}' después de {timeout} segundos")
        current_url = driver.current_url
        logger.warning(f"URL actual: {current_url}")
        return False

def wait_for_text_to_be_present(driver: WebDriver, locator, text: str, timeout=DEFAULT_TIMEOUT):
    """
    Espera a que un elemento contenga un texto específico.
    
    Args:
        driver (WebDriver): Instancia del WebDriver
        locator (tuple): Tuple que contiene el tipo y valor del localizador
        text (str): Texto que debe contener el elemento
        timeout (int, optional): Tiempo máximo de espera en segundos
        
    Returns:
        bool: True si el elemento contiene el texto, False en caso contrario
    """
    logger.debug(f"Esperando a que el elemento {locator} contenga el texto: {text}")
    try:
        return WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
    except TimeoutException:
        logger.warning(f"El elemento {locator} no contiene el texto '{text}' después de {timeout} segundos")
        return False

def wait_for_element_attribute(driver: WebDriver, locator, attribute: str, value: str, timeout=DEFAULT_TIMEOUT):
    """
    Espera a que un elemento tenga un atributo con un valor específico.
    
    Args:
        driver (WebDriver): Instancia del WebDriver
        locator (tuple): Tuple que contiene el tipo y valor del localizador
        attribute (str): Nombre del atributo
        value (str): Valor esperado del atributo
        timeout (int, optional): Tiempo máximo de espera en segundos
        
    Returns:
        bool: True si el elemento tiene el atributo con el valor especificado, False en caso contrario
    """
    logger.debug(f"Esperando a que el elemento {locator} tenga el atributo {attribute}={value}")
    try:
        return WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element_attribute(locator, attribute, value)
        )
    except TimeoutException:
        logger.warning(f"El elemento {locator} no tiene el atributo {attribute}={value} después de {timeout} segundos")
        return False