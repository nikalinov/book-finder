from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
from time import sleep
from re import search
import json


GLASGOW_URL = 'https://glasgow.summon.serialssolutions.com/'
GOODREADS_URL = 'https://www.goodreads.com/'
CONTENT_TYPES = ['Book / eBook']


class BookFinder:
    def __init__(self, title, number):
        self.title = title
        self.number = number
        self.books_json = []

    def find_books(self):
        """ Returns JSON representation of found books """
        glasgow_finder = GlasgowFinder()
        books = glasgow_finder.find_books(self.title, self.number)

        goodreads_finder = GoodreadsFinder()
        books = goodreads_finder.find_ratings(books)
        books_json = json.dumps(books, indent=4)
        print(books_json)
        self.books_json = books_json

    def send_books(self):
        """ Sends POST request with JSON to the server """
        pass


def setup_driver():
    """ Initialize driver with a closed browser and redirect to the search page """
    browser_options = FirefoxOptions()
    browser_options.headless = True
    driver = Firefox(options=browser_options)
    return driver


class GlasgowFinder:
    def __init__(self):
        self.title = ""
        self.number = 20
        self.driver = None

    def get_books(self) -> list[dict]:
        books: list[dict]
        books = []

        # results web-elements/blocks
        results = self.driver.find_elements(By.XPATH, "//div[starts-with(@id,'FETCH-glasgow_catalog')]")[:self.number]

        for res in results:
            # find book's title and link
            heading = res.find_element(By.CSS_SELECTOR, '.customPrimaryLinkContainer.ng-scope')
            a = heading.find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'a')
            books.append({'title': a.text, 'glasgow_link': a.get_attribute('href')})

            # find book's author(s)
            authors = res.find_element(By.XPATH, ".//div[@class='authors']")
            authors = authors.find_elements(By.CSS_SELECTOR, '.customPrimaryLink.ng-binding')
            books[-1]['authors'] = []
            for author in authors:
                books[-1]['authors'].append(author.text)

            # find book's year
            year_info = res.find_element(By.CSS_SELECTOR, '.shortSummary.ng-binding.ng-scope').text
            try:
                year = int(search(r'(19|20)\d{2}', year_info).group(0))
            except AttributeError:
                year = None
            books[-1]['year'] = year

            # find type (book and/or eBook) for each result
            types = self.driver.find_element(
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

    def show_results(self):
        # filter by 'book / eBook'
        for option in CONTENT_TYPES:
            WebDriverWait(self.driver, 5).until(
                expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR, f"[title='{option}']")
                )
            )
            self.driver.find_element(By.CSS_SELECTOR, f"[title='{option}']").click()

        # get enough results ( >= default number/number from command-line args.) on the page
        while True:
            numbers_elems = self.driver.find_elements(By.CSS_SELECTOR, '.resultNumber.ng-binding.ng-scope')
            last_number = int(numbers_elems[-1].text)
            if last_number >= self.number:
                break
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(1)

    def find_books(self, title, number):
        self.title = title
        if number:
            self.number = number

        # web-driver configuration
        self.driver = setup_driver()
        self.driver.get(GLASGOW_URL + '?' + urlencode({'q': self.title}))
        # showing enough ( >= requested book number) results on the page to extract
        self.show_results()
        # structuring results into list of dictionaries (representation of each book)
        books = self.get_books()

        self.driver.quit()
        return books


class GoodreadsFinder:
    def __init__(self):
        self.books = []

    def find_ratings(self, books):
        self.books = books
        driver = setup_driver()

        for book in self.books:
            driver.get(GOODREADS_URL + 'search?' + urlencode({'q': book['title']}))

            try:
                driver.find_element(By.CSS_SELECTOR, '[itemprop="name"][role="heading"][aria-level="4"]')
            except NoSuchElementException:
                continue

            # find average rating and number of reviews
            rating_info = driver.find_element(By.CLASS_NAME, 'minirating').text
            average = float(search(r'\d\.\d{2}', rating_info).group(0))
            reviews = int(search(r'\d+', rating_info[::-1]).group(0))
            book['average'] = average
            book['reviews'] = reviews

            # find link to the book
            link = driver.find_element(By.XPATH, '//a[starts-with(@href,"/book/show/")]').get_attribute('href')
            book['goodreads_link'] = link

        """for book in books:
            for k, v in book.items():
                print(f'{k}: {v}')
            print()"""
        return self.books
