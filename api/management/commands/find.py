from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from django.core.management.base import BaseCommand
from urllib.parse import urlencode


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

        """while True:
            numbers_elems = driver.find_elements(By.CLASS_NAME, 'resultNumber ng-binding bg-scope')
            numbers = [elem.text for elem in numbers_elems]
            print(numbers_elems)
            print()
            if numbers[-1] >= kwargs['number']:
                break
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')"""

        numbers_elems = driver.find_elements(By.CSS_SELECTOR, '.resultNumber.ng-binding.bg-scope')
        numbers = [elem.text for elem in numbers_elems]

        # results = driver.find_element(By.ID, 'results').find_element(By.CLASS_NAME, 'inner')

        #driver.quit()
