from selenium.common import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxOptions, ActionChains
from selenium.webdriver.common.by import By
from django.core.management.base import BaseCommand
from urllib.parse import urlencode
from time import sleep
from re import search

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

URL = 'https://glasgow.summon.serialssolutions.com/?s.'
CONTENT_TYPES = ['Book / eBook']


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
        query = {'q': search_title}
        url = URL + urlencode(query)
        driver.get(url)
        return driver

    @staticmethod
    def get_books(driver, number) -> list[dict]:
        books: list[dict]
        books = []

        # results web-elements/blocks
        results = driver.find_elements(By.XPATH, "//div[starts-with(@id,'FETCH-glasgow_catalog')]")[:number]

        for res in results:
            # find book's title and link
            heading = res.find_element(By.CSS_SELECTOR, '.customPrimaryLinkContainer.ng-scope')
            a = heading.find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'a')
            books.append({'title': a.text, 'link': a.get_attribute('href')})

            # find book's author(s)
            authors = res.find_element(By.XPATH, ".//div[@class='authors']")
            authors = authors.find_elements(By.CSS_SELECTOR, '.customPrimaryLink.ng-binding')
            books[-1]['authors'] = []
            for author in authors:
                books[-1]['authors'].append(author.text)

            # find book's year
            year_info = res.find_element(By.CSS_SELECTOR, '.shortSummary.ng-binding.ng-scope').text
            year = search(r'(19|20)\d{2}', year_info).group(0)
            books[-1]['year'] = year

            # find type (book and/or eBook) for each result
            types = driver.find_element(
                By.CSS_SELECTOR,
                '.availability.documentSummaryAvailability.availabilityContent.ng-scope'
            )
            books[-1]['types'] = []
            try:
                types.find_element(By.CSS_SELECTOR, '.contentType.ng-binding.minimalist')
                books[-1]['types'].append('Book')
            except NoSuchElementException:
                pass
            try:
                types.find_element(By.CSS_SELECTOR, '.contentType.ng-binding')
                books[-1]['types'].append('eBook')
            except NoSuchElementException:
                pass

        return books

    @staticmethod
    def show_results(driver, number):
        # filter by 'book / eBook'
        for option in CONTENT_TYPES:
            WebDriverWait(driver, 3).until(
                expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR, f"[title='{option}']")
                )
            )
            driver.find_element(By.CSS_SELECTOR, f"[title='{option}']").click()

        # get enough results ( >= default number/number from command-line args.) on the page
        while True:
            numbers_elems = driver.find_elements(By.CSS_SELECTOR, '.resultNumber.ng-binding.ng-scope')
            last_number = int(numbers_elems[-1].text)
            if last_number >= number:
                break
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(1)

        return driver

    def handle(self, *args, **kwargs):
        # web-driver configuration
        driver = self.set_driver(kwargs['title'])
        # showing enough ( >= requested book number) results on the page to extract
        driver = self.show_results(driver, kwargs['number'])
        # structuring results into list of dictionaries (representation of each book)
        books = self.get_books(driver, kwargs['number'])

        driver.quit()
