# FILE: Dockerfile
# --- REWRITTEN FOR API-ONLY ---

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install only essential system dependencies.
# ffmpeg is kept in case you want to do any future audio format conversion.
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies.
# This step will now be significantly faster.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download SpaCy model
RUN python -m spacy download en_core_web_sm

# Copy your application code from the local 'app' directory into the container's '/app' directory
COPY ./app .

# Expose port
EXPOSE 8000

# Start FastAPI. This command is simple and relies on the flattened structure.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]