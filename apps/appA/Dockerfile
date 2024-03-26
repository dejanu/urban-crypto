FROM python:3.8.13-slim-buster
WORKDIR /app
COPY . /app

# fix error: command 'gcc' failed: No such file or directory
# RUN apk add --no-cache gcc musl-dev linux-headers

RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP appa.py
EXPOSE 5000
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0" ]
