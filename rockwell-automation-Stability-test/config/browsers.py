"""
Aqui puedo configurar si quiero que se vea o no la ventana de navegacion
Configuración para diferentes navegadores soportados por el framework.
Contiene opciones específicas para cada navegador.
"""

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def get_chrome_options():
    """
    Configura y devuelve opciones para el navegador Chrome.
    
    Returns:
        ChromeOptions: Opciones configuradas para Chrome
    """
    options = ChromeOptions()
    #options.add_argument("--start-maximized")  # Maximiza la ventana del navegador
    options.add_argument("--disable-extensions")  # Desactiva extensiones
    options.add_argument("--disable-popup-blocking")  # Permite popups
    options.add_argument("--disable-infobars")  # Desactiva infobars
    
    # Opciones para ejecución sin interfaz gráfica (headless)
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    #options.add_argument("--window-size=1920,1080")
    
    return options

def get_firefox_options():
    """
    Configura y devuelve opciones para el navegador Firefox.
    
    Returns:
        FirefoxOptions: Opciones configuradas para Firefox
    """
    options = FirefoxOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    
    # Opciones para ejecución sin interfaz gráfica (headless)
    # options.add_argument("--headless")
    
    return options

def get_edge_options():
    """
    Configura y devuelve opciones para el navegador Edge.
    
    Returns:
        EdgeOptions: Opciones configuradas para Edge
    """
    options = EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    
    # Opciones para ejecución sin interfaz gráfica (headless)
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    
    return options