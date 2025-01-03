# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container (if you have one)
COPY requirements .

# Install any dependencies (if you have a requirements.txt)
RUN pip install --no-cache-dir -r requirements

# Copy the Python code into the container
COPY . .

# Set the entrypoint for the container to run the calculator
ENTRYPOINT ["python", "calculator.py"]
