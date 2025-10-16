# 1. Use an official Python runtime as a parent image
# Using 'slim' is a good practice for smaller image sizes
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the dependency file and install dependencies first
# This is a key optimization. Docker caches layers. As long as requirements.txt
# doesn't change, Docker won't re-run this slow step.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Download the spaCy model. This also gets cached.
RUN python -m spacy download en_core_web_sm

# 5. Copy the rest of your application code into the container
COPY ./app /app

# 6. Expose the port the app runs on
EXPOSE 8000

# 7. Define the command to run your app when the container starts
# We use 0.0.0.0 to make the server accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]