1) You need to have docker installed
2) git clone this repo
3) To run webapp type: docker-compose up --build -d in cmd from project folder

To run tests:
  1) py -m venv myvenv -> activate venv
  2) pip install -r requirements.txt
  3) rename .env.template to .env
  4) pytest from root project folder while docker compose is up
  Go to http://127.0.0.1:8000/docs 
If there are module import errors:
  add project folder to PYTHONPATH variable: from project folder type: set PYTHONPATH=./ (on WINDOWS), export PYTHONPATH="$PYTHONPATH:$(pwd) (on Linux/MacOS)
