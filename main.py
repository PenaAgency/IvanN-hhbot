import argparse
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from helpers import hh_login, find_with_filters, apply
from selenium_class import SeleniumWith


def main(args):
    password = args.password
    login = args.login
    search_url = args.search_url
    letter_path = args.letter_path
    
    if letter_path is not None:
        with open(letter_path, 'r') as file:
            covering_letter = file.read()
    else:
        covering_letter = None

    with SeleniumWith() as driver:
        driver.get('https://hh.ru/')
        driver.maximize_window()
        # Wait to find elements
        driver.implicitly_wait(20)

        driver = hh_login(driver, password, login)
        driver = find_with_filters(driver, search_url)
        
        # covering_letter = 'Пожалуйста рассмотрите мое резюме.'
        driver = apply(driver, search_url, covering_letter=covering_letter)

        time.sleep(10)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Agrs for programm')
    parser.add_argument('-password', dest='password', help='Password from hh.ru')
    parser.add_argument('-login', dest='login', help='Email or phone from hh.ru')
    parser.add_argument('-letter_path', dest='letter_path', default=None, help='Path to covering letter')
    parser.add_argument('-search_url', dest='search_url', help='Search string')
    args = parser.parse_args()
    main(args)
    