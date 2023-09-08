from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from django.core.management.base import BaseCommand
from urllib.parse import urlencode


URL = 'https://glasgow.summon.serialssolutions.com/?s.'


class Command(BaseCommand):
    help = 'Find a top N books from the Glasgow University library ' \
           '(specify number and searched title as the command arguments)'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str)
        parser.add_argument('number', nargs='?', type=int, default=10)

    def handle(self, *args, **kwargs):
        # self.stdout.write(self.style.SUCCESS(f'title: {kwargs["title"]}, number: {kwargs["number"]}'))
        browser_options = FirefoxOptions()
        browser_options.headless = True
        driver = Firefox(options=browser_options)

        query = {'q': kwargs['title']}
        driver.get(URL + urlencode(query))

        # results = driver.find_element(By.ID, 'results').find_element(By.CLASS_NAME, 'inner')

        driver.quit()
