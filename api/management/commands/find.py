from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from django.core.management.base import BaseCommand
from urllib.parse import urlencode
from time import sleep


URL = 'https://glasgow.summon.serialssolutions.com/?s.'
CONTENT_TYPES = ['Book / eBook']
DISCIPLINES = ['Computer science']


class Command(BaseCommand):
    help = 'Find a top N books from the Glasgow University library ' \
           '(specify number and searched title as the command arguments)'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str)
        parser.add_argument('number', nargs='?', type=int, default=20)

    @staticmethod
    def set_driver(search_title):
        """ Initialize driver with a closed browser and redirect to the search page """
        browser_options = FirefoxOptions()
        browser_options.headless = False
        driver = Firefox(options=browser_options)
        driver.implicitly_wait(5)
        query = {'q': search_title}
        driver.get(URL + urlencode(query))
        return driver

    @staticmethod
    def get_books(driver, number) -> list[dict]:
        books: list[dict]
        books = []

        # find titles and links
        headings = driver.find_elements(By.CSS_SELECTOR, '.customPrimaryLinkContainer.ng-scope')[:number]
        for element in headings:
            a = element.find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'a')
            books.append({'title': a.text, 'link': a.get_attribute('href')})

        authors = driver.find_elements(By.CSS_SELECTOR, '.customPrimaryLink.ng-binding')[:number]
        years = driver.find_elements(By.CSS_SELECTOR, '.shortSummary.ng-binding.ng-scope')[:number]
        # find type (book or eBook) for each result
        types = driver.find_elements(By.CSS_SELECTOR, '.contentType.ng-binding.minimalist')[:number]

        for i in range(number):
            books[i]['author'] = authors[i].text
            books[i]['year'] = years[i].text[:4]
            books[i]['type'] = types[i].text

        return books

    def handle(self, *args, **kwargs):
        # web-driver configuration
        driver = self.set_driver(kwargs['title'])

        # filter by 'book / eBook'
        for option in CONTENT_TYPES:
            driver.find_element(By.LINK_TEXT, option).click()

        # filter by disciplines
        for discipline in DISCIPLINES:
            search = driver.find_element(By.XPATH, "//*[starts-with(@id, 'moreFacetsFilter')]")
            search.click()
            search.send_keys(discipline)
            driver.find_element(By.LINK_TEXT, discipline).click()

        # get enough results ( >= default number/number from command-line args.) on the page
        while True:
            numbers_elems = driver.find_elements(By.CSS_SELECTOR, '.resultNumber.ng-binding.ng-scope')
            last_number = int(numbers_elems[-1].text)
            print(last_number)
            if last_number >= kwargs['number']:
                print('finish')
                break
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(5)

        books = self.get_books(driver, kwargs['number'])
        print(*books, sep='\n')
        #driver.quit()
