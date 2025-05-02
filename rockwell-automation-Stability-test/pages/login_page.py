"""
Page Object for the Rockwell Automation login page.
Contains locators and methods for interacting with login page elements.
"""
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage
from utils.logger import logger
from config.config import DEFAULT_TIMEOUT

class LoginPage(BasePage):
    """
    Page Object Model for the login page and authentication flow.
    """
    
    # Locators for the initial SSO page (if it appears)
    SIGN_IN_WITH_SSO_BUTTON = (By.XPATH, "/html/body/div/main/section/div/div/div/div/form/button")
    
    # Locators for email input screen
    EMAIL_INPUT = (By.ID, "emailInput")
    EMAIL_LABEL = (By.XPATH, "//label[contains(text(), 'Email Address')]")
    CONTINUE_BUTTON = (By.ID, "continueBtn")
    
    # Locators for password screen
    PASSWORD_INPUT = (By.ID, "passwordInput")
    PASSWORD_LABEL = (By.XPATH, "//label[contains(text(), 'Enter Password')]")
    SIGN_IN_BUTTON = (By.XPATH, "//button[contains(text(), 'SIGN IN')]")
    TOGGLE_PASSWORD = (By.ID, "togglePassword")
    GO_BACK_BUTTON = (By.XPATH, "//button[contains(text(), 'GO BACK')]")
    
    # Localizadores para la página de proyectos
    NEW_PROJECT_BUTTON = (By.CSS_SELECTOR, "#mat-mdc-dialog-0 > div > div > ra-extensible-dialog > div > mat-dialog-content > ra-ide-welcome-screen > section > ra-ide-panel.ra-ide-panel--vertical-content > div > ra-ide-panel > div > ra-ide-welcome-slot:nth-child(2) > article > div > ra-create-workspace-welcome > ra-ui-list > div > div:nth-child(1) > div > div > div > span.ra-ui-list-item-label-wrapper > ra-ui-static-text > div > div > span:nth-child(3)")
    
    # Localizadores para ingresar datos en el projecto
    TYPE_PROJECT_NAME = (By.ID,"mat-input-0") 
    TEXT_INPUT_PROJECT = (By.ID,"mat-input-0")
    PROJECT_NAME_INPUT_ALT = (By.XPATH,"//*[@id=\"mat-input-3\"]")
    CREATE_PROJECT_BUTTON = (By.CSS_SELECTOR,"#mat-mdc-dialog-1 > div > div > ra-extensible-dialog > div > mat-dialog-actions > div.mat-dialog-actions.ra-dialog__actions.ra-dialog__actions--right.ng-star-inserted > div:nth-child(1) > ra-ui-main-button > button > span.mat-button-wrapper > div > ra-ui-static-text > div > div")
    DISMISS_BUTTON = (By.CSS_SELECTOR,"#mat-mdc-dialog-3 > div > div > ra-extensible-dialog > div > mat-dialog-actions > div > div:nth-child(2) > ra-ui-outlined-button > button > span.mat-button-wrapper > div > ra-ui-static-text > div > div")
    
    # Localizador de System View
    GITLAB_CHECK = (By.CSS_SELECTOR,"#contextProductHeader > div > mat-sidenav-container > mat-sidenav-content > ra-ide-app-shell > div > section.ra-ide-app-shell__status-bar.ng-star-inserted > ra-ide-status-bar > section > div.ra-ide-status-bar__slot.ra-ide-status-bar__slot--global > ra-ide-status-bar-item:nth-child(1) > div > span > span.ra-ide-status-bar-item__content.ra-ide-status-bar-item__content--text.body-2.ng-star-inserted")
        
    # copilot localizador
    
    COPILOT = (By.XPATH, "/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[3]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner[1]/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ai-assistant/div/div[2]/div/div/ra-ui-multiline-input/mat-form-field/div/div[1]/div/textarea")
    XPATHsend = "/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[3]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner[1]/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ai-assistant/div/div[2]/div/ra-ui-icon-button/button"
    SendCOPILOT = (By.XPATH,XPATHsend)
    SoCreated = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/div[1]/ra-ide-explorer/div/ra-ide-panel/div/ra-ide-logical-model-explorer/ra-ide-explorer-tree/ra-ui-tree/cdk-virtual-scroll-viewport/div[1]/mat-tree/mat-tree-node[1]/div/li/div/div/ra-ui-tree-node/div/div[2]/ra-ui-static-text/div/div")
    
    #Local changes
    LOCALCHANGE = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[4]/ra-ide-status-bar/section/div[3]/ra-ide-status-bar-item[1]/div/span/span[2]")
    DEVICEVIEW = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/ra-ide-panel-bar-outlet/ra-ide-panel-bar-group/ra-ide-panel-bar-toggle-button[2]/div/div/span")
    EXPLORERVIEW = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/ra-ide-panel-bar-outlet/ra-ide-panel-bar-group/ra-ide-panel-bar-toggle-button[3]/div/div/span")
    LIBRARYVIEW = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/ra-ide-panel-bar-outlet/ra-ide-panel-bar-group/ra-ide-panel-bar-toggle-button[4]/div/div/span")
    
    #Device L85E
    NEWDEVICE = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/div[2]/div/ra-ide-nav-tab-group/div/mat-tab-group/div/mat-tab-body[1]/div/ra-ide-explorer/div/ra-ide-panel[1]/div/ra-explorer-connections/ra-ui-tree/cdk-virtual-scroll-viewport/div[1]/div/ra-ui-empty-state/div/div[3]/ra-ui-outlined-button/button/span[1]/div/ra-ui-static-text/div/div")
    SELCONTROLLERS = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-content/ra-device-add-dialog/div/ra-device-selection-page/div/div[1]/div/ra-ui-checkbox[3]/mat-checkbox/label/span[1]")   
    CHECKBOX = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-content/ra-device-add-dialog/div/ra-device-selection-page/div/div[2]/div[1]/ra-device-catalog-list/div/div/ag-grid-angular/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/div[9]/div/div/div/div/div[2]/input")
    CONTINUECONTROL = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-actions/div[2]/div[1]/ra-ui-main-button/button/span[1]/div/ra-ui-static-text/div/div")
    TIPENAME = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-content/ra-device-add-dialog/div/ra-device-configure-page/div/div[2]/div[1]/div[1]/div[2]/ra-ui-accordion/div/ra-ui-accordion-item/div[2]/div/ra-ui-accordion-item/div[2]/div/ra-property-bag/div/div[1]/ra-ui-input/mat-form-field/div/div[1]/div[2]/input")    
    FINISH_BUTTON = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-actions/div[2]/div[2]/ra-ui-main-button/button/span[1]/div/ra-ui-static-text/div/div")
    BACKPLANE = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/div[2]/div/ra-ide-nav-tab-group/div/mat-tab-group/div/mat-tab-body[1]/div/ra-ide-explorer/div/ra-ide-panel[1]/div/ra-explorer-connections/ra-ui-tree/cdk-virtual-scroll-viewport/div[1]/mat-tree/mat-tree-node[3]/div/li/div/div/ra-ui-tree-node/div/div[2]/ra-ui-static-text/div/div")
    
    #Deploy view
    DEPLOYBUTTON = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[1]/div/div/ra-ide-icons-toolbar/ul/li[1]/div[2]/ra-ui-icon-button/button/span[1]/mat-icon")
    CONTROLSHOWN = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[2]/div/ra-ide-panel[1]/div/ra-ide-tabs-outlet/div[2]/section/ra-ide-tab-content/div/div/ra-deploy/div/div[2]/ag-grid-angular/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/div/div/div[1]")
    
    #VCS
    SAVED = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-toolbar/div[1]/ra-ui-content-projection/div/div/ra-ui-static-text[2]/div")
    COMMIT = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[1]/div/div/ra-ide-icons-toolbar/ul/li[2]/div[1]/ra-ui-icon-button/button/span[1]/mat-icon")
    TIPECOMMIT = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-content/ra-dialog-form/div/ra-ui-dynamic-form/div/ra-ui-dynamic-form-schema/div/div/ra-ui-dynamic-form-category/div/mat-accordion/ra-ui-accordion-item/div/div/ra-ui-dynamic-form-area/div/div/ra-ui-dynamic-form-property/div/div/span/ra-ui-input/mat-form-field/div/div[1]/div[2]/input")
    COMMITBUTTON = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-actions/div[2]/div[1]/ra-ui-main-button/button/span[1]/div/ra-ui-static-text/div")
    PUSHBUTTON = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[1]/div/div/ra-ide-icons-toolbar/ul/li[2]/div[2]/ra-ui-icon-button/button")
    CLOSETAB = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/div/div")
    PROJECTSINCRO = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[4]/ra-ide-status-bar/section/div[3]/ra-ide-status-bar-item[1]")
    
    # Locators for error messages
    ERROR_MESSAGE = (By.ID, "pe-err-message")
    
    
    ######################## FUNCIONES DE APLICACION
    def __init__(self, driver, base_url=None):
        """
        Initialize the login page object.
        
        Args:
            driver: WebDriver instance
            base_url (str, optional): Base URL of the site
        """
        super().__init__(driver, base_url)
    
    def open_login_page(self):
        """
        Abre la página de login.
        """
        logger.info("🌐 Abriendo página de login")
        self.open()
        
        # Check if we need to click on SSO button first
        if self.is_element_present(self.SIGN_IN_WITH_SSO_BUTTON, timeout=115):
            logger.info("🔍 Botón SSO detectado, preparando para hacer clic")
            self.click_element(self.SIGN_IN_WITH_SSO_BUTTON)
        else:
            logger.debug("Botón SSO no presente, continuando directamente al formulario de login")
        
        # Wait for email input to be visible
        try:
            self.wait_for_element_visible(self.EMAIL_INPUT)
            logger.info("✅ Página de login cargada correctamente")
        except TimeoutException:
            logger.error("❌ Error: No se pudo cargar la página de login")
            self.take_screenshot("login_page_not_loaded")
            raise
        
        return self
    
    def wait_three_seconds(self):
        """
        Pauses execution for exactly 3 seconds.
        Useful for waiting for elements to load or animations to complete.
        
        Returns:
            self: Returns self for method chaining
        """
        logger.info("⏱️ Esperando 3 segundos...")
        import time
        time.sleep(6)
        logger.info("✅ Espera de 3 segundos completada")
        return self
    
    def enter_email(self, email):
        """
        Enter email address in the email input field.
        
        Args:
            email (str): Email address to enter
        """
        logger.info(f"Entering email: {email}")
        self.wait_for_element_visible(self.EMAIL_INPUT)
        self.input_text(self.EMAIL_INPUT, email)
        return self
    
    def click_continue(self):
        """
        Click the Continue button after entering email.
        """
        logger.info("Clicking Continue button")
        self.wait_for_element_clickable(self.CONTINUE_BUTTON)
        self.click_element(self.CONTINUE_BUTTON)
        
        # Wait for password input to be visible
        try:
            self.wait_for_element_visible(self.PASSWORD_INPUT)
        except TimeoutException:
            logger.warning("Password input not visible after clicking Continue. Taking screenshot.")
            self.take_screenshot("password_input_not_visible")
            raise
        
        return self
    
    def enter_password(self, password):
        """
        Enter password in the password input field.
        
        Args:
            password (str): Password to enter
        """
        logger.info("Entering password")  # Not logging the actual password for security
        self.wait_for_element_visible(self.PASSWORD_INPUT)
        self.input_text(self.PASSWORD_INPUT, password)
        return self
    
    def click_sign_in(self):
        """
        Click the Sign In button after entering password.
        """
        logger.info("Clicking Sign In button")
        self.wait_for_element_clickable(self.SIGN_IN_BUTTON)
        self.click_element(self.SIGN_IN_BUTTON)
        
        # Take screenshot after clicking Sign In
        self.take_screenshot("after_sign_in_click")
        return self
    
    def toggle_password_visibility(self):
        """
        Toggle password visibility.
        """
        logger.info("Toggling password visibility")
        if self.is_element_present(self.TOGGLE_PASSWORD):
            self.click_element(self.TOGGLE_PASSWORD)
        return self
    
    def go_back(self):
        """
        Click the Go Back button to return to email screen.
        """
        logger.info("Clicking Go Back button")
        self.click_element(self.GO_BACK_BUTTON)
        
        # Wait for email input to be visible again
        self.wait_for_element_visible(self.EMAIL_INPUT)
        return self
    
    def step_new_project(self):
        """
        Proceso de crear new project.
        """
        logger.info("🖱️ Intentando hacer clic en el botón 'New project'")
        
        logger.info("Click en abriendo projectos")
        if self.is_element_present(self.NEW_PROJECT_BUTTON,timeout=160):
            self.wait_for_element_clickable(self.NEW_PROJECT_BUTTON)
            self.click_element(self.NEW_PROJECT_BUTTON)
            logger.info("✅ Botón 'New project' encontrado y clickeado exitosamente")
            #ESCRIBIENDO NOMBRE
            logger.info("Esperando boton")
            self.wait_for_element_visible(self.TYPE_PROJECT_NAME,timeout=160)
            logger.info("✅ Espacio 'project name' encontrado y typeado exitosamente")
            return self
    
    def typing_name_project(self):
        """
        function to tape the name of the project (random)
        """
        try:
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            project_name = f"TestProject_{random_suffix}"
            logger.info(f"⌨️ Introduciendo nombre de proyecto: '{project_name}'")
            self.wait_for_element_visible(self.TEXT_INPUT_PROJECT, timeout=110)
            self.click_element(self.TEXT_INPUT_PROJECT)
            self.input_text(self.TEXT_INPUT_PROJECT, project_name)
            
        except Exception as e:
            logger.warning(f"Error con localizador principal: {e}")
            # Si falla, intentar con el localizador alternativo
            logger.info("Intentando con localizador alternativo para el campo de nombre")
            self.input_text(self.PROJECT_NAME_INPUT_ALT, project_name)
            raise
        return self
        
    
    def create_new_project_click(self):
        """
        click on create button
        """
        try:
            self.wait_for_element_visible(self.CREATE_PROJECT_BUTTON, timeout=110)
            self.click_element(self.CREATE_PROJECT_BUTTON)
            
        except Exception as e:
            logger.warning(f"Error con localizador principal: {e}")
            # Si falla, intentar con el localizador alternativo
            raise
        return self

    def dismiss_button(self):
        """
        Dismiss vault project
        """
        try:
            self.wait_for_element_visible(self.DISMISS_BUTTON, timeout=120)
            self.click_element(self.DISMISS_BUTTON)
            
        except Exception as e:
            logger.warning(f"Error con localizador principal: {e}")
            # Si falla, intentar con el localizador alternativo
            raise
        return self
    
    def validate_gitlab(self):
        """validating message project synchronize"""
        try:
            self.wait_for_element_visible(self.GITLAB_CHECK, timeout=120)
            logger.info("✅ Espacio 'project sinchronized' encontrado exitosamente")
            
        except Exception as e:
            logger.warning(f"Error con localizador principal: {e}")
            # Si falla, intentar con el localizador alternativo
            raise
        return self
    
    def copilot_use(self):
        """creating with copilot"""
        
        try:
            
            PROMT = "Create a Smart object( named SO_Copilot), with program(P1_Copilot)"
            logger.info(f"⌨️ Introduciendo Promt")
            self.wait_for_element_visible(self.COPILOT, timeout=120)
            self.input_text(self.COPILOT, PROMT,110)
            self.click_element(self.SendCOPILOT,110)
            self.wait_for_element_visible(self.SoCreated,115)
            
        except Exception as e:
            logger.warning(f"Error con localizador principal: {e}")
            raise
        return self
    
    def verifing_texts(self):
        """Here we validate al texts and views"""
        try:
            self.wait_for_element_visible(self.LOCALCHANGE,110)
            logger.info("✅ Texto 'Local changes available' encontrado exitosamente")
            self.wait_for_element_clickable(self.DEVICEVIEW,110)
            logger.info("✅ Device View encontrado exitosamente")
            self.wait_for_element_clickable(self.EXPLORERVIEW,110)
            logger.info("✅ Explorer View encontrado exitosamente")
            self.wait_for_element_clickable(self.LIBRARYVIEW,110)
            logger.info("✅ Library View encontrado exitosamente")
            self.click_element(self.DEVICEVIEW,110)
            logger.info("Done")
                
        except Exception as e:
            logger.warning(f"Error con localizador principal: {e}")
            raise    
        return self
    
    def select_controller(self):
        """select controler L85E"""
        try:
            
            self.wait_for_element_clickable(self.DEVICEVIEW,120)
            logger.info("✅ Device View encontrado exitosamente")
            self.click_element(self.DEVICEVIEW,120)
            self.click_element(self.NEWDEVICE,120)
            self.click_element(self.SELCONTROLLERS,120)
            self.click_element(self.CHECKBOX,120)
            self.click_element(self.CONTINUECONTROL,120)
            self.click_element(self.TIPENAME,120)
            self.input_text(self.TIPENAME, "Controller_automate",120)
            self.click_element(self.FINISH_BUTTON,120)
            self.wait_for_element_visible(self.BACKPLANE,120)
            logger.info("Done")
                
        except Exception as e:
            logger.warning(f"Error con localizador principal: {e}")
            raise    
        return self
    
    def VCS(self):
        """select controler L85E"""
        try:
            
            self.wait_three_seconds()
            self.wait_for_element_clickable(self.SAVED,120)
            logger.info("✅ haciendo pasos de VCS")
            self.click_element(self.COMMIT,120)
            self.input_text(self.TIPECOMMIT, "COMMIT AUTOMATED",120)
            self.click_element(self.COMMITBUTTON,120)
            self.wait_three_seconds()
            self.wait_for_element_clickable(self.PUSHBUTTON,120)
            self.click_element(self.PUSHBUTTON,120)
            self.click_element(self.CLOSETAB,120)
            self.wait_three_seconds()
            self.wait_three_seconds()
            self.wait_for_element_clickable(self.PROJECTSINCRO,120)
            logger.info("VCS Done")
                
        except Exception as e:
            logger.warning(f"Error con localizador principal: {e}")
            raise    
        return self
    
    def get_error_message(self):
        """
        Get any error message displayed during login.
        
        Returns:
            str: Error message text or empty string if no error
        """
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ""
    
    
    
    ################ PASOS DE LA AUTOMATIZACION
    
    
    def complete_test(self, email, password):
        """
        Complete the full login process.
        
        Args:
            email (str): Email address to use
            password (str): Password to use
            
        Returns:
            self for method chaining
        """
        logger.info(f"🔐 Iniciando proceso de Pruebas con el email: {email}")
        
        # Open login page (will handle SSO button if needed)
        logger.info("PASO 1: Abrir página de login")
        self.open_login_page()
        
        # Enter email and continue
        logger.info("PASO 2: Introducir dirección de email")
        self.enter_email(email)
        
        logger.info("PASO 3: Hacer clic en botón Continuar")
        self.click_continue()
        
        # Enter password and sign in
        logger.info("PASO 4: Introducir contraseña")
        self.enter_password(password)
        
        logger.info("PASO 5: Hacer clic en botón Sign In")
        self.click_sign_in()
        
        logger.info("PASO 6: Hacer clic en new project")
        self.step_new_project() 
        
        logger.info("PASO 7: Escribiendo nombre aleatorio")
        self.typing_name_project()
        
        logger.info("PASO 8: Click en crear nuevo projecto")
        self.create_new_project_click()
        logger.info("Click on dismiss button")
        self.dismiss_button()
        self.take_screenshot("New project Step")
        
        logger.info("PASO 9: Validando Gitlab")
        self.validate_gitlab()
        self.copilot_use()
        
        logger.info("PASO 10: Crear Smart object y validacion de vistas")
        self.verifing_texts()
        self.take_screenshot("Creation of Smart Objects")
        
        logger.info("PASO 11: Seleccionar controlador")
        self.select_controller()
        self.take_screenshot("Devices")
        
        logger.info("PASO 12: VCS")
        self.VCS()
        self.take_screenshot("VCS")
        
        logger.info("✅ Prueba terminada")
        
        
        # Take a final screenshot
        self.take_screenshot("final step")
        
        # Here we could return the next page (e.g., DashboardPage) if needed
        return self