from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class Selenium:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


class SeleniumWith:
    def __init__(self) -> None:
        self.selenium = Selenium()
    
    def __enter__(self):
        return self.selenium.driver

    def __exit__(self, type, value, triceback):
        for handle in self.selenium.driver.window_handles:
            self.selenium.driver.switch_to.window(handle)
            self.selenium.driver.close()
        self.selenium = None
        print(triceback)
        