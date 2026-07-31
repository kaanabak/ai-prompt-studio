FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/
COPY static/ static/

RUN useradd --create-home appuser \
 && mkdir -p /app/data \
 && chown -R appuser:appuser /app
USER appuser

ENV PROMPTFORGE_HOST=0.0.0.0 \
    PROMPTFORGE_PORT=5000 \
    PROMPTFORGE_DATA_DIR=/app/data

EXPOSE 5000
VOLUME ["/app/data"]

HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1

CMD ["python", "app.py"]
