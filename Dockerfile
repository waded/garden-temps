FROM balenalib/raspberry-pi-python:3.7

RUN install_packages

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . ./

CMD ["python", "garden-temps.py"]