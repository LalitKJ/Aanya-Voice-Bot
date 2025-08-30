# Use a slim Python image
FROM python:3.13-slim-bullseye

# Copy the uv binary to the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application code to the container
COPY . /app

# Set the working directory
WORKDIR /app

# Install dependencies
RUN uv sync --frozen --no-cache

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the application
CMD ["/app/.venv/bin/uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]