import contextlib
import os

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from core.exceptions.web_driver import UnableToRenderPage


class WebDriverManager:
    def __init__(self):
        self.driver = None
        self.options = None
        self.dc = None
        self.initiate_configurations()

    def initiate_configurations(self):
        # Create Chromeoptions instance
        self.options = webdriver.ChromeOptions()

        # Adding argument to disable the AutomationControlled flag
        self.options.add_argument("--disable-blink-features=AutomationControlled")

        # Exclude the collection of enable-automation switches
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Turn-off userAutomationExtension
        self.options.add_experimental_option("useAutomationExtension", False)

        session_folder_path = os.path.join(os.getcwd(), 'core', 'session')

        # Update the options.add_argument line to use the new path
        self.options.add_argument(f"user-data-dir={session_folder_path}")

        # Check if the current version of chromedriver exists
        # and if it doesn't exist, download it automatically,
        # then add chromedriver to path
        chromedriver_autoinstaller.install()

    def start_driver(self):
        self.driver = webdriver.Chrome(options=self.options)

    def refresh_driver(self):
        if self.driver:
            self.driver.quit()
        self.start_driver()

    def close_driver(self):
        if self.driver:
            self.driver.quit()
        self.driver = None

    def navigate_to(self, url, raise_exception=False):
        if not self.driver:
            self.start_driver()
        try:
            self.driver.get(url)
        except TimeoutException:
            if raise_exception:
                raise UnableToRenderPage

    def open_new_tab(self, url=None, raise_exception=False):
        if self.driver:
            self.driver.execute_script("window.open('', '_blank');")
            self.switch_to_new_window()
        else:
            self.start_driver()
        if url:
            self.navigate_to(url, raise_exception=raise_exception)

    def switch_to_new_window(self):
        if self.driver:
            self.driver.switch_to.window(self.driver.window_handles[-1])
        else:
            self.start_driver()

    def close_current_tab(self):
        try:
            if self.driver:
                self.driver.close()
            self.switch_to_new_window()
        except Exception:
            self.switch_to_new_window()

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def find_element_with_wait(self, locator, wait=5):
        try:
            return WebDriverWait(self.driver, wait).until(
                lambda x: x.find_element(
                    *locator
                )
            )
        except TimeoutException as e:
            return None

    def find_elements_with_wait(self, locator, wait=5):
        try:
            return WebDriverWait(self.driver, wait).until(
                lambda x: x.find_elements(
                    *locator
                )
            )
        except TimeoutException as e:
            return []

    def scroll_to_bottom(self, max_iterations=5):
        SCROLL_COMMAND = "return document.body.scrollHeight"
        next_height = initial_height = self.driver.execute_script(SCROLL_COMMAND)
        for _ in range(max_iterations):
            with contextlib.suppress(TimeoutException):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(self.driver, 1).until(
                    lambda driver: driver.execute_script(SCROLL_COMMAND) > next_height)
            next_height = self.driver.execute_script(SCROLL_COMMAND)

        # Check if the page content has actually changed
        final_height = self.driver.execute_script(SCROLL_COMMAND)
        return final_height != initial_height

    @staticmethod
    def _find_element_with_wait(element, locator, wait=5):
        try:
            return WebDriverWait(element, wait).until(
                lambda x: x.find_element(
                    *locator
                )
            )
        except TimeoutException as e:
            return None
