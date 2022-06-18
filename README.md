## FastAPI Intro
**Book App**
* A project to introduce to FastAPI framework.
* An application is tiny warehouse to store books.
* In the app realize CRUD operations and integrated tests to test them.
* Python 3.10 is required
* Try to use this app on Heroku. ---> **[Link](https://km93-fast-api-book-app.herokuapp.com)** 

## Local Setup & Run

````
git clone https://github.com/konstantinMosin93/fast-api-intro.git
cd fast-api-intro
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
````

* To run App.
````
uvicorn main:app --reload
````
* The Book App Client will be available at http://127.0.0.1:8000/docs

## Run Tests
````
cd fast-api-intro
python -m pytest tests
````

## Run in Docker

````
cd fast-api-intro
docker build -t bookapp .
docker run -d --name testbookapp -p 80:80 bookapp
````
* The Book App Client will be available at http://127.0.0.1:80/docs

## Author

* Kostya Mosin
* Email: konstantinmosin@coherentsolutions.com