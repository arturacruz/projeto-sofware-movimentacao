FROM python:bookworm

RUN "pip install -r requirements.txt"

ENTRYPOINT ["python", "app.py"]
