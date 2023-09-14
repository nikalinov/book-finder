from selenium.common import NoSuchElementException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from django.core.management.base import BaseCommand
from _finders import GlasgowFinder, GoodreadsFinder
from urllib.parse import urlencode
from time import sleep
from re import search
import sys
import os


class Command(BaseCommand):
    help = 'Find a top N books from the Glasgow University library ' \
           '(specify number and searched title as the command arguments)'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str)
        parser.add_argument('number', nargs='?', type=int, default=20)

    def handle(self, *args, **kwargs):
        glasgow_finder = GlasgowFinder()
        books = glasgow_finder.find_books(kwargs['title'], kwargs['number'])

        # print(*books, sep='\n\n')
        goodreads_finder = GoodreadsFinder()
        books = goodreads_finder.find_ratings(books)
