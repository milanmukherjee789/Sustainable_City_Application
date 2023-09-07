Start the python environment using server/Scripts/activate.
Then cd to server and use the command pip install -r requirements.txt.
Then cd to serverPython.
Make changes in Databases of settings.py in serverPython.
Create a database named twitter_data in MySQL.
Run the command python manage.py makemigrations.
Run the command python manage.py migrate.
To start the server use python manage.py runserver.
Run twitter.scraper.py separately. 
To get the data use <ipaddress>:<port>/list/ 
To post the data use <ipaddress>:<port>/add/ 
