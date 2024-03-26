# Local setup

* Virtual EnvironmentError:

```bash
# create .venv virtual environment
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

* Start app:

```bash
export FLASK_APP=appa.py
flask run --host=0.0.0.0

# check endpoint
curl http://127.0.0.1:5000/now
```