FROM python:3.10-slim-buster

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# CMD ["python3", "app.py"]
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]