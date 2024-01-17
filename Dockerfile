# The official Python runtime
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install the needed packages mentioned in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Port 80 available to the world outside the container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
