FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# set path to our python api file
ENV MODULE_NAME="app.main"
ENV PYTHONBUFFERED TRUE

RUN pip install -U --no-cache-dir --upgrade pip setuptools wheel

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy contents of project into docker
COPY ./ /app
