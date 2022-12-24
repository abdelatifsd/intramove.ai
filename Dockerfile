# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt #--no-cache-dir
RUN pip install -r requirements.txt 

EXPOSE 9999

#CMD ["python", "server.py","-m","development"]
