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

    # Locators for the projects page
    NEW_PROJECT_BUTTON = (By.CSS_SELECTOR, "#mat-mdc-dialog-0 > div > div > ra-extensible-dialog > div > mat-dialog-content > ra-ide-welcome-screen > section > ra-ide-panel.ra-ide-panel--vertical-content > div > ra-ide-panel > div > ra-ide-welcome-slot:nth-child(2) > article > div > ra-create-workspace-welcome > ra-ui-list > div > div:nth-child(1) > div > div > div > span.ra-ui-list-item-label-wrapper > ra-ui-static-text > div > div > span:nth-child(3)")

    # Locators for entering project data
    TYPE_PROJECT_NAME = (By.ID,"mat-input-0")
    TEXT_INPUT_PROJECT = (By.ID,"mat-input-0")
    PROJECT_NAME_INPUT_ALT = (By.XPATH,"//*[@id=\"mat-input-3\"]")
    CREATE_PROJECT_BUTTON = (By.CSS_SELECTOR,"#mat-mdc-dialog-1 > div > div > ra-extensible-dialog > div > mat-dialog-actions > div.mat-dialog-actions.ra-dialog__actions.ra-dialog__actions--right.ng-star-inserted > div:nth-child(1) > ra-ui-main-button > button > span.mat-button-wrapper > div > ra-ui-static-text > div > div")
    DISMISS_BUTTON = (By.CSS_SELECTOR,"#mat-mdc-dialog-3 > div > div > ra-extensible-dialog > div > mat-dialog-actions > div > div:nth-child(2) > ra-ui-outlined-button > button > span.mat-button-wrapper > div > ra-ui-static-text > div > div")

    # Locator for System View
    GITLAB_CHECK = (By.CSS_SELECTOR,"#contextProductHeader > div > mat-sidenav-container > mat-sidenav-content > ra-ide-app-shell > div > section.ra-ide-app-shell__status-bar.ng-star-inserted > ra-ide-status-bar > section > div.ra-ide-status-bar__slot.ra-ide-status-bar__slot--global > ra-ide-status-bar-item:nth-child(1) > div > span > span.ra-ide-status-bar-item__content.ra-ide-status-bar-item__content--text.body-2.ng-star-inserted")

    # Copilot locators
    COPILOT = (By.XPATH, "/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[3]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner[1]/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ai-assistant/div/div[2]/div/div/ra-ui-multiline-input/mat-form-field/div/div[1]/div/textarea")
    XPATHsend = "/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[3]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner[1]/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ai-assistant/div/div[2]/div/ra-ui-icon-button/button"
    SendCOPILOT = (By.XPATH,XPATHsend)
    SoCreated = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/div[1]/ra-ide-explorer/div/ra-ide-panel/div/ra-ide-logical-model-explorer/ra-ide-explorer-tree/ra-ui-tree/cdk-virtual-scroll-viewport/div[1]/mat-tree/mat-tree-node[1]/div/li/div/div/ra-ui-tree-node/div/div[2]/ra-ui-static-text/div/div")

    # Local changes
    LOCALCHANGE = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[4]/ra-ide-status-bar/section/div[3]/ra-ide-status-bar-item[1]/div/span/span[2]")
    DEVICEVIEW = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/ra-ide-panel-bar-outlet/ra-ide-panel-bar-group/ra-ide-panel-bar-toggle-button[2]/div/div/span")
    EXPLORERVIEW = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/ra-ide-panel-bar-outlet/ra-ide-panel-bar-group/ra-ide-panel-bar-toggle-button[3]/div/div/span")
    LIBRARYVIEW = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/ra-ide-panel-bar-outlet/ra-ide-panel-bar-group/ra-ide-panel-bar-toggle-button[4]/div/div/span")

    # Device L85E
    NEWDEVICE = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/div[2]/div/ra-ide-nav-tab-group/div/mat-tab-group/div/mat-tab-body[1]/div/ra-ide-explorer/div/ra-ide-panel[1]/div/ra-explorer-connections/ra-ui-tree/cdk-virtual-scroll-viewport/div[1]/div/ra-ui-empty-state/div/div[3]/ra-ui-outlined-button/button/span[1]/div/ra-ui-static-text/div/div")
    SELCONTROLLERS = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-content/ra-device-add-dialog/div/ra-device-selection-page/div/div[1]/div/ra-ui-checkbox[3]/mat-checkbox/label/span[1]")
    CHECKBOX = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-content/ra-device-add-dialog/div/ra-device-selection-page/div/div[2]/div[1]/ra-device-catalog-list/div/div/ag-grid-angular/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/div[9]/div/div/div/div/div[2]/input")
    CONTINUECONTROL = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-actions/div[2]/div[1]/ra-ui-main-button/button/span[1]/div/ra-ui-static-text/div/div")
    TIPENAME = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-content/ra-device-add-dialog/div/ra-device-configure-page/div/div[2]/div[1]/div[1]/div[2]/ra-ui-accordion/div/ra-ui-accordion-item/div[2]/div/ra-ui-accordion-item/div[2]/div/ra-property-bag/div/div[1]/ra-ui-input/mat-form-field/div/div[1]/div[2]/input")
    FINISH_BUTTON = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-actions/div[2]/div[2]/ra-ui-main-button/button/span[1]/div/ra-ui-static-text/div/div")
    BACKPLANE = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[1]/div/ra-ide-dock-panel-multi-group/section/ra-ide-panel/div/ra-ide-dock-panel-group/section/ra-ide-dock-panel-inner/ra-ide-dock-panel/div/ra-ide-tool-panel/div[2]/ra-ide-panel/div/ra-ide-explorer-outlet/div[2]/div/ra-ide-nav-tab-group/div/mat-tab-group/div/mat-tab-body[1]/div/ra-ide-explorer/div/ra-ide-panel[1]/div/ra-explorer-connections/ra-ui-tree/cdk-virtual-scroll-viewport/div[1]/mat-tree/mat-tree-node[3]/div/li/div/div/ra-ui-tree-node/div/div[2]/ra-ui-static-text/div/div")

    # Deploy view
    DEPLOYBUTTON = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[1]/div/div/ra-ide-icons-toolbar/ul/li[1]/div[2]/ra-ui-icon-button/button/span[1]/mat-icon")
    CONTROLSHOWN = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[2]/div[1]/div[1]/ra-ide-panel[2]/div/ra-ide-panel[1]/div/ra-ide-tabs-outlet/div[2]/section/ra-ide-tab-content/div/div/ra-deploy/div/div[2]/ag-grid-angular/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/div/div/div[1]")

    # VCS
    SAVED = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-toolbar/div[1]/ra-ui-content-projection/div/div/ra-ui-static-text[2]/div")
    COMMIT = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[1]/div/div/ra-ide-icons-toolbar/ul/li[2]/div[1]/ra-ui-icon-button/button/span[1]/mat-icon")
    TIPECOMMIT = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-content/ra-dialog-form/div/ra-ui-dynamic-form/div/ra-ui-dynamic-form-schema/div/div/ra-ui-dynamic-form-category/div/mat-accordion/ra-ui-accordion-item/div/div/ra-ui-dynamic-form-area/div/div/ra-ui-dynamic-form-property/div/div/span/ra-ui-input/mat-form-field/div/div[1]/div[2]/input")
    COMMITBUTTON = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/mat-dialog-actions/div[2]/div[1]/ra-ui-main-button/button/span[1]/div/ra-ui-static-text/div")
    PUSHBUTTON = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[1]/div/div/ra-ide-icons-toolbar/ul/li[2]/div[2]/ra-ui-icon-button/button")
    CLOSETAB = (By.XPATH,"/html/body/div[1]/div[2]/div/mat-dialog-container/div/div/ra-extensible-dialog/div/div/div")
    PROJECTSINCRO = (By.XPATH,"/html/body/app-root/ra-ide-title-bar/div/ra-ui-product-header/div/mat-sidenav-container/mat-sidenav-content/ra-ide-app-shell/div/section[4]/ra-ide-status-bar/section/div[3]/ra-ide-status-bar-item[1]")

    # Locators for error messages
    ERROR_MESSAGE = (By.ID, "pe-err-message")

    ######################## APPLICATION FUNCTIONS ########################
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
        Opens the login page.
        """
        logger.info("🌐 Opening login page")
        self.open()

        # Check if we need to click on SSO button first
        if self.is_element_present(self.SIGN_IN_WITH_SSO_BUTTON, timeout=115):
            logger.info("🔍 SSO button detected, preparing to click")
            self.click_element(self.SIGN_IN_WITH_SSO_BUTTON)
        else:
            logger.debug("SSO button not present, proceeding directly to login form")

        # Wait for email input to be visible
        try:
            self.wait_for_element_visible(self.EMAIL_INPUT)
            logger.info("✅ Login page loaded successfully")
        except TimeoutException:
            logger.error("❌ Error: Could not load login page")
            self.take_screenshot("login_page_not_loaded")
            raise

        return self

    def wait_three_seconds(self):
        """
        Pauses execution for exactly 6 seconds (as per original code).
        Useful for waiting for elements to load or animations to complete.

        Returns:
            self: Returns self for method chaining
        """
        logger.info("⏱️ Waiting 6 seconds...") # Adjusted comment to match sleep time
        import time
        time.sleep(6)
        logger.info("✅ Wait of 6 seconds completed")
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
        Process to create a new project.
        """
        logger.info("🖱️ Attempting to click the 'New project' button")

        logger.info("Clicking to open projects")
        if self.is_element_present(self.NEW_PROJECT_BUTTON,timeout=160):
            self.wait_for_element_clickable(self.NEW_PROJECT_BUTTON)
            self.click_element(self.NEW_PROJECT_BUTTON)
            logger.info("✅ 'New project' button found and clicked successfully")
            # WRITING NAME
            logger.info("Waiting for button") # Consider more descriptive log: "Waiting for project name input"
            self.wait_for_element_visible(self.TYPE_PROJECT_NAME,timeout=160)
            logger.info("✅ 'Project name' field found successfully") # Adjusted log message
            return self
        # Consider adding an else block or raising an error if the button is not present

    def typing_name_project(self):
        """
        Function to type the name of the project (random).
        """
        try:
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            project_name = f"TestProject_{random_suffix}"
            logger.info(f"⌨️ Entering project name: '{project_name}'")
            self.wait_for_element_visible(self.TEXT_INPUT_PROJECT, timeout=110)
            self.click_element(self.TEXT_INPUT_PROJECT) # Click before inputting might be needed
            self.input_text(self.TEXT_INPUT_PROJECT, project_name)

        except Exception as e:
            logger.warning(f"Error with primary locator: {e}")
            # If it fails, try the alternative locator
            logger.info("Trying alternative locator for the name field")
            try: # Add try-except for the alternative locator as well
                self.wait_for_element_visible(self.PROJECT_NAME_INPUT_ALT, timeout=10) # Shorter timeout for alternative?
                self.click_element(self.PROJECT_NAME_INPUT_ALT)
                self.input_text(self.PROJECT_NAME_INPUT_ALT, project_name)
            except Exception as alt_e:
                logger.error(f"Alternative locator also failed: {alt_e}")
                self.take_screenshot("error_typing_project_name") # Screenshot on final failure
                raise alt_e # Re-raise the error from the alternative attempt
        return self


    def create_new_project_click(self):
        """
        Click on create button.
        """
        try:
            self.wait_for_element_visible(self.CREATE_PROJECT_BUTTON, timeout=110)
            self.click_element(self.CREATE_PROJECT_BUTTON)

        except Exception as e:
            logger.error(f"Error clicking create project button: {e}") # Changed level to error
            self.take_screenshot("error_create_project_click")
            raise
        return self

    def dismiss_button(self):
        """
        Dismiss vault project dialog (assuming).
        """
        try:
            # Increased timeout as sometimes dialogs take time to appear
            self.wait_for_element_visible(self.DISMISS_BUTTON, timeout=180)
            self.click_element(self.DISMISS_BUTTON)

        except Exception as e:
             # Log warning as sometimes this dialog might not appear
            logger.warning(f"Could not find or click dismiss button: {e}")
            self.take_screenshot("warning_dismiss_button_not_found")
            # Decide if this should raise an error or just be a warning
            # raise e # Uncomment if this step is critical
        return self

    def validate_gitlab(self):
        """Validating project synchronized message."""
        try:
            self.wait_for_element_visible(self.GITLAB_CHECK, timeout=180) # Increased timeout
            logger.info("✅ 'Project synchronized' indicator found successfully") # Adjusted message

        except Exception as e:
            logger.error(f"Error validating GitLab synchronization status: {e}")
            self.take_screenshot("error_validate_gitlab")
            raise
        return self

    def copilot_use(self):
        """Creating with Copilot."""

        try:
            PROMPT = "Create a Smart object( named SO_Copilot), with program(P1_Copilot)" # Changed var name convention
            logger.info(f"⌨️ Entering Copilot prompt")
            self.wait_for_element_visible(self.COPILOT, timeout=120)
            self.input_text(self.COPILOT, PROMPT, 110)
            self.wait_for_element_clickable(self.SendCOPILOT, 110) # Wait for clickable
            self.click_element(self.SendCOPILOT, 110)
            # Wait for the expected result (the created Smart Object node)
            self.wait_for_element_visible(self.SoCreated, 180) # Increased timeout
            logger.info("✅ Copilot interaction successful, Smart Object created.")

        except Exception as e:
            logger.error(f"Error during Copilot interaction: {e}")
            self.take_screenshot("error_copilot_use")
            raise
        return self

    def verifing_texts(self):
        """Here we validate all texts and views."""
        try:
            self.wait_for_element_visible(self.LOCALCHANGE,110)
            logger.info("✅ Text 'Local changes available' found successfully")
            self.wait_for_element_clickable(self.DEVICEVIEW,110)
            logger.info("✅ Device View found successfully")
            self.wait_for_element_clickable(self.EXPLORERVIEW,110)
            logger.info("✅ Explorer View found successfully")
            self.wait_for_element_clickable(self.LIBRARYVIEW,110)
            logger.info("✅ Library View found successfully")
            # It seems the next step is selecting the controller, which starts by clicking Device View again.
            # self.click_element(self.DEVICEVIEW,110) # Removed redundant click here
            logger.info("View verification done.") # Adjusted log message

        except Exception as e:
            logger.error(f"Error verifying views or 'Local Changes' text: {e}")
            self.take_screenshot("error_verifying_texts")
            raise
        return self

    def select_controller(self):
        """Select controller L85E."""
        try:
            logger.info("Navigating to Device View to add controller...")
            self.wait_for_element_clickable(self.DEVICEVIEW,120)
            # logger.info("✅ Device View found successfully") # Redundant log
            self.click_element(self.DEVICEVIEW,120)
            logger.info("Clicking 'New Device'...")
            self.click_element(self.NEWDEVICE,120)
            logger.info("Selecting 'Controllers' checkbox...")
            self.click_element(self.SELCONTROLLERS,120)
            logger.info("Selecting specific controller checkbox (L85E)...")
            self.click_element(self.CHECKBOX,120)
            logger.info("Clicking 'Continue'...")
            self.click_element(self.CONTINUECONTROL,120)
            logger.info("Entering controller name...")
            self.wait_for_element_visible(self.TIPENAME, 120) # Wait before clicking/typing
            self.click_element(self.TIPENAME,120) # Click might be needed to focus
            self.input_text(self.TIPENAME, "Controller_automate",120)
            logger.info("Clicking 'Finish'...")
            self.click_element(self.FINISH_BUTTON,120)
            logger.info("Waiting for Backplane to appear...")
            self.wait_for_element_visible(self.BACKPLANE,180) # Increased timeout
            logger.info("✅ Controller selection and addition done.")

        except Exception as e:
            logger.error(f"Error selecting or adding controller: {e}")
            self.take_screenshot("error_select_controller")
            raise
        return self

    def VCS(self):
        """Perform Version Control System (Commit & Push) steps."""
        try:
            logger.info("Performing VCS steps (Commit & Push)...")
            # Wait for save indicator - might need adjustment based on actual behavior
            logger.info("Waiting for 'Saved' indicator...")
            self.wait_three_seconds() # Consider replacing sleeps with explicit waits if possible
            self.wait_for_element_clickable(self.SAVED,120) # Is SAVED clickable or just visible? Adjust if needed.
            logger.info("✅ Project saved. Proceeding with commit.")
            logger.info("Clicking 'Commit' button...")
            self.click_element(self.COMMIT,120)
            logger.info("Entering commit message...")
            self.input_text(self.TIPECOMMIT, "COMMIT AUTOMATED",120)
            logger.info("Clicking final 'Commit' button...")
            self.click_element(self.COMMITBUTTON,120)
            # Wait after commit before push
            self.wait_three_seconds()
            logger.info("Clicking 'Push' button...")
            self.wait_for_element_clickable(self.PUSHBUTTON,120)
            self.click_element(self.PUSHBUTTON,120)
            # Handle potential push confirmation/result dialog
            logger.info("Closing push result dialog (if present)...")
            # This assumes CLOSETAB closes the push result dialog. Timeout might need adjustment.
            # Use is_element_present if the dialog doesn't always appear.
            try:
                self.click_element(self.CLOSETAB, 60) # Shorter timeout for closing dialog
            except TimeoutException:
                logger.warning("Push result dialog close button not found or timed out.")
            # Wait for project synchronization status update
            logger.info("Waiting for project synchronization status...")
            self.wait_three_seconds() # Consider replacing sleeps
            self.wait_three_seconds()
            self.wait_for_element_clickable(self.PROJECTSINCRO,180) # Increased timeout, check if clickable or visible
            logger.info("✅ VCS steps (Commit & Push) done.")

        except Exception as e:
            logger.error(f"Error during VCS steps: {e}")
            self.take_screenshot("error_vcs")
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

    ################ AUTOMATION STEPS ################


    def complete_test(self, email, password):
        """
        Complete the full test process.

        Args:
            email (str): Email address to use
            password (str): Password to use

        Returns:
            self for method chaining
        """
        logger.info(f"🔐 Starting test process with email: {email}")

        # Open login page (will handle SSO button if needed)
        logger.info("STEP 1: Open login page")
        print("Opening login page ✅")
        self.open_login_page()

        # Enter email and continue
        logger.info("STEP 2: Enter email address")
        print("Entering email address ✅")
        self.enter_email(email)

        logger.info("STEP 3: Click Continue button")
        print("Clicking Continue button ✅")
        self.click_continue()

        # Enter password and sign in
        logger.info("STEP 4: Enter password")
        print("Entering password ✅")
        self.enter_password(password)

        logger.info("STEP 5: Click Sign In button")
        print("Clicking Sign In button ✅")
        self.click_sign_in()

        logger.info("STEP 6: Click new project")
        print("Clicking new project ✅")
        self.step_new_project()

        logger.info("STEP 7: Typing random name")
        print("Typing random name ✅")
        self.typing_name_project()

        logger.info("STEP 8: Click create new project")
        print("Clicking create new project ✅")
        self.create_new_project_click()
        logger.info("Clicking dismiss button") # Keep logger for details
        self.dismiss_button()
        self.take_screenshot("New project Step")
        print("Clicked dismiss button ✅") # Keep print for high-level step

        logger.info("STEP 9: Validating Gitlab and using Copilot") # Combined log
        print("Validating Gitlab and using Copilot ✅")
        self.validate_gitlab()
        self.copilot_use()

        logger.info("STEP 10: Create Smart object and validate views")
        print("Creating Smart object and validating views ✅")
        self.verifing_texts()
        self.take_screenshot("Creation of Smart Objects")
        print("Taking photos ✅") # "Taking screenshot" is more accurate

        logger.info("STEP 11: Select controller")
        print("Selecting controller L85E ✅")
        self.select_controller()
        self.take_screenshot("Devices")

        logger.info("STEP 12: VCS")
        print("Performing VCS steps ✅") # Changed print message slightly
        self.VCS()
        self.take_screenshot("VCS")

        logger.info("✅ Test finished") # Keep logger


        # Take a final screenshot
        self.take_screenshot("final step")
        print("Taking final screenshot ✅") # Changed print message

        # Here we could return the next page (e.g., DashboardPage) if needed
        return self