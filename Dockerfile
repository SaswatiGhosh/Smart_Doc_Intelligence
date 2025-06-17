FROM python:3.12-alpine


WORKDIR /Final_Project

COPY requirements.txt .


RUN pip install -r requirements.txt

COPY . .

ENV AWS_DEFAULT_REGION=ap-south-1



WORKDIR /Final_Project/myproject_doc_intelligence


EXPOSE 3000

CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]

