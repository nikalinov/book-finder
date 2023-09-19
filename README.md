# Book finder
* A script that finds books on the Glasgow University library resource, takes reviews from Goodreads, and structures it in a database within Django environment.
* After the script is run, the JSON object is formed from the book results and sent to the server.
* Using sorting and/or filtering queries in a url, one can retrieve the books without empty reviews and sorted by number of reviews/best rating.
## Table of contents:
* [Getting started](#getting-started)
* [Usage guide](#usage-guide)
* [Technologies used](#technologies-used)
## Getting started
0. Prerequisites: installed Python3 and some IDE/code editor which supports Python and Django (ideally PyCharm because of heavy Django support).
1. Set up a local copy of the repository.  
  1.1. Open a terminal and navigate to the directory that you would like the Book finder to be stored in;  
  1.2. In the terminal, run `git clone https://github.com/nikalinov/book_finder.git`  
  1.3. Navigate into the Book finder directory and create a virtual environment: `python3 -m venv <enter-venv-name-here>`  
  1.4. Activate the virtual environment:  
       `$ source <enter-venv-name-here>/bin/activate` (Linux/MacOS)  **or** `<enter-venv-name-here>\Scripts\activate.bat` (Windows)  
  1.5. Install the prerequisite modules/libraries from requirements.txt: `pip install -r requirements.txt`
  1.6. Create .env file and add a secret Django key there
## Usage guide
## Technologies used
