## Project setup

```bash
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

The project needs to be configured with your Auth0 domain and client ID in order for the authentication flow to work.

To do this, replace the values within `auth.py` with your own Auth0 application credentials:

```bash
AUTH0_DOMAIN = '<YOUR AUTH0 DOMAIN>'
API_AUDIENCE = '<YOUR AUTH0 API IDENTIFIER>'
```

Also change the `database.py` with your own database credentials

```bash
conn = psycopg2.connect(
    database="<YOUR DATABASE NAME>",
    user="<YOUR DATABASE USER>",
    password="<YOUR DATABASE PASSWORD>",
    host="<YOUR DATABASE HOST>",
    port="<YOUR DATABASE PORT>"
)
```

## Prepare Database and Create Tables
```bash
python3 database.py -construct
```

## Running
```bash
hypercorn main:app --bind localhost:5000 --reload
```

### Resetting Database and Drop Tables
```bash
python3 database.py -reset
```