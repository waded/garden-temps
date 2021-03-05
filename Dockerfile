FROM balenalib/raspberry-pi-python:3.7

RUN install_packages

CMD ["python", "garden-temps.py"]