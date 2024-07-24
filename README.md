cd demo-socketio
create virtual environment & activate env follow below command
- sudo apt install python3-virtualenv
- virtualenv -p python3 venv
- source venv/bin/activate

install all packages
- pip install -r requirements.txt

run socketio using below command
- daphne -b 127.0.0.1 -p 8080 socket_test.asgi:application

run command for static files:
- python manage.py collectstatic
