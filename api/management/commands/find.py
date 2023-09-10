from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from django.core.management.base import BaseCommand
from urllib.parse import urlencode
from time import sleep


URL = 'https://glasgow.summon.serialssolutions.com/?s.'
FILTERS = ['Book / eBook']


class Command(BaseCommand):
    help = 'Find a top N books from the Glasgow University library ' \
           '(specify number and searched title as the command arguments)'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str)
        parser.add_argument('number', nargs='?', type=int, default=10)

    def handle(self, *args, **kwargs):
        browser_options = FirefoxOptions()
        browser_options.headless = False
        driver = Firefox(options=browser_options)
        driver.implicitly_wait(5)
        query = {'q': kwargs['title']}
        driver.get(URL + urlencode(query))

        for option in FILTERS:
            driver.find_element(By.LINK_TEXT, option).click()

        while True:
            numbers_elems = driver.find_elements(By.CSS_SELECTOR, '.resultNumber.ng-binding.ng-scope')
            last_number = int(numbers_elems[-1].text)
            print(last_number)
            if last_number >= kwargs['number']:
                print('finish')
                break
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(5)

        # results = driver.find_element(By.ID, 'results').find_element(By.CLASS_NAME, 'inner')
        # driver.quit()
