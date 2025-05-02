"""
Clase base para todos los page objects.
Contiene métodos comunes utilizados en múltiples páginas.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple, Optional
import time
from datetime import datetime
import os
import re
from config.config import SCREENSHOTS_DIR

from config.config import DEFAULT_TIMEOUT
from utils.logger import logger


class BasePage:
    """
    Clase base que todas las page objects deben heredar.
    Proporciona métodos comunes para interactuar con elementos de la página.
    """
    
    def __init__(self, driver, base_url=None):
        """
        Inicializa el page object.
        
        Args:
            driver: Instancia del WebDriver
            base_url (str, optional): URL base del sitio
        """
        #parametros 
        self.driver = driver
        self.base_url = base_url
    
    def open(self, url_path=""):
        """
        Abre una URL específica, combinándola con la URL base.
        
        Args:
            url_path (str, optional): Ruta a añadir a la URL base
        """
        full_url = f"{self.base_url}{url_path}" if self.base_url else url_path
        logger.info(f"Navegando a: {full_url}")
        self.driver.get(full_url)
    
    def find_element(self, locator: Tuple[str, str], timeout=DEFAULT_TIMEOUT) -> WebElement:
        """
        Encuentra un elemento utilizando un localizador específico y espera hasta que esté presente.
        
        Args:
            locator (tuple): Tuple que contiene el tipo y valor del localizador (By.ID, "id_value")
            timeout (int, optional): Tiempo máximo de espera en segundos
            
        Returns:
            WebElement: Elemento encontrado
            
        Raises:
            TimeoutException: Si el elemento no se encuentra en el tiempo especificado
        """
        try:
            logger.debug(f"Buscando elemento: {locator[0]}='{locator[1]}'")
            start_time = time.time()
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            elapsed_time = time.time() - start_time
            logger.debug(f"Elemento encontrado en {elapsed_time:.2f} segundos: {locator[0]}='{locator[1]}'")
            return element
        except TimeoutException:
            logger.error(f"⚠️ NO SE ENCONTRÓ el elemento {locator[0]}='{locator[1]}' después de {timeout} segundos")
            self.take_screenshot(f"error_find_{locator[1].replace(':', '_')}")
            raise
    
    def is_element_present(self, locator: Tuple[str, str], timeout=5) -> bool:
        """
        Verifica si un elemento está presente en la página.
        
        Args:
            locator (tuple): Tuple que contiene el tipo y valor del localizador
            timeout (int, optional): Tiempo máximo de espera en segundos
            
        Returns:
            bool: True si el elemento está presente, False en caso contrario
        """
        try:
            self.find_element(locator, timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False
    
    def click_element(self, locator: Tuple[str, str], timeout=DEFAULT_TIMEOUT):
        """
        Encuentra un elemento y hace clic en él.
        
        Args:
            locator (tuple): Tuple que contiene el tipo y valor del localizador
            timeout (int, optional): Tiempo máximo de espera en segundos
        """
        element = self.find_element(locator, timeout)
        logger.info(f"👆 Haciendo clic en elemento: {locator[0]}='{locator[1]}'")
        try:
            element.click()
            logger.debug(f"Clic realizado exitosamente en: {locator[0]}='{locator[1]}'")
        except Exception as e:
            logger.error(f"⚠️ Error al hacer clic en {locator[0]}='{locator[1]}': {e}")
            self.take_screenshot(f"error_click_{locator[1].replace(':', '_')}")
            raise
    
    def input_text(self, locator: Tuple[str, str], text: str, timeout=DEFAULT_TIMEOUT):
        """
        Encuentra un elemento e introduce texto en él.
        
        Args:
            locator (tuple): Tuple que contiene el tipo y valor del localizador
            text (str): Texto a introducir
            timeout (int, optional): Tiempo máximo de espera en segundos
        """
        element = self.find_element(locator, timeout)
        # No mostramos el texto completo si es una contraseña
        display_text = "********" if "password" in str(locator).lower() else text
        logger.info(f"⌨️ Introduciendo texto en elemento {locator[0]}='{locator[1]}': '{display_text}'")
        try:
            element.clear()
            element.send_keys(text)
            logger.debug(f"Texto introducido exitosamente en: {locator[0]}='{locator[1]}'")
        except Exception as e:
            logger.error(f"⚠️ Error al introducir texto en {locator[0]}='{locator[1]}': {e}")
            self.take_screenshot(f"error_input_{locator[1].replace(':', '_')}")
            raise
    
    def get_text(self, locator: Tuple[str, str], timeout=DEFAULT_TIMEOUT) -> str:
        """
        Obtiene el texto de un elemento.
        
        Args:
            locator (tuple): Tuple que contiene el tipo y valor del localizador
            timeout (int, optional): Tiempo máximo de espera en segundos
            
        Returns:
            str: Texto del elemento
        """
        element = self.find_element(locator, timeout)
        return element.text
    
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout=DEFAULT_TIMEOUT) -> WebElement:
        """
        Espera hasta que un elemento sea visible en la página.
        
        Args:
            locator (tuple): Tuple que contiene el tipo y valor del localizador
            timeout (int, optional): Tiempo máximo de espera en segundos
            
        Returns:
            WebElement: Elemento visible
            
        Raises:
            TimeoutException: Si el elemento no es visible en el tiempo especificado
        """
        try:
            logger.debug(f"Esperando a que el elemento sea visible: {locator}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"El elemento {locator} no fue visible después de {timeout} segundos")
            self.take_screenshot(f"error_visibility_{locator[1].replace(':', '_')}")
            raise
    
    def wait_for_element_clickable(self, locator: Tuple[str, str], timeout=DEFAULT_TIMEOUT) -> WebElement:
        """
        Espera hasta que un elemento sea clickable en la página.
        
        Args:
            locator (tuple): Tuple que contiene el tipo y valor del localizador
            timeout (int, optional): Tiempo máximo de espera en segundos
            
        Returns:
            WebElement: Elemento clickable
            
        Raises:
            TimeoutException: Si el elemento no es clickable en el tiempo especificado
        """
        try:
            logger.debug(f"Esperando a que el elemento sea clickable: {locator}")
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"El elemento {locator} no fue clickable después de {timeout} segundos")
            self.take_screenshot(f"error_clickable_{locator[1].replace(':', '_')}")
            raise
    
    def take_screenshot(self, name: str):
        """
        Toma una captura de pantalla del estado actual del navegador.
        Organiza las capturas en carpetas según la URL base.
        
        Args:
            name (str): Nombre para el archivo de captura
        """
        
        
        # Obtener la URL actual para determinar el servidor
        current_url = self.driver.current_url
        
        # Extraer el identificador del servidor (ftdspprod001, ftdspprod002, etc.)
        server_match = re.search(r'ftdspprod\d{3}', current_url)
        server_id = server_match.group(0) if server_match else "unknown_server"
        
        # Crear directorio específico para este servidor
        server_screenshots_dir = os.path.join(SCREENSHOTS_DIR, server_id)
        os.makedirs(server_screenshots_dir, exist_ok=True)
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{server_screenshots_dir}/{name}_{timestamp}.png"
        
        logger.info(f"Tomando captura de pantalla: {filename}")
        self.driver.save_screenshot(filename)
    
    def get_page_title(self) -> str:
        """
        Obtiene el título de la página actual.
        
        Returns:
            str: Título de la página
        """
        return self.driver.title
    
    def get_page_url(self) -> str:
        """
        Obtiene la URL actual.
        
        Returns:
            str: URL actual
        """
        return self.driver.current_url