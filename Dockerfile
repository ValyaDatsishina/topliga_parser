FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt

CMD [ "python3", "-m venv venv"]
CMD [ "source", "venv/bin/activate"]

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .

LABEL authors="valentinabelezak"

ENTRYPOINT ["top", "-b"]