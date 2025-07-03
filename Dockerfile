FROM python:3.11-slim

WORKDIR /app

COPY requirements.in .

RUN pip install pip-tools && \
pip-compile --output-file=requirements.txt requirements.in && \
pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]