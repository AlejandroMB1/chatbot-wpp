FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install pip-tools

COPY requirements.in .

RUN pip-compile --output-file=requirements.txt requirements.in

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]