"""
Tests for the login flow in the Rockwell Automation application.
"""

import pytest
from pages.login_page import LoginPage
from utils.logger import logger
from config.config import TEST_USERNAME, TEST_PASSWORD
import datetime

def test_login_with_credentials(setup):
    """
    Test the full login process using environment variables for credentials.
    
    Args:
        setup: Fixture providing the driver and base URL
    """
    driver, base_url = setup
    logger.info("=" * 80)
    logger.info(f"▶️ INICIANDO TEST: Login con credenciales en {base_url}")
    logger.info("=" * 80)
    
    # Skip the test if credentials are not set
    if not TEST_USERNAME or not TEST_PASSWORD:
        logger.warning("⚠️ Credenciales de prueba no configuradas en variables de entorno")
        pytest.skip("Test credentials not set in environment variables")
    
    try:
        # Create login page instance
        login_page = LoginPage(driver, base_url)
        
        # Complete the login process
        login_page.complete_test(TEST_USERNAME, TEST_PASSWORD)
        
        # Here you would add assertions to verify successful login
        logger.info("Verificando login exitoso...")
        # Ejemplo: verificar que estamos en la página de dashboard después del login
        # assert "dashboard" in driver.current_url.lower(), "No se redirigió al dashboard después del login"
        
        logger.info("✅ TEST COMPLETADO EXITOSAMENTE")
    except Exception as e:
        logger.error(f"❌ ERROR EN EL TEST: {e}")
        # Capturar screenshot final en caso de error
        try:
            driver.save_screenshot(f"reports/screenshots/error_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        except:
            pass
        raise
    finally:
        logger.info("=" * 80)
        