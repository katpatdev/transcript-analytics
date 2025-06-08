# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir: Disables the cache, which reduces the image size.
# --trusted-host pypi.python.org: Can help avoid SSL issues in some networks.
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application's code to the working directory
COPY . .

# Download NLTK data during the build
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app

# Run app.py when the container launches
# Use gunicorn for a production-ready server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]