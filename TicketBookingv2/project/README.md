# app.py

## Prerequisites

- Python3
- Node.js
- Redis

## Installation

```sh
#Install backend dependencies
pip install -r requirements.txt

#Install frontend dependencies:
npm install

#Running the Application

#Backend
python app.py

#Frontend
npm run serve


#Celery Tasks

#Celery Worker
celery -A app.celery worker -l info

#Celery Beat
celery -A app.celery beat --max-interval 2 -l info

#Redis Server
redis-server

#Mailhog
mailhog
```




