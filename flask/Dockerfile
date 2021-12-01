FROM python:3.7-buster


RUN apt-get update

WORKDIR /workdir
COPY app.py /workdir
COPY SpeechRecognizer.py /workdir
COPY requirements.txt /workdir

RUN pip3 install --no-cache-dir -q -r /workdir/requirements.txt


CMD ["python", "app.py"]
