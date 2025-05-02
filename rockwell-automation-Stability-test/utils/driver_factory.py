"""
Configuracion de Selenium, donde llamo todos los modulos a correr
ademas me traigo las configuracion de los diferentes drivers a correr
Factory para crear instancias del WebDriver.
Centraliza la creación y configuración de diferentes navegadores.
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
# Import webdriver_manager only if needed for Firefox/Edge or local runs
# from webdriver_manager.chrome import ChromeDriverManager # Removed for Chrome
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config.config import IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT
from config.browsers import get_chrome_options, get_firefox_options, get_edge_options
from utils.logger import logger

class DriverFactory:

    """
    Clase para crear y configurar instancias del WebDriver para diferentes navegadores.
    """

    @staticmethod
    def get_driver(browser_name="chrome"):
        """
        Creates and configures a WebDriver instance based on the specified browser.

        Args:
            browser_name (str): Name of the browser to use. Options: "chrome", "firefox", "edge"

        Returns:
            WebDriver: Configured WebDriver instance

        Raises:
            ValueError: If an unsupported browser is specified
        """
        browser_name = browser_name.lower()

        if browser_name == "chrome":
            # --- Modification Start ---
            # Rely on ChromeDriver being in the system PATH (installed by the workflow)
            # No need to use ChromeDriverManager().install() in the GitHub Action environment
            logger.info("Initializing Chrome driver using system PATH for ChromeDriver")
            try:
                # Pass executable_path=None or omit it; Selenium >= 4.6 should find it automatically
                # If using an older Selenium, you might need Service() without arguments
                # For Selenium 4.10+, Service() is recommended even when using PATH
                service = ChromeService() # Selenium should find chromedriver in PATH
                driver = webdriver.Chrome(service=service, options=get_chrome_options())
                logger.info("Chrome driver initialized successfully using system PATH.")
            except Exception as e:
                logger.error(f"Error initializing Chrome driver using system PATH: {e}")
                logger.error("Ensure ChromeDriver is installed and accessible in the system's PATH.")
                # Optional: Add fallback for local execution if needed, but primarily rely on PATH in CI
                # try:
                #     logger.warning("Falling back to ChromeDriverManager for local execution.")
                #     from webdriver_manager.chrome import ChromeDriverManager
                #     service = ChromeService(executable_path=ChromeDriverManager().install())
                #     driver = webdriver.Chrome(service=service, options=get_chrome_options())
                # except Exception as fallback_e:
                #     logger.error(f"Fallback using ChromeDriverManager also failed: {fallback_e}")
                #     raise fallback_e # Re-raise the fallback error if it fails too
                raise e # Re-raise the original error if no fallback or fallback fails
            # --- Modification End ---

        elif browser_name == "firefox":
            # Use webdriver-manager for Firefox if needed
            logger.info("Initializing Firefox driver using GeckoDriverManager")
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=get_firefox_options())
            logger.info("Firefox driver initialized successfully.")
        elif browser_name == "edge":
            # Use webdriver-manager for Edge if needed
            logger.info("Initializing Edge driver using EdgeChromiumDriverManager")
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=get_edge_options())
            logger.info("Edge driver initialized successfully.")
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        # Configure timeouts
        driver.implicitly_wait(IMPLICIT_WAIT)
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

        return driver
