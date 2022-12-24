# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt #--no-cache-dir

RUN pip install faiss-cpu sentence-transformers fastapi uvicorn pydantic black stripe python-dotenv numpy bson
RUN python -m pip install "pymongo[srv]"

RUN mkdir data

EXPOSE 8000

#CMD ["python", "server.py","-m","development"]
