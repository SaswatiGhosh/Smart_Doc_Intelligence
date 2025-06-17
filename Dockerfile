FROM python:3

WORKDIR /Smart_Doc_Intelligence

COPY requirements.txt .


RUN pip install -r requirements.txt

COPY .. ..

ENV AWS_DEFAULT_REGION=ap-south-1

WORKDIR /myproject_doc_intelligence

CMD ["python3", "manage.py", "runserver", "0.0.0.0:3000"]

EXPOSE 3000


