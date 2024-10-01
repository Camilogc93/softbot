# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY app.py .
COPY functions.py .
COPY vectorstore_setup.py .
COPY model_embedding.py .
COPY .env .

# Expose port 8000 to the outside world
EXPOSE 5000

# Command to run the FastAPI app using Uvicorn
CMD ["uvicorn", "app:fastapi_app", "--host", "0.0.0.0", "--port", "5000"]
