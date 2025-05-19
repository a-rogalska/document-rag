FROM python:3.13-slim

COPY requirements.txt .

RUN pip3 install -r requirements.txt

WORKDIR /app

COPY . .

EXPOSE 80

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=80", "--server.address=0.0.0.0"]