import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


NOT_WORKING_LINKS = []


def hh_login(driver, password, login):
    sign_in = driver.find_element(By.CSS_SELECTOR,'.supernova-button[data-qa="login"]')
    sign_in.click()
    sign_in_by_pass = driver.find_element(By.CSS_SELECTOR,'button[data-qa="expand-login-by-password"]')
    sign_in_by_pass.click()

    login_input = driver.find_element(By.CSS_SELECTOR, 'input[data-qa="login-input-username"]')
    login_input.click()
    login_input.clear()
    login_input.send_keys(login)
    pass_input = driver.find_element(By.CSS_SELECTOR, 'input[data-qa="login-input-password"]')
    pass_input.click()
    pass_input.clear()
    pass_input.send_keys(password)
    sign_in_button = driver.find_element(By.CSS_SELECTOR,'button[data-qa="account-login-submit"]')
    sign_in_button.click()
    return driver


def find_with_filters(driver, search_url):
    driver.get("https://dzen.ru/")
    driver.get(search_url)
    return driver


def apply(driver, search_url, covering_letter=None):
    '''Apply with covering letter'''

    try:
        paginate_links = driver.find_elements(By.CSS_SELECTOR, 'a[data-qa="pager-page"]')
    except NoSuchElementException:
        paginate_links = []
    paginate_links = [i.get_attribute('href') for i in paginate_links] if paginate_links else []
    paginate_links = [search_url, *paginate_links] 

    for page, url in enumerate(paginate_links, 1):
        if page == 1:
            apply_on_page(driver, covering_letter=covering_letter)
        else:
            driver.get(url)
            apply_on_page(driver, covering_letter=covering_letter)

    return driver


def apply_on_page(driver, covering_letter=None):
    vacancies_links = driver.find_elements(By.CSS_SELECTOR, 'a.serp-item__title[data-qa="serp-item__title"]')
    vacancies_links = get_vacancies_url(vacancies_links)
    main_window = driver.window_handles[0]

    for url in vacancies_links:
        if url in NOT_WORKING_LINKS:
            continue
        # open new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        # Need to exclude redirect on test task from employer
        driver.get(url)
        current_url = driver.current_url
        
        try:
            apply_button = driver.find_element(By.CSS_SELECTOR, 'a[data-qa="vacancy-response-link-top"]')
            apply_button.click()
            time.sleep(1)

            if current_url != driver.current_url:
                NOT_WORKING_LINKS.append(url)
            elif current_url == driver.current_url and covering_letter:
                letter_button = driver.find_element(By.CSS_SELECTOR, 'button[data-qa="vacancy-response-letter-toggle"]')
                letter_button.click()

                text_input = driver.find_element(By.CSS_SELECTOR, 'textarea[name="text"]')
                text_input.click()
                text_input.clear()
                text_input.send_keys(covering_letter)
                send_letter_button = driver.find_element(By.CSS_SELECTOR, 'button[data-qa="vacancy-response-letter-submit"]')
                send_letter_button.click()
        except NoSuchElementException:
            print(f'No apply button on {url}')
        
        driver.close()
        driver.switch_to.window(main_window)


    return driver


def get_vacancies_url(vacancies_links):
    links = [i.get_attribute('href').replace('/analytics_source', '') for i in vacancies_links]
    return [i for i in links if i not in NOT_WORKING_LINKS]