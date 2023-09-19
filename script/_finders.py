from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from urllib.parse import urlencode
from django.conf import settings
from django.urls import reverse
from requests import post
from time import sleep
from re import search
from os import devnull


GLASGOW_URL = 'https://glasgow.summon.serialssolutions.com/'
GOODREADS_URL = 'https://www.goodreads.com/'
CONTENT_TYPES = ['Book / eBook']


class BookFinder:
    def __init__(self, title, number):
        self.title = title
        self.number = number
        self.books = []

    def find_books(self):
        """ Returns JSON representation of found books """
        glasgow_finder = GlasgowFinder(self.title, self.number)
        self.books = glasgow_finder.find_books()

        goodreads_finder = GoodreadsFinder(self.books)
        goodreads_finder.find_ratings()

    def send_books(self):
        """ Sends POST request with JSON to the server """
        url_end = reverse('book-list')
        url = f'{settings.BASE_URL}{url_end}'
        for book in self.books:
            request = post(url, json=book)

            """if str(request.status_code)[0] != '2':
                print(f'response: {request.text}')
                print(book)"""


def setup_driver():
    """ Initialize driver with a closed browser and redirect to the search page """
    browser_options = FirefoxOptions()
    browser_options.headless = True
    service = Service(log_path=devnull)
    driver = Firefox(options=browser_options, service=service)
    return driver


class GlasgowFinder:
    def __init__(self, title, number):
        self.title = title
        self.number = number
        self.driver = None
        books: list[dict]
        self.books = []

    def add_title_link(self, book_element: WebElement):
        heading = book_element.find_element(By.CSS_SELECTOR, '.customPrimaryLinkContainer.ng-scope')
        a = heading.find_element(By.TAG_NAME, 'span').find_element(By.TAG_NAME, 'a')
        self.books.append({'title': a.text, 'glasgow_link': a.get_attribute('href')})

    def add_authors(self, book_element: WebElement):
        authors_block = book_element.find_element(By.XPATH, ".//div[@class='authors']")
        authors_block = authors_block.find_elements(By.CSS_SELECTOR, '.customPrimaryLink.ng-binding')
        authors = []
        for author in authors_block:
            authors.append(author.text)
        self.books[-1]['authors'] = '; '.join(authors)

    def add_year(self, book_element: WebElement):
        year_info = book_element.find_element(By.CSS_SELECTOR, '.shortSummary.ng-binding.ng-scope').text
        try:
            year = int(search(r'(19|20)\d{2}', year_info).group(0))
        except AttributeError:
            year = None
        self.books[-1]['year'] = year

    def add_types(self, book_element: WebElement):
        types = book_element.find_element(
            By.CSS_SELECTOR,
            '.availability.documentSummaryAvailability.availabilityContent.ng-scope'
        )
        self.books[-1]['types'] = []
        try:
            types.find_element(By.CSS_SELECTOR, '.contentType.ng-binding.minimalist')
            self.books[-1]['types'].append('Book')
        except NoSuchElementException:
            pass
        try:
            types.find_element(By.CSS_SELECTOR, '.contentType.ng-binding')
            self.books[-1]['types'].append('eBook')
        except NoSuchElementException:
            pass
        self.books[-1]['types'] = '; '.join(self.books[-1]['types'])

    def get_books(self) -> list[dict]:
        # results web-elements/blocks
        results = self.driver.find_elements(By.XPATH, "//div[starts-with(@id,'FETCH-glasgow_catalog')]")[:self.number]

        for res in results:
            # find book's title and link
            self.add_title_link(res)

            # find book's author(s)
            self.add_authors(res)

            # find book's year
            self.add_year(res)

            # find type (book and/or eBook) for each result
            self.add_types(res)

        return self.books

    def show_results(self):
        # filter by 'Book / eBook'
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

    def find_books(self):

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
    def __init__(self, books):
        self.books = books

    def find_ratings(self):
        self.books = self.books
        driver = setup_driver()

        for book in self.books:
            driver.get(GOODREADS_URL + 'search?' + urlencode({'q': book['title']}))

            try:
                driver.find_element(By.CSS_SELECTOR, '[itemprop="name"][role="heading"][aria-level="4"]')
            except NoSuchElementException:
                continue

            # find average rating and number of reviews
            rating_info = driver.find_element(By.CLASS_NAME, 'minirating').text
            rating = float(search(r'\d\.\d{2}', rating_info).group(0))
            reviews = int(search(r'\d+', rating_info[::-1]).group(0))
            if reviews == 0:
                rating = None
            book['rating'] = rating
            book['reviews'] = reviews

            # find link to the book
            link = driver.find_element(By.XPATH, '//a[starts-with(@href,"/book/show/")]').get_attribute('href')
            book['goodreads_link'] = link

        """for book in books:
            for k, v in book.items():
                print(f'{k}: {v}')
            print()"""
