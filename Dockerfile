FROM python:3.10
WORKDIR /topliga_parser/excel_processor
COPY requirements.txt requirements.txt

CMD ["python3", "-m venv venv"]
CMD ["source", "venv/bin/activate"]

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
#RUN chmod 755 .
COPY . .

CMD ["python3", "chatbot.py"]