# Using lightweight Python image from Docker Hub as starting image
FROM python:3.12-slim
# Copy the current directory contents into the container at /app
COPY . /app
# Change the working directory
WORKDIR /app
# Install the required Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
