#### Commands used to start the project

> uv init
> uv run main.py
> .venv\Scripts\activate
> uv add django
> uv pip install pip
> django-admin startproject myproject_doc_intelligence
> cd ..
> pip install django-tailwind
> python manage.py migrate
> python manage.py runserver

-   **uv add** should be used to add dependencies in the .toml file

-   Use **git and uv add** operation in the parent folder

#### To install packages from .toml file

> uv pip install -r pyproject.toml


WORKFLOW

File uploaded to S3 → Lambda 1 runs → Textract job starts → on job completion, SNS sends notification → Lambda 2 is triggered, processes the results, and logs the extracted lines.