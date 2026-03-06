FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1

ARG OBSIDIAN_HOST=192.168.1.16
ARG OBSIDIAN_API_KEY=""
ENV OBSIDIAN_HOST=$OBSIDIAN_HOST
ENV OBSIDIAN_API_KEY=$OBSIDIAN_API_KEY

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY obsidian_server.py .
RUN useradd -m -u 1000 mcpuser && chown -R mcpuser:mcpuser /app
USER mcpuser
CMD ["python", "obsidian_server.py"]