#! /bin/bash
USER=$(cat .env | grep DB_USER | sed -n 's/.*= *\(.*\)/\1/p')
PASS=$(cat .env | grep DB_PASS | sed -n 's/.*= *\(.*\)/\1/p')
NAME=$(cat .env | grep DB_NAME | sed -n 's/.*= *\(.*\)/\1/p')



python3 -mvenv ./dev && source ./dev/bin/activate
pip install -r requirements.txt
if alembic show 1 ; then echo "Nothing to migrate"; else
                alembic revision --autogenerate -m "Add Message Model" --rev 1
                alembic upgrade 1;
fi

cd ./src
python3 ./main.py
