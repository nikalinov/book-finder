# Book finder
* A script that finds books on the Glasgow University library resource, takes reviews from Goodreads, and structures it in a database within Django environment.
* After the script is run, the JSON object is formed from the book results and sent to the server.
* Using sorting and/or filtering queries in a url, one can retrieve the books without empty reviews and sorted by number of reviews/best rating.
## Table of contents:
* [Getting started](#getting-started)
* [Usage guide](#usage-guide)
* [Technologies used](#technologies-used)
## Getting started
0. Prerequisites: installed Python (version at least 3).
1. Set up a local copy of the repository.  
  1.1. Open a terminal and navigate to the directory that you would like the Book finder to be stored in;  
  1.2. In the terminal, run to clone the repository into the current directory:
   ```
   git clone https://github.com/nikalinov/book_finder.git
   ```
3. Navigate into the Book finder directory and create a virtual environment:
   ```
   python3 -m venv <enter-venv-name-here>
   ```
5. Activate the virtual environment:  
   ```
   $ source <enter-venv-name-here>/bin/activate  
   ```
   (Linux/MacOS)  
   **or**  
   ```
   <enter-venv-name-here>\Scripts\activate.bat
   ```
   (Windows)
6. Install the prerequisite modules/libraries from requirements.txt:  
   ```
   pip install -r requirements.txt
   ```
7. It is needed to create a personal Django secret key. For that, navigate to the 'book_finder' directory  
   (which is in the original 'book_finder' project directory) and run:  
   ```
   python3 secret_key_generator.py
   ```
## Usage guide
1. To turn on the Django server for sending data, run from the root directory:
   ```
   python3 manage.py runserver
   ```
3. Open another command line window to start a separate session, navigate into the 'script' directory of  
   the project and run the command:  
   ```
   python3 find.py <enter-your-title-here> <enter-number-of-results-here>
   ```
   where the search query can be any phrase/word and the number must be at least 15.  
   One can omit the number and it will default to 15. For example,  
   ```
   python3 find.py python 20
   ```
   or
   ```
   python3 find.py java
   ```
   In case everything works correctly, the 2 messages will be displayed:  
   ```
   Successfully found books!
   Successfully sent books to the server!
   ```
5. The sent data is available via endpoints `http://127.0.0.1:8000/api/book/list/` (GET - retrieve book list,  
   POST - post a book record) and `http://127.0.0.1:8000/api/book/<book_pk>` (GET - retrieve a book record).  
   For the book list, one can add a query variables `sort` and `filter`, for example:  
   `http://127.0.0.1:8000/api/book/list/?sort=rating&filter=true` - retrieves the book list sorted by highest  
   rating and with excluded zero-rating books ([screenshot of the result](https://imgur.com/a/6jbxI1Z)).

## Technologies used
