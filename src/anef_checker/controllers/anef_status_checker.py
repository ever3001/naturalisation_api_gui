"""Module for checking naturalization application status on the ANEF website."""

from __future__ import annotations

import os
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Final,
    Optional,
)

import chromedriver_autoinstaller  # type: ignore[import-untyped]
from dotenv import load_dotenv
from loguru import logger
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
)
from selenium import webdriver

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

load_dotenv()

DEFAULT_TIMEOUT: Final[int] = 10
BASE_URL: Final[str] = 'https://administration-etrangers-en-france.interieur.gouv.fr'


class ANEFCredentials(BaseModel):
    """ANEF authentication credentials model."""

    username: str = Field(..., min_length=1)
    password: SecretStr = Field(..., min_length=1)
    base_url: str = Field(default=BASE_URL)


class ANEFStatusChecker(BaseModel):
    """Handles checking naturalization application status on the ANEF website."""

    credentials: ANEFCredentials
    _driver: Optional[WebDriver] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __enter__(self) -> ANEFStatusChecker:
        """Initialize the ANEFStatusChecker and return it for use in a with statement."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:  # type: ignore[no-untyped-def] # noqa: ANN001
        """Cleanup resources when exiting the with statement."""
        self.cleanup()

    def _setup_webdriver(self) -> WebDriver:
        """Initialize and configure Chrome WebDriver."""
        chromedriver_autoinstaller.install()  # Automatically installs chromedriver if needed
        options = webdriver.ChromeOptions()
        if os.getenv('SELENIUM_HEADLESS', 'true').lower() == 'true':
            options.add_argument('--headless')
        return webdriver.Chrome(options=options)

    @property
    def driver(self) -> WebDriver:
        """Lazy initialization of the WebDriver."""
        if not self._driver:
            self._driver = self._setup_webdriver()
        return self._driver

    def _wait_for_element(self, by: str, value: str, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """Wait for an element to be present on the page."""
        return WebDriverWait(self.driver, timeout).until(expected_conditions.presence_of_element_located((by, value)))

    def _inject_status_interceptor(self) -> None:
        """Inject JavaScript to intercept the application status response."""
        script = '''
        (function() {
            const originalCall = Function.prototype.call;
            Function.prototype.call = function(...args) {
                const result = originalCall.apply(this, args);
                if (result?.dossier?.statut && result.dossier.statut.length < 150) {
                    window.myDossier = result.dossier;
                }
                return result;
            };
        })();
        '''
        self.driver.execute_script(script)  # type: ignore[no-untyped-call]

    def login(self) -> None:
        """Perform login to the ANEF website."""
        self.driver.get(str(self.credentials.base_url))

        # Wait for necessary elements and click the login link
        self._wait_for_element(By.ID, 'connexion_link')
        self._wait_for_element(By.XPATH, "//span[contains(text(), 'Je valide mon VLS-TS')]")
        self.driver.find_element(By.ID, 'connexion_link').click()

        # Fill in credentials and submit the form
        self._wait_for_element(By.ID, 'login')
        username_field = self.driver.find_element(By.ID, 'login')
        password_field = self.driver.find_element(By.ID, 'password')
        username_field.send_keys(self.credentials.username)
        password_field.send_keys(self.credentials.password.get_secret_value())
        self.driver.find_element(By.XPATH, '//button[@type="submit"]').click()

        # Confirm successful login by waiting for a specific element
        self._wait_for_element(By.XPATH, "//a[@aria-label='CONFORMITY_DECLARATION.CHECKED_LINKS.MY_ACCOUNT.LABEL']")

    def navigate_to_status_page(self) -> None:
        """Navigate to the naturalization status page."""
        account_url = f'{self.credentials.base_url}/particuliers/#/espace-personnel/mon-compte'
        self.driver.get(account_url)

        naturalization_link = self._wait_for_element(
            By.XPATH,
            '//span[contains(text(), "Demande d\'accès à la Nationalité Française")]',
        )
        self._inject_status_interceptor()
        naturalization_link.click()

    def get_application_status(self) -> Dict[str, Any]:
        """Retrieve the naturalization application status."""
        WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(
            lambda d: d.execute_script("return typeof window.myDossier !== 'undefined';"),  # type: ignore[no-untyped-call]
        )
        dossier: Dict[str, Any] = self.driver.execute_script('return window.myDossier;')  # type: ignore[no-untyped-call]
        return dossier

    def cleanup(self) -> None:
        """Close the browser and cleanup resources."""
        if self._driver:

            self._driver.quit()
            self._driver = None


def check_naturalization_status(credentials: ANEFCredentials) -> Dict[str, Any]:
    """Check naturalization application status using provided credentials."""
    if not credentials:
        raise RuntimeError(
            'Missing required credentials',
        )
    with ANEFStatusChecker(credentials=credentials) as checker:
        try:
            checker.login()
            checker.navigate_to_status_page()
            application_status = checker.get_application_status()
            logger.debug(application_status)
            return application_status
        except TimeoutException:
            logger.error('Timeout occurred while checking naturalization status. Please checks your credentials.')
            return {}
