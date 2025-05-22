FROM python:3.9
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
