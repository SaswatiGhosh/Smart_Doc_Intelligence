FROM python:3.12-alpine

WORKDIR /Final_Project

COPY requirements.txt .


RUN pip install -r requirements.txt

COPY .. ..



WORKDIR /Final_Project/myproject_doc_intelligence

CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]

EXPOSE 3000


