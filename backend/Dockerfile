# Production image for the FastAPI backend.
#
# Migrations are deliberately NOT run automatically on container start
# (no `alembic upgrade head` baked into the entrypoint) - running them as
# an explicit deploy step avoids multiple replicas racing to migrate the
# same database on startup. See the README's Deployment section.
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first so this layer is cached unless requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
