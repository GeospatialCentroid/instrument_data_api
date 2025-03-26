# instrument_data_api


## Setup

### Downloading and setting-up django
    
1. Clone the project, and direct your terminal window to the project folder 
2. create virtual environment
    ```python -m venv venv```
3. Activate virtual environment
```source venv/bin/activate```
or on windows: 
```.\venv\scripts\Activate.ps1 ```

4. Install the requirements
With python and git installed
```pip install -r requirements.txt```
Note: if you add and python packages, be sure to run ```pip freeze > requirements.txt```

### Creating the database and required tables
With Postegres and PgAdmin installed

1. Create a server connection and database called 'instrument_manager'
2. With the virtual environment activated, run:
``` 
python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser
```
3. Enter details to create a superuser

### Starting the app
1. With the virtual environment activated, run:
```python manage.py runserver```
   
2. Navigate to http://127.0.0.1:8000/admin and enter the superuser details
