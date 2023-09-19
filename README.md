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
       `git clone https://github.com/nikalinov/book_finder.git`
2. Navigate into the Book finder directory and create a virtual environment:  
       `python3 -m venv <enter-venv-name-here>`
3. Activate the virtual environment:  
   `$ source <enter-venv-name-here>/bin/activate` (Linux/MacOS)  
   **or**  
   `<enter-venv-name-here>\Scripts\activate.bat` (Windows)
4. Install the prerequisite modules/libraries from requirements.txt:  
   `pip install -r requirements.txt`
5. It is needed to create a personal Django secret key. For that, navigate to the 'book_finder' directory  
   (which is in the original 'book_finder' project directory) and run:  
   `python3 secret_key_generator.py`
## Usage guide
1. Navigate into the 'script' directory and run the command:
   `python3 find.py <enter-your-title-here> <enter-number-of-results-here>`;
   where the search query can be any phrase/word and the number must be at least 15.
   One can omit the number and it will  default 
## Technologies used
