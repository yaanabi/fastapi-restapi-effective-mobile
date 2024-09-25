You need to have docker installed
git clone this repo
To run webapp type: docker-compose up --build -d in cmd from project folder

To run tests:
  py -m venv myvenv -> activate venv
  pip install -r requirements.txt
  rename .env.template to .env
  pytest from root project folder while docker compose is up
  Go to http://127.0.0.1:8000/docs 
