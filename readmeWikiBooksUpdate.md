This uses the gutendex repository which has built in APIs to recover the books.

The python file fetchData.py can be run to populate a database. Due to storage limitations, the current code is limited to 100 books and only a few attributes (title, author, gutenbergID, and gutenbergID link). 

In addition, the detchData.py file scrapes the img link of each book and stores along with the title.

Due to authors being a many to many relationship, it is stored in a seperate table. However, it can be accessed with the gutenberg ID on a seperate table.

To fetch new data run the following requirements
1. Install virtual environment with python (python -m venv venv
2. Activate virtual environment (for Windows venv\Scripts\activate)
3. Install the requirements (pip install -r requirements.txt)
4. Activate database or create new one. NOTE**: you will need to update the name of the database and secret key in the .env file found in gutendex folder
5. Once the .env file values has been correctly set, run python fetchData.py to populate database.
6 (optiona). Edit the fetchBooks definition if needing to add more or less books.
7 (optional). To edit the attributes to specify more data (download Count, copyright, etc), edit the fetchData.py to include more variables. Use the models.py to find variable names.
