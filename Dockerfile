FROM python:3.9

WORKDIR app/
COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app.py .
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
EXPOSE 8501
