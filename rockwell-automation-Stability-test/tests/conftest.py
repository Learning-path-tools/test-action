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

# Assuming BASE_URLS, SCREENSHOTS_DIR etc. are correctly defined in config.config
from config.config import DEFAULT_BROWSER, DEFAULT_TIMEOUT, BASE_URLS, SCREENSHOTS_DIR
from utils.driver_factory import DriverFactory
from utils.logger import logger, setup_logger # Ensure setup_logger is imported if used directly

# --- Global logger instance ---
# It's generally better practice to configure the logger within fixtures or tests
# where the context (like base_url) is known, rather than relying on a mutable global.
# However, keeping the original structure for now.
# logger = setup_logger() # Initial setup (might be overwritten in setup fixture)


def pytest_addoption(parser):
    """
    Agrega opciones de línea de comandos para pytest.
    """
    parser.addoption(
        "--url-index",
        action="store",
        default=None, # Default to None if not provided
        type=str,     # Read as string initially to handle potential non-integer input gracefully
        help="Índice de la URL a probar (e.g., 1-20). Si no se especifica, se usará la URL predeterminada."
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
    Handles --url-index and --all-urls flags.
    """
    # Check if the test function requests the 'base_url' fixture and isn't already parameterized
    if "base_url" in metafunc.fixturenames and not hasattr(metafunc.function, "parametrize"):
        url_index_str = metafunc.config.getoption("url_index")
        all_urls_flag = metafunc.config.getoption("all_urls")

        target_urls = []

        if all_urls_flag:
            # If --all-urls is set, use all URLs from BASE_URLS
            target_urls = BASE_URLS
            print(f"Running tests on all {len(target_urls)} URLs.") # Debug print
        elif url_index_str is not None:
            # If --url-index is provided, try to use that specific index
            try:
                # Convert the input string to an integer
                url_index = int(url_index_str)
                # Validate if the 1-based index is within the valid range
                if 1 <= url_index <= len(BASE_URLS):
                    # --- Correction ---
                    # Subtract 1 from the user's 1-based index to get the 0-based list index
                    actual_index = url_index - 1
                    target_urls = [BASE_URLS[actual_index]]
                    print(f"Running test on URL index {url_index}: {target_urls[0]}") # Debug print
                    # --- End Correction ---
                else:
                    # Fail the test setup if the index is out of range
                    pytest.fail(
                        f"Invalid --url-index: {url_index}. "
                        f"Must be an integer between 1 and {len(BASE_URLS)}."
                    )
            except ValueError:
                # Fail the test setup if the input cannot be converted to an integer
                pytest.fail(
                    f"Invalid --url-index: '{url_index_str}'. Must be an integer."
                )
        else:
            # Default behavior: If neither --all-urls nor --url-index is provided, use the first URL
            if BASE_URLS:
                target_urls = [BASE_URLS[0]]
                print(f"No specific URL index provided. Running test on default URL: {target_urls[0]}") # Debug print
            else:
                pytest.fail("BASE_URLS list is empty in config.config. Cannot determine default URL.")

        # Parameterize the test function with the selected URL(s)
        if target_urls:
            metafunc.parametrize("base_url", target_urls)
        else:
            # This case should ideally be caught by previous checks, but as a safeguard:
            pytest.fail("Could not determine which URL(s) to run the test against.")


@pytest.fixture(scope="function")
def driver(request): # Pass request to access metafunc config if needed, though not used here directly now
    """
    Fixture que proporciona una instancia del WebDriver para cada función de test.

    Yields:
        WebDriver: Instancia del WebDriver configurada.
    """
    # Note: Logger setup is moved to the 'setup' fixture where 'base_url' is available
    print(f"Initializing browser: {DEFAULT_BROWSER}") # Use print for basic fixture info

    # Create WebDriver instance using the factory
    try:
        browser_driver = DriverFactory.get_driver(DEFAULT_BROWSER)
    except Exception as e:
        pytest.fail(f"Failed to initialize WebDriver ({DEFAULT_BROWSER}): {e}")
        return # Ensure no further execution if driver fails

    # Yield the driver to the test function
    yield browser_driver

    # --- Teardown ---
    # Quit the browser after the test function completes
    print("Closing browser.") # Use print for basic fixture info
    browser_driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para procesar el resultado de cada test y capturar screenshots en caso de fallos.
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # We only look at the 'call' phase results and only if the test failed
    if rep.when == "call" and rep.failed:
        try:
            # Attempt to retrieve the driver instance from the test item's function arguments
            # 'driver' fixture should be used in the test for this to work
            driver_instance = item.funcargs.get("driver")
            if driver_instance:
                # Get base_url info if available to include in the filename
                base_url = item.funcargs.get("base_url", "unknown_url")
                # Try to extract a server identifier (e.g., ftdspprod001)
                server_match = re.search(r'ftdspprod\d{3}', base_url)
                url_id = server_match.group(0) if server_match else base_url.split("//")[-1].split(".")[0]

                # Construct a meaningful screenshot name
                screenshot_name = f"FAILED_{item.name}_{url_id}"
                take_screenshot(driver_instance, screenshot_name)
            else:
                # Log if driver instance wasn't found (e.g., test failed during setup before driver was available)
                print(f"Screenshot skipped for {item.name}: Driver instance not found in funcargs.") # Use print in hook
        except Exception as e:
            print(f"Error capturing screenshot for {item.name}: {e}") # Use print in hook


def take_screenshot(driver: WebDriver, name: str):
    """
    Captura un screenshot del navegador actual y lo guarda en una carpeta organizada por servidor.

    Args:
        driver (WebDriver): Instancia del WebDriver.
        name (str): Nombre base para el archivo de captura (sin extensión).
    """
    try:
        # Get current URL to determine the server ID for folder organization
        current_url = driver.current_url
        server_match = re.search(r'ftdspprod\d{3}', current_url)
        # Use a more generic fallback if the specific pattern isn't found
        server_id = server_match.group(0) if server_match else current_url.split("//")[-1].split(".")[0].replace('.', '_')

        # Create a subdirectory for the specific server if it doesn't exist
        server_screenshots_dir = os.path.join(SCREENSHOTS_DIR, server_id)
        os.makedirs(server_screenshots_dir, exist_ok=True)

        # Generate filename with timestamp to avoid overwrites
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize the name part (replace characters invalid in filenames)
        safe_name = re.sub(r'[<>:"/\\|?*\[\]]', '_', name)
        filename = os.path.join(server_screenshots_dir, f"{safe_name}_{timestamp}.png")

        print(f"Capturing screenshot: {filename}") # Use print
        success = driver.save_screenshot(filename)
        if not success:
             print(f"Warning: driver.save_screenshot returned False for {filename}")
    except Exception as e:
        print(f"Failed to capture screenshot '{name}': {e}") # Use print


@pytest.fixture(scope="function")
def setup(driver, base_url):
    """
    Fixture que configura el driver navegando a una URL base específica antes de cada test.
    También configura el logger para usar un archivo específico para esa URL.

    Args:
        driver: Instancia del WebDriver (desde el fixture 'driver').
        base_url: URL base a la que se navegará (proporcionada por pytest_generate_tests).

    Returns:
        tuple: (WebDriver, str) - El driver configurado y la URL base utilizada.
    """
    # --- Logger Reconfiguration ---
    # Extract a unique identifier from the base_url for logging purposes
    server_match = re.search(r'ftdspprod\d{3}', base_url)
    url_id = server_match.group(0) if server_match else base_url.split("//")[-1].split(".")[0].replace('.', '_')

    # Get a logger instance configured specifically for this URL/server ID
    # This ensures logs for different parallel runs (if using xdist) go to separate files
    test_logger = setup_logger(url_id)

    test_logger.info("="*30 + f" TEST SETUP ({url_id}) " + "="*30)
    test_logger.info(f"  Browser: {DEFAULT_BROWSER}")
    test_logger.info(f"  Target URL: {base_url}")
    test_logger.info(f"  Server ID: {url_id}")
    test_logger.info(f"  Default Timeout: {DEFAULT_TIMEOUT}s")

    test_logger.info(f"Navigating to base URL: {base_url}")
    try:
        driver.get(base_url)
        test_logger.info("Navigation successful.")
        # Optional: Add a wait for page load complete here if needed
        # from utils.waits import wait_for_page_load
        # wait_for_page_load(driver)
    except Exception as e:
        test_logger.error(f"Failed to navigate to {base_url}: {e}")
        # Capture screenshot immediately if navigation fails
        take_screenshot(driver, f"ERROR_NAVIGATE_{url_id}")
        pytest.fail(f"Setup failed: Could not navigate to {base_url}. Error: {e}")

    # Return the configured driver and the base URL to the test function
    return driver, base_url
