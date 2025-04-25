uv init 
uv run main.py
.venv\Scripts\activate
uv add django
uv pip install pip
django-admin startproject myproject_doc_intelligence
cd ..
pip install django-tailwind
python manage.py migrate
python manage.py runserver